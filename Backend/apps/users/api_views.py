from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer, UserSerializer
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'Usuario registrado correctamente.',
                'user': UserSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileAPIView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class AdminUserListAPIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        from .models import CustomUser
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class PasswordResetRequestAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            frontend_url = request.headers.get('Origin') or 'https://reserva-laguna-de-la-bolsa.vercel.app'
            reset_url = f"{frontend_url}/pages/reset-password.html?uid={uid}&token={token}"
            
            # --- Enviar usando Resend API (HTTP) para evitar bloqueos SMTP ---
            import requests
            
            resend_key = settings.RESEND_API_KEY
            if not resend_key:
                return Response({'error': 'Configuración de correo incompleta (Falta API Key).'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            try:
                # Nota: Resend requiere que el remitente esté verificado. 
                # Si no tienes dominio verificado, usa 'onboarding@resend.dev' o el que Resend te asigne.
                email_data = {
                    "from": "Reserval <onboarding@resend.dev>",
                    "to": [email],
                    "subject": "Restablecer contraseña - Reserva Laguna De La Bolsa",
                    "html": f"""
                        <div style="font-family: sans-serif; max-width: 600px; margin: auto;">
                            <h2>Hola {user.first_name},</h2>
                            <p>Haz solicitado restablecer tu contraseña para tu cuenta en Reserva Laguna De La Bolsa.</p>
                            <p>Haz clic en el botón de abajo para continuar:</p>
                            <a href="{reset_url}" style="background-color: #29B6F6; color: white; padding: 12px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 20px 0;">Restablecer Contraseña</a>
                            <p>Si no solicitaste este cambio, puedes ignorar este correo.</p>
                            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
                            <p style="font-size: 12px; color: #999;">Este es un correo automático, por favor no respondas.</p>
                        </div>
                    """
                }
                
                res = requests.post(
                    "https://api.resend.com/emails",
                    headers={
                        "Authorization": f"Bearer {resend_key}",
                        "Content-Type": "application/json"
                    },
                    json=email_data
                )
                
                if res.status_code not in [200, 201]:
                    return Response({'error': f'Error de Resend: {res.text}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            except Exception as e:
                return Response({'error': f'Error al procesar el envío: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({'message': 'Se ha enviado un correo con instrucciones para restablecer tu contraseña.'})
        except User.DoesNotExist:
            # Por seguridad, no revelamos si el correo existe o no
            return Response({'message': 'Si el correo está registrado, recibirás instrucciones en breve.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('password')
        if not uid or not token or not new_password:
            return Response({'error': 'Todos los campos son obligatorios'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Contraseña restablecida correctamente. Ya puedes iniciar sesión.'})
            else:
                return Response({'error': 'El enlace de recuperación es inválido o ha expirado.'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Enlace inválido.'}, status=status.HTTP_400_BAD_REQUEST)