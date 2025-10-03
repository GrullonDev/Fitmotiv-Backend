# 🏋️‍♂️ FitMotiv Backend API

API completa de fitness y motivación desarrollada con FastAPI que incluye sistemas avanzados de seguimiento de progreso, notificaciones push inteligentes y motivación diaria gamificada.

## ✨ Características Principales

### 🔐 Sistema de Autenticación
- Autenticación JWT con refresh tokens
- Gestión completa de usuarios
- Verificación de email y recuperación de contraseña

### � Sistema de Tracking de Progreso
- Objetivos personalizables con múltiples métricas
- Analytics y tendencias automatizadas
- Dashboard completo de progreso
- Logging automático de actividades

### 🔔 Sistema de Notificaciones Push
- Soporte para FCM (Android) y APNS (iOS)
- Configuraciones granulares por usuario
- Notificaciones inteligentes basadas en actividad
- Historial completo de notificaciones

### � Sistema de Motivación Diaria
- **15 quotes motivacionales** en español categorizados
- **10 desafíos diarios** con diferentes dificultades  
- **Sistema de puntos y recompensas** gamificado
- **5 niveles de motivación** progresivos
- **Tracking de streaks** y consistencia
- **Dashboard motivacional** completo

### 🏃‍♂️ Gestión de Ejercicios y Rutinas
- Base de datos completa de ejercicios
- Rutinas personalizables
- Tracking de entrenamientos

## 🛠️ Tecnologías

- **FastAPI** - Framework web moderno y rápido
- **SQLAlchemy** - ORM para base de datos
- **Pydantic** - Validación de datos con schemas
- **JWT** - Autenticación con tokens seguros
- **SQLite** - Base de datos para desarrollo
- **PostgreSQL** - Base de datos para producción
- **Email Validator** - Validación de direcciones de correo

## 🏗️ Estructura del proyecto

```
fitmotiv-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Aplicación principal FastAPI
│   ├── config.py                  # Configuración y variables de entorno
│   ├── database.py                # Configuración de base de datos
│   ├── models.py                  # Modelos SQLAlchemy
│   ├── schemas.py                 # Esquemas Pydantic
│   ├── security.py                # Funciones de seguridad y JWT
│   ├── blacklist.py               # Blacklist de tokens
│   └── routers/
│       ├── __init__.py
│       ├── auth_router.py         # Autenticación y usuarios
│       ├── user_router.py         # Gestión de usuarios
│       ├── exercise_router.py     # Ejercicios y rutinas
│       ├── progress_router.py     # Tracking de progreso
│       ├── notification_router.py # Sistema de notificaciones
│       └── motivation_router.py   # Sistema de motivación diaria
├── scripts/
│   ├── populate_exercises.py      # Poblar ejercicios de ejemplo
│   ├── populate_progress.py       # Poblar datos de progreso
│   ├── populate_motivation.py     # Poblar sistema de motivación
│   └── test_system.py             # Pruebas del sistema
├── alembic/                       # Configuración de migraciones
├── requirements.txt               # Dependencias optimizadas
├── test.db                        # Base de datos SQLite (desarrollo)
└── README.md
```

## 🚀 Instalación y Configuración Local

### 📋 Prerrequisitos
- Python 3.9 o superior
- pip (incluido con Python)

### ⚡ Inicio Rápido

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd fitmotiv-backend
   ```

2. **Instalar dependencias**
   ```bash
   # Usar python3 -m pip para evitar problemas de PATH
   python3 -m pip install -r requirements.txt
   ```

3. **Poblar base de datos con datos de ejemplo**
   ```bash
   # Poblar ejercicios básicos
   python3 scripts/populate_exercises.py
   
   # Poblar datos de progreso de ejemplo
   python3 scripts/populate_progress.py
   
   # Poblar sistema de motivación (quotes, desafíos, recompensas)
   python3 scripts/populate_motivation.py
   ```

4. **Iniciar el servidor**
   ```bash
   python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **¡Listo! 🎉**
   - **API**: http://localhost:8000
   - **Documentación interactiva**: http://localhost:8000/docs
   - **Documentación alternativa**: http://localhost:8000/redoc

### 🔧 Configuración Avanzada (Opcional)

Si quieres personalizar la configuración, crea un archivo `.env`:

```bash
# Variables de entorno opcionales
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./test.db
```

## 🎮 Sistema de Gamificación

### 🏆 Puntos y Recompensas
- **10-35 puntos** por desafío completado según dificultad
- **Bonus automático** por mantener streaks
- **8 recompensas** desbloqueables por logros

### 📈 Niveles de Motivación
1. 🌱 **Principiante** (0-99 puntos) - Desafíos básicos
2. 🌿 **Motivado** (100-299 puntos) - Desafíos medios + quotes premium
3. 🌳 **Dedicado** (300-599 puntos) - Desafíos avanzados + estadísticas
4. 🏆 **Campeón** (600-999 puntos) - Desafíos exclusivos + insignias especiales
5. 👑 **Leyenda** (1000+ puntos) - Acceso VIP + coach virtual

### 🔥 Sistema de Streaks
- **Tracking automático** de días consecutivos
- **Múltiples tipos**: workout, challenge, login, progress_update
- **Recompensas especiales** por hitos: 7, 30, 100 días

## 💻 Uso en desarrollo

```bash
# Forma recomendada - con reload automático
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Para desarrollo sin reload (más estable para pruebas)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Testing del Sistema

```bash
# Ejecutar pruebas automáticas del sistema
python3 scripts/test_system.py

