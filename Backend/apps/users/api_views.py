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
            try:
                send_mail(
                    'Restablecer contraseña - Reserva Laguna De La Bolsa',
                    f'Hola {user.first_name},\n\nHaz clic en el siguiente enlace para restablecer tu contraseña:\n{reset_url}\n\nSi no solicitaste este cambio, puedes ignorar este correo.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
            except Exception as mail_error:
                return Response({'error': f'Error al enviar el correo. ({str(mail_error)})'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response({'message': 'Se ha enviado un correo con instrucciones para restablecer tu contraseña.'})
        except User.DoesNotExist:
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