# 🏋️‍♂️ FitMotiv Backend API

## 🎯 Descripción

**FitMotiv** es una API completa de fitness y motivación desarrollada con FastAPI que incluye sistemas avanzados de seguimiento de progreso, notificaciones push inteligentes y motivación diaria gamificada.

## ✨ Características Principales

### 📊 Sistema de Tracking de Progreso
- Objetivos personalizables con múltiples métricas
- Analytics y tendencias automatizadas
- Dashboard completo de progreso
- Logging automático de actividades

### 🔔 Sistema de Notificaciones Push
- Soporte para FCM (Android) y APNS (iOS)
- Configuraciones granulares por usuario
- Notificaciones inteligentes basadas en actividad
- Historial completo de notificaciones

### 💪 Sistema de Motivación Diaria
- **15 quotes motivacionales** en español categorizados
- **10 desafíos diarios** con diferentes dificultades  
- **Sistema de puntos y recompensas** gamificado
- **5 niveles de motivación** progresivos
- **Tracking de streaks** y consistencia
- **Dashboard motivacional** completo

## 🚀 Instalación

### Prerrequisitos
- Python 3.9+
- SQLite (incluido)

### Configuración

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd fitmotiv-backend
```

2. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

3. **Configurar variables de entorno**
```bash
# Crear archivo .env con las siguientes variables:
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

4. **Inicializar base de datos**
```bash
# Ejecutar migraciones
alembic upgrade head

# Poblar datos de ejemplo
python scripts/populate_exercises.py
python scripts/populate_motivation.py
```

5. **Iniciar servidor**
```bash
uvicorn app.main:app --reload
```

## 📖 Documentación de la API

Una vez iniciado el servidor, accede a:
- **Documentación interactiva**: http://localhost:8000/docs
- **Documentación alternativa**: http://localhost:8000/redoc

## 🛠️ Endpoints Principales

### 🔐 Autenticación
- `POST /api/auth/register` - Registro de usuario
- `POST /api/auth/login` - Inicio de sesión
- `GET /api/auth/me` - Perfil del usuario actual

### 📊 Progreso
- `GET /api/progress/dashboard` - Dashboard completo
- `POST /api/progress/goals` - Crear objetivo
- `GET /api/progress/analytics` - Análisis de tendencias
- `POST /api/progress/log-activity` - Registrar actividad

### 🔔 Notificaciones
- `POST /api/notifications/register-token` - Registrar token de dispositivo
- `GET /api/notifications/settings` - Configuraciones de notificación
- `POST /api/notifications/send` - Enviar notificación
- `GET /api/notifications/history` - Historial de notificaciones

### 💪 Motivación
- `GET /api/motivation/quote-of-the-day` - Quote motivacional del día
- `GET /api/motivation/challenge-of-the-day` - Desafío del día
- `GET /api/motivation/dashboard` - Dashboard de motivación
- `POST /api/motivation/complete-challenge` - Completar desafío
- `GET /api/motivation/streaks` - Streaks del usuario
- `GET /api/motivation/levels` - Niveles de motivación
- `GET /api/motivation/rewards` - Recompensas disponibles

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

## 🗄️ Base de Datos

### Modelos Principales
- **User, UserProfile** - Gestión de usuarios
- **Exercise, Routine, UserRoutine** - Ejercicios y rutinas
- **Goal, ProgressLog** - Objetivos y progreso
- **Notification, NotificationSetting** - Sistema de notificaciones
- **DailyQuote, DailyChallenge** - Contenido motivacional
- **UserStreak, MotivationReward** - Gamificación

## 🧪 Testing

```bash
# Poblar datos de prueba
python scripts/populate_motivation.py

# Ejecutar pruebas del sistema
python scripts/test_system.py

# Verificar endpoints manualmente
curl http://localhost:8000/api/motivation/quote-of-the-day
```

## 🏗️ Arquitectura

```
app/
├── main.py              # Aplicación principal FastAPI
├── models.py            # Modelos SQLAlchemy
├── schemas.py           # Esquemas Pydantic
├── database.py          # Configuración de BD
├── security.py          # Autenticación JWT
└── routers/
    ├── auth_router.py       # Autenticación
    ├── user_router.py       # Gestión de usuarios
    ├── exercise_router.py   # Ejercicios y rutinas
    ├── progress_router.py   # Tracking de progreso
    ├── notification_router.py # Notificaciones
    └── motivation_router.py   # Sistema de motivación
```

## 🚀 Próximos Pasos

1. **App Mobile** - Desarrollar aplicación móvil (React Native/Flutter)
2. **Analytics Avanzados** - Más métricas y reportes personalizados
3. **Social Features** - Sistema de amigos y competencias
4. **AI Coaching** - Recomendaciones inteligentes con ML
5. **Integración Wearables** - Conectar con dispositivos fitness

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**¡FitMotiv está listo para motivar a los usuarios en su viaje fitness! 💪**

*Desarrollado con FastAPI, SQLAlchemy y mucha motivación 🚀*