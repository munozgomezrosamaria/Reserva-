# Reserva Natural Laguna de la Bolsa 🌿

Plataforma web para la Reserva Natural Laguna de la Bolsa. Permite a los visitantes explorar servicios, hacer reservaciones y conocer la reserva.

## Estructura del Proyecto

```
Reserval/
├── Backend/          → Django REST API (Deploy en Render)
│   ├── apps/         → Apps Django (users, services, reservations)
│   ├── config/       → Configuración Django
│   ├── manage.py
│   ├── requirements.txt
│   ├── render.yaml   → Config deploy Render
│   └── build.sh      → Script de build
├── Frontend/         → Sitio estático (Deploy en Vercel)
│   ├── index.html    → Página principal
│   ├── pages/        → Login, register, services, etc.
│   ├── css/          → Estilos
│   ├── js/           → API client + lógica
│   └── vercel.json   → Config deploy Vercel
```

## Configuración Local

### Backend

```bash
cd Backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Crear archivo .env (ver .env.example)
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd Frontend
npx serve .
# Abrir http://localhost:3000
```

## Deploy

| Componente | Plataforma | URL |
|-----------|-----------|-----|
| Frontend  | Vercel    | `https://tu-app.vercel.app` |
| Backend   | Render    | `https://tu-app.onrender.com` |
| Database  | Railway   | PostgreSQL |

### Variables de Entorno (Backend - Render)

| Variable | Descripción |
|----------|------------|
| `SECRET_KEY` | Clave secreta de Django |
| `DATABASE_URL` | URL de PostgreSQL (Railway) |
| `DEBUG` | `False` en producción |
| `ALLOWED_HOSTS` | `.onrender.com` |
| `CORS_ALLOWED_ORIGINS` | URL del frontend en Vercel |

### Configuración Frontend

Editar `Frontend/js/api.js` y cambiar la URL del backend:

```javascript
const API_BASE_URL = 'https://tu-backend.onrender.com/api';
```

## API Endpoints

| Método | Endpoint | Descripción |
|--------|---------|-------------|
| POST | `/api/token/` | Obtener JWT tokens |
| POST | `/api/token/refresh/` | Refrescar token |
| POST | `/api/users/register/` | Registrar usuario |
| GET | `/api/users/profile/` | Perfil del usuario |
| GET | `/api/services/` | Listar servicios |
| GET | `/api/services/:id/` | Detalle de servicio |
| GET | `/api/reservations/` | Listar reservas del usuario |
| POST | `/api/reservations/` | Crear reserva |

## Tecnologías

- **Backend**: Django 5+, Django REST Framework, SimpleJWT
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Base de datos**: PostgreSQL
- **Deploy**: Vercel + Render + Railway