# Probar endpoint específico
curl http://localhost:8000/api/motivation/quote-of-the-day
```

## 📖 Documentación de la API

Una vez iniciado el servidor, accede a:
- **Documentación interactiva (Swagger)**: `http://localhost:8000/docs`
- **Documentación alternativa (ReDoc)**: `http://localhost:8000/redoc`
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`

## 🛠️ Endpoints principales

### 🔐 Autenticación
- `POST /api/auth/register` - Registrar usuario
- `POST /api/auth/login` - Iniciar sesión
- `GET /api/auth/me` - Obtener perfil del usuario actual
- `POST /api/auth/refresh` - Renovar token
- `POST /api/auth/logout` - Cerrar sesión

### 👤 Usuarios
- `GET /api/users/me` - Obtener perfil del usuario
- `PUT /api/users/me` - Actualizar perfil

### 💪 Sistema de Motivación Diaria
- `GET /api/motivation/quote-of-the-day` - Quote motivacional del día
- `GET /api/motivation/challenge-of-the-day` - Desafío del día
- `GET /api/motivation/dashboard` - Dashboard de motivación completo
- `POST /api/motivation/complete-challenge` - Completar desafío
- `GET /api/motivation/streaks` - Streaks del usuario
- `GET /api/motivation/levels` - Niveles de motivación disponibles
- `GET /api/motivation/rewards` - Recompensas disponibles
- `GET /api/motivation/challenges/available` - Desafíos disponibles

### 📊 Tracking de Progreso
- `GET /api/progress/dashboard` - Dashboard completo de progreso
- `POST /api/progress/goals` - Crear objetivo personalizado
- `GET /api/progress/analytics` - Análisis de tendencias
- `POST /api/progress/log-activity` - Registrar actividad
- `GET /api/progress/goals/mine` - Mis objetivos

### 🔔 Sistema de Notificaciones
- `POST /api/notifications/register-token` - Registrar token de dispositivo
- `GET /api/notifications/settings` - Configuraciones de notificación
- `POST /api/notifications/send` - Enviar notificación
- `GET /api/notifications/history` - Historial de notificaciones

### 🏃‍♂️ Ejercicios y Rutinas
- `GET /api/exercises` - Listar ejercicios disponibles
- `POST /api/exercises` - Crear ejercicio personalizado
- `GET /api/routines` - Listar rutinas del usuario
- `POST /api/routines` - Crear rutina personalizada

## 📱 Ejemplo de uso para Frontend

### JavaScript/React
```javascript
// Configuración base
const API_BASE_URL = 'http://localhost:8000';

// Obtener quote del día (sin autenticación)
const getDailyQuote = async () => {
  const response = await fetch(`${API_BASE_URL}/api/motivation/quote-of-the-day`);
  return response.json();
};

// Login
const login = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `username=${email}&password=${password}`
  });
  return response.json();
};

// Dashboard de motivación (requiere autenticación)
const getMotivationDashboard = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/motivation/dashboard`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return response.json();
};
```

## 💾 Base de datos

### Desarrollo (Automático)
El proyecto usa **SQLite** por defecto para desarrollo local. La base de datos se crea automáticamente al iniciar el servidor.

### Datos de Ejemplo Incluidos
- ✅ **15 quotes motivacionales** en español categorizados
- ✅ **10 desafíos diarios** con diferentes dificultades
- ✅ **8 recompensas** por logros y hitos
- ✅ **5 niveles** de motivación progresivos
- ✅ **Ejercicios básicos** para entrenamientos

## 🔧 Comandos Útiles

### Gestión de datos
```bash
# Repoblar base de datos (si necesitas datos frescos)
python3 scripts/populate_exercises.py
python3 scripts/populate_progress.py
python3 scripts/populate_motivation.py

# Probar sistema completo
python3 scripts/test_system.py
```

### Desarrollo
```bash
# Iniciar servidor con reload automático
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Iniciar servidor estable (para pruebas)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Verificar dependencias
python3 -m pip list | grep fastapi
```

## 🚀 Funcionalidades Implementadas

### ✅ Sistemas Completados
- **Sistema de Autenticación JWT** con gestión de usuarios
- **Sistema de Motivación Diaria** con gamificación completa
- **Sistema de Tracking de Progreso** con analytics
- **Sistema de Notificaciones Push** inteligentes
- **Base de datos de Ejercicios** y rutinas
- **API REST completa** con documentación automática

### 📊 Métricas del Proyecto
- **50+ endpoints** distribuidos en 6 routers
- **20+ modelos** de base de datos
- **60+ esquemas** Pydantic para validación
- **15 quotes** motivacionales en español
- **10 desafíos** diarios con gamificación
- **5 niveles** de motivación progresivos

## ❗ Solución de Problemas

### Error: "command not found: pip"
```bash
# Usar python3 -m pip en lugar de pip
python3 -m pip install -r requirements.txt
```

### Error: "Port already in use"
```bash
# Buscar proceso usando el puerto
lsof -i :8000
# Terminar proceso
kill -9 <PID>
# O usar otro puerto
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8001
```

### Error de base de datos
```bash
# Eliminar base de datos y recrear
rm test.db
# Repoblar datos
python3 scripts/populate_exercises.py
python3 scripts/populate_motivation.py
```

## 🤝 Contribución

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

---

**¡FitMotiv 3.0.0 está listo para motivar a los usuarios en su viaje fitness! 💪**

*Desarrollado con FastAPI, SQLAlchemy y mucha motivación 🚀*