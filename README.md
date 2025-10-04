# FitMotiv Backend API v1.0

<div align="center">
<h3>Una API completa de backend para aplicación de fitness y motivación con perfiles extendidos, seguimiento avanzado de progreso y sistema de objetivos inteligente.</h3>
</div>

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-orange.svg)

## <span style="color: #2563eb;">⭐</span> Funcionalidades Principales v1.0

### <span style="colo### v1.0.0 (Octubre 2025) - **Primera Versión Estable**
- <span style="color: #059669;">▶</span> **Perfiles de usuario extendidos** con 40+ campos personalizables
- <span style="color: #059669;">▶</span> **Sistema de objetivos SMART** con seguimiento automático de progreso
- <span style="color: #059669;">▶</span> **Seguimiento avanzado de peso** con análisis de tendencias y proyecciones
- <span style="color: #059669;">▶</span> **Workout of the Day** con recomendaciones personalizadas y sistema de calificación
- <span style="color: #059669;">▶</span> **Dashboard inteligente** con análisis completo de progreso y estadísticas
- <span style="color: #059669;">▶</span> **Sistema de carga de archivos** para fotos de perfil, portada y progreso
- <span style="color: #059669;">▶</span> **API completamente compatible** con aplicaciones móviles modernas
- <span style="color: #2563eb;">▶</span> **Autenticación JWT robusta** con refresh tokens y blacklist
- <span style="color: #dc2626;">▶</span> **Sistema de motivación gamificado** con quotes, desafíos y recompensas
- <span style="color: #7c3aed;">▶</span> **Sistema de notificaciones inteligentes** para FCM y APNS
- <span style="color: #2563eb;">▶</span> **Análisis y métricas avanzadas** con proyecciones estadísticas
- <span style="color: #dc2626;">▶</span> **Base de datos completa** de ejercicios y rutinas
- <span style="color: #2563eb;">▶</span> **Documentación automática** con Swagger UI y ReDoc</span> Características Principales
- **<span style="color: #2563eb;">●</span> Perfiles de Usuario Extendidos**: Información completa de fitness, salud y preferencias personales
- **<span style="color: #059669;">●</span> Sistema de Objetivos Avanzado**: Objetivos SMART con seguimiento automático de hitos y progreso
- **<span style="color: #7c3aed;">●</span> Seguimiento de Peso Corporal**: Análisis de tendencias, proyecciones y fotos de progreso
- **<span style="color: #dc2626;">●</span> Workout of the Day**: Rutinas diarias personalizadas con sistema de calificación y recomendaciones
- **<span style="color: #059669;">●</span> Dashboard Inteligente**: Resumen completo de progreso y estadísticas detalladas
- **<span style="color: #2563eb;">●</span> Carga de Archivos**: Fotos de perfil, portada y progreso con gestión automática
- **<span style="color: #7c3aed;">●</span> Análisis Avanzados**: Estadísticas detalladas y proyecciones de progreso basadas en datos

### <span style="color: #dc2626;">💪</span> Sistema de Motivación y Gamificación
- **15 quotes motivacionales** en español categorizados por tema
- **10 desafíos diarios** con diferentes niveles de dificultad
- **Sistema de puntos y recompensas** gamificado con 8 logros desbloqueables
- **5 niveles de motivación** progresivos (Principiante → Leyenda)
- **Tracking de streaks** para mantener la consistencia
- **Dashboard motivacional** completo con métricas de engagement

### <span style="color: #059669;">🔐</span> Sistema de Autenticación Robusto
- Autenticación JWT con refresh tokens seguros
- Gestión completa de usuarios con verificación
- Recuperación de contraseña y verificación de email
- Blacklist de tokens para logout seguro

### <span style="color: #2563eb;">🔔</span> Sistema de Notificaciones Inteligentes
- Soporte completo para FCM (Android) y APNS (iOS)
- Configuraciones granulares por usuario y tipo de notificación
- Notificaciones inteligentes basadas en actividad y progreso
- Historial completo con estadísticas de engagement

## <span style="color: #7c3aed;">🛠️</span> Stack Tecnológico

- **FastAPI 0.100+** - Framework web moderno con documentación automática
- **SQLAlchemy 2.0+** - ORM avanzado con soporte async
- **Pydantic v2** - Validación de datos con schemas tipados
- **JWT** - Autenticación segura con tokens
- **SQLite** - Base de datos rápida para desarrollo
- **PostgreSQL** - Base de datos escalable para producción
- **Alembic** - Gestión de migraciones de base de datos
- **Python 3.9+** - Lenguaje base con tipado estático

## <span style="color: #2563eb;">🏗️</span> Arquitectura del Proyecto

```
fitmotiv-backend/
├── ```
app/
│   ├── __init__.py
│   ├── main.py                     # <span style="color: #dc2626;">●</span> Aplicación principal FastAPI
│   ├── config.py                   # <span style="color: #059669;">●</span> Configuración y variables de entorno
│   ├── database.py                 # <span style="color: #2563eb;">●</span> Configuración de base de datos
│   ├── models.py                   # <span style="color: #7c3aed;">●</span> Modelos SQLAlchemy extendidos
│   ├── schemas.py                  # <span style="color: #059669;">●</span> Schemas Pydantic para validación
│   ├── security.py                 # <span style="color: #dc2626;">●</span> Funciones de seguridad y JWT
│   ├── blacklist.py                # <span style="color: #7c3aed;">●</span> Blacklist de tokens
│   └── routers/
│       ├── __init__.py
│       ├── auth_router.py          # <span style="color: #dc2626;">●</span> Autenticación y usuarios
│       ├── user_router.py          # <span style="color: #2563eb;">●</span> Gestión de usuarios
│       ├── profile_router.py       # <span style="color: #059669;">●</span> Gestión de perfiles extendidos
│       ├── goals_router.py         # <span style="color: #059669;">●</span> Sistema de objetivos SMART
│       ├── weight_progress_router.py # <span style="color: #059669;">●</span> Seguimiento de peso corporal
│       ├── workouts_router.py      # <span style="color: #059669;">●</span> Rutinas diarias personalizadas
│       ├── exercise_router.py      # <span style="color: #dc2626;">●</span> Ejercicios y rutinas
│       ├── routine_router.py       # <span style="color: #7c3aed;">●</span> Rutinas de entrenamiento
│       ├── nutrition_router.py     # <span style="color: #059669;">●</span> Gestión nutricional
│       ├── progress_router.py      # <span style="color: #2563eb;">●</span> Tracking de progreso
│       ├── notification_router.py  # <span style="color: #dc2626;">●</span> Sistema de notificaciones
│       └── motivation_router.py    # <span style="color: #dc2626;">●</span> Sistema de motivación diaria
├── scripts/
│   ├── init_database.py            # <span style="color: #059669;">●</span> Script maestro de inicialización
│   ├── populate_exercises.py       # <span style="color: #dc2626;">●</span> Poblar ejercicios de ejemplo
│   ├── populate_workouts.py        # <span style="color: #059669;">●</span> Poblar rutinas semanales
│   ├── populate_progress.py        # <span style="color: #2563eb;">●</span> Poblar datos de progreso
│   ├── populate_motivation.py      # <span style="color: #dc2626;">●</span> Poblar sistema de motivación
│   └── test_system.py              # <span style="color: #7c3aed;">●</span> Pruebas del sistema
├── uploads/                        # <span style="color: #059669;">●</span> Directorio para archivos subidos
│   ├── profiles/                   # <span style="color: #2563eb;">●</span> Fotos de perfil
│   ├── progress/                   # <span style="color: #2563eb;">●</span> Fotos de progreso
│   └── covers/                     # <span style="color: #2563eb;">●</span> Fotos de portada
├── alembic/                        # <span style="color: #059669;">●</span> Configuración de migraciones
├── requirements.txt                # <span style="color: #7c3aed;">●</span> Dependencias optimizadas
├── .env                           # <span style="color: #059669;">●</span> Variables de entorno
├── test.db                        # <span style="color: #2563eb;">●</span> Base de datos SQLite (desarrollo)
└── README.md                      # <span style="color: #2563eb;">●</span> Esta documentación
```

## <span style="color: #dc2626;">⚡</span> Instalación y Configuración

### <span style="color: #2563eb;">📋</span> Prerrequisitos
- **Python 3.9+** (recomendado 3.11+)
- **pip** (incluido con Python)
- **Git** para clonar el repositorio

### <span style="color: #dc2626;">⚡</span> Inicio Rápido (5 minutos)

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/GrullonDev/Fitmotiv-Backend.git
   cd fitmotiv-backend
   ```

2. **Instalar dependencias**
   ```bash
   # Usar python3 -m pip para evitar problemas de PATH
   python3 -m pip install -r requirements.txt
   ```

3. **Inicializar base de datos con datos de ejemplo**
   ```bash
   # Script maestro que inicializa todo automáticamente
   python3 scripts/init_database.py
   ```

4. **Iniciar el servidor**
   ```bash
   python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **¡Listo! 🎉**
   - **API**: http://localhost:8000
   - **Documentación interactiva**: http://localhost:8000/docs
   - **Documentación alternativa**: http://localhost:8000/redoc

### 🔧 Configuración de Variables de Entorno

El proyecto incluye un archivo `.env` preconfigurado, pero puedes personalizarlo:

```bash
# Configuración de la base de datos
DATABASE_URL=sqlite:///./test.db
# Para PostgreSQL: postgresql://username:password@localhost/fitmotiv_db

# Configuración JWT
SECRET_KEY=tu-clave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Configuración de Email (opcional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=tu-email@gmail.com
EMAIL_HOST_PASSWORD=tu-password
```

## <span style="color: #2563eb;">📊</span> API Endpoints Completos

### <span style="color: #059669;">🔐</span> Autenticación y Usuarios
```
POST   /api/auth/register           # Registro de usuario
POST   /api/auth/login              # Inicio de sesión
POST   /api/auth/refresh            # Renovar token
POST   /api/auth/logout             # Cerrar sesión
GET    /api/auth/me                 # Obtener perfil actual
GET    /api/users/me                # Información del usuario
PUT    /api/users/me                # Actualizar usuario
```

### <span style="color: #2563eb;">👤</span> Perfiles Extendidos <span style="color: #059669;">(v1.0)</span>
```
GET    /api/profiles/me             # Obtener perfil completo
PUT    /api/profiles/me             # Actualizar perfil
POST   /api/profiles/me/picture     # Subir foto de perfil
POST   /api/profiles/me/cover       # Subir foto de portada
GET    /api/profiles/me/preferences # Obtener preferencias de fitness
PUT    /api/profiles/me/preferences # Actualizar preferencias
GET    /api/profiles/me/health      # Información de salud
PUT    /api/profiles/me/health      # Actualizar datos de salud
GET    /api/profiles/me/settings    # Configuraciones personales
PUT    /api/profiles/me/settings    # Actualizar configuraciones
```

### <span style="color: #dc2626;">🎯</span> Sistema de Objetivos SMART <span style="color: #059669;">(v1.0)</span>
```
GET    /api/goals/                  # Listar objetivos
POST   /api/goals/                  # Crear objetivo SMART
GET    /api/goals/{goal_id}         # Obtener objetivo específico
PUT    /api/goals/{goal_id}         # Actualizar objetivo
DELETE /api/goals/{goal_id}         # Eliminar objetivo
POST   /api/goals/{goal_id}/progress # Registrar progreso
GET    /api/goals/analytics         # Análisis de objetivos
GET    /api/goals/dashboard         # Dashboard de objetivos
GET    /api/goals/milestones        # Hitos alcanzados
```

### <span style="color: #7c3aed;">⚖️</span> Seguimiento de Peso Corporal <span style="color: #059669;">(v1.0)</span>
```
GET    /api/weight/entries          # Entradas de peso
POST   /api/weight/entries          # Registrar nuevo peso
PUT    /api/weight/entries/{id}     # Actualizar entrada
DELETE /api/weight/entries/{id}     # Eliminar entrada
GET    /api/weight/analytics        # Análisis de peso detallado
GET    /api/weight/trends           # Tendencias y proyecciones
GET    /api/weight/milestones       # Hitos de pérdida de peso
POST   /api/weight/photos           # Subir foto de progreso
GET    /api/weight/summary/weekly   # Resumen semanal
```

### <span style="color: #dc2626;">🏃‍♂️</span> Workout of the Day <span style="color: #059669;">(v1.0)</span>
```
GET    /api/workouts/today          # Rutina de hoy
GET    /api/workouts/               # Todas las rutinas disponibles
GET    /api/workouts/{workout_id}   # Rutina específica
POST   /api/workouts/{workout_id}/complete # Completar rutina
GET    /api/workouts/my/completions # Mis rutinas completadas
GET    /api/workouts/my/stats       # Mis estadísticas
GET    /api/workouts/recommendations/personalized # Recomendaciones
GET    /api/workouts/weekly/schedule # Calendario semanal
```

### 💪 Sistema de Motivación Diaria
```
GET    /api/motivation/quote-of-the-day # Quote motivacional del día
GET    /api/motivation/challenge-of-the-day # Desafío del día
GET    /api/motivation/dashboard    # Dashboard de motivación completo
POST   /api/motivation/complete-challenge # Completar desafío
GET    /api/motivation/streaks      # Streaks del usuario
GET    /api/motivation/levels       # Niveles de motivación disponibles
GET    /api/motivation/rewards      # Recompensas disponibles
GET    /api/motivation/challenges/available # Desafíos disponibles
```

### 📈 Tracking de Progreso
```
GET    /api/progress/dashboard      # Dashboard completo de progreso
POST   /api/progress/goals          # Crear objetivo personalizado
GET    /api/progress/analytics      # Análisis de tendencias
POST   /api/progress/log-activity   # Registrar actividad
GET    /api/progress/goals/mine     # Mis objetivos
```

### 🔔 Sistema de Notificaciones
```
POST   /api/notifications/register-token # Registrar token de dispositivo
GET    /api/notifications/settings # Configuraciones de notificación
PUT    /api/notifications/settings # Actualizar configuraciones
POST   /api/notifications/send     # Enviar notificación
GET    /api/notifications/history  # Historial de notificaciones
```

### 🏃‍♂️ Ejercicios y Rutinas
```
GET    /api/exercises              # Listar ejercicios disponibles
POST   /api/exercises              # Crear ejercicio personalizado
GET    /api/routines               # Listar rutinas del usuario
POST   /api/routines               # Crear rutina personalizada
```

## 🎮 Sistema de Gamificación Completo

### 🏆 Puntos y Recompensas
- **10-35 puntos** por desafío completado según dificultad
- **Bonus automático** por mantener streaks consecutivos
- **8 recompensas desbloqueables** por diferentes logros y hitos
- **Sistema de multiplicadores** por consistency y logros especiales

### 📈 Niveles de Motivación Progresivos
1. 🌱 **Principiante** (0-99 puntos) - Desafíos básicos y motivación inicial
2. 🌿 **Motivado** (100-299 puntos) - Desafíos medios + quotes premium
3. 🌳 **Dedicado** (300-599 puntos) - Desafíos avanzados + estadísticas detalladas
4. 🏆 **Campeón** (600-999 puntos) - Desafíos exclusivos + insignias especiales
5. 👑 **Leyenda** (1000+ puntos) - Acceso VIP + coach virtual personalizado

### 🔥 Sistema de Streaks Inteligente
- **Tracking automático** de días consecutivos de actividad
- **Múltiples tipos**: workout, challenge, login, progress_update, weight_log
- **Recompensas especiales** por hitos importantes: 7, 30, 100, 365 días

## 📱 Ejemplos de Uso para Frontend

### JavaScript/React Native
```javascript
// Configuración base
const API_BASE_URL = 'http://localhost:8000';

// Headers con autenticación
const getAuthHeaders = (token) => ({
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
});

// 🔐 Autenticación
const login = async (email, password) => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: `username=${email}&password=${password}`
  });
  return response.json();
};

// 👤 Obtener perfil extendido
const getUserProfile = async (token) => {
  const response = await fetch(`${API_BASE_URL}/api/profiles/me`, {
    headers: getAuthHeaders(token)
  });
  return response.json();
};

// 📸 Subir foto de perfil
const uploadProfilePicture = async (token, imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);
  
  const response = await fetch(`${API_BASE_URL}/api/profiles/me/picture`, {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${token}` },
    body: formData
  });
  return response.json();
};

// 🎯 Crear objetivo SMART
const createGoal = async (token, goalData) => {
  const response = await fetch(`${API_BASE_URL}/api/goals/`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify(goalData)
  });
  return response.json();
};

// ⚖️ Registrar peso
const logWeight = async (token, weightData) => {
  const response = await fetch(`${API_BASE_URL}/api/weight/entries`, {
    method: 'POST',
    headers: getAuthHeaders(token),
    body: JSON.stringify(weightData)
  });
  return response.json();
};

// 🏃‍♂️ Obtener workout del día
const getTodayWorkout = async () => {
  const response = await fetch(`${API_BASE_URL}/api/workouts/today`);
  return response.json();
};

// 💪 Obtener quote del día
const getDailyQuote = async () => {
  const response = await fetch(`${API_BASE_URL}/api/motivation/quote-of-the-day`);
  return response.json();
};
```

### Flutter/Dart
```dart
// Configuración base
class ApiService {
  static const String baseUrl = 'http://localhost:8000';
  
  // Login
  static Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/auth/login'),
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: 'username=$email&password=$password',
    );
    return json.decode(response.body);
  }
  
  // Obtener perfil extendido
  static Future<Map<String, dynamic>> getUserProfile(String token) async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/profiles/me'),
      headers: {'Authorization': 'Bearer $token'},
    );
    return json.decode(response.body);
  }
}
```

## 💾 Base de Datos y Modelos

### Desarrollo (SQLite - Automático)
El proyecto usa **SQLite** por defecto para desarrollo local. La base de datos se crea automáticamente al iniciar el servidor.

### Producción (PostgreSQL)
Para producción, actualiza la variable `DATABASE_URL` en `.env`:
```bash
DATABASE_URL=postgresql://username:password@localhost/fitmotiv_db
```

### 📊 Datos de Ejemplo Incluidos
- ✅ **7 rutinas semanales** variadas (HIIT, Yoga, Fuerza, Cardio, Flexibilidad, Cuerpo Completo)
- ✅ **15 quotes motivacionales** en español categorizados por tema
- ✅ **10 desafíos diarios** con diferentes niveles de dificultad
- ✅ **8 recompensas** por logros y hitos específicos
- ✅ **5 niveles** de motivación progresivos con beneficios
- ✅ **Ejercicios básicos** para entrenamientos personalizados

## 🧪 Testing y Desarrollo

### Ejecutar Tests
```bash
# Test completo del sistema
python3 scripts/test_system.py

# Verificar endpoints específicos
curl -X GET "http://localhost:8000/api/motivation/quote-of-the-day"
curl -X GET "http://localhost:8000/health"
```

### Scripts de Utilidad
```bash
# Inicialización completa (recomendado)
python3 scripts/init_database.py

# Scripts individuales para desarrollo
python3 scripts/populate_exercises.py      # Solo ejercicios
python3 scripts/populate_workouts.py       # Solo rutinas
python3 scripts/populate_motivation.py     # Solo motivación
python3 scripts/populate_progress.py       # Solo progreso
```

### Comandos de Desarrollo
```bash
# Servidor con recarga automática (desarrollo)
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Servidor estable (pruebas/demo)
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Verificar dependencias
python3 -m pip list | grep fastapi
```

## 📖 Documentación de la API

### Acceso a Documentación
Una vez iniciado el servidor:
- **Swagger UI (Interactiva)**: http://localhost:8000/docs
- **ReDoc (Alternativa)**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Características de la Documentación
- ✅ **Documentación automática** generada por FastAPI
- ✅ **Ejemplos interactivos** para todos los endpoints
- ✅ **Schemas de validación** detallados
- ✅ **Códigos de respuesta** y ejemplos de error
- ✅ **Autenticación integrada** para probar endpoints protegidos

## 🚀 Deployment y Producción

### Docker
```bash
# Construir imagen
docker build -t fitmotiv-backend .

# Ejecutar contenedor
docker run -p 8000:8000 -e DATABASE_URL="your-db-url" fitmotiv-backend
```

### Docker Compose (Desarrollo)
```bash
# Levantar stack completo con PostgreSQL
docker-compose up -d

# Ver logs
docker-compose logs -f
```

### Variables de Entorno para Producción
```bash
# Base de datos
DATABASE_URL=postgresql://user:password@localhost/fitmotiv_prod

# Seguridad
SECRET_KEY=your-super-secure-secret-key-for-production
ALGORITHM=HS256

# Email (opcional)
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=noreply@yourapp.com
EMAIL_HOST_PASSWORD=your-email-password
```

## ❗ Solución de Problemas Comunes

### Error: "command not found: pip" o "command not found: python"
```bash
# Usar rutas específicas de python3
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

### Error: "Port already in use"
```bash
# Encontrar proceso usando el puerto
lsof -i :8000

# Terminar proceso específico
kill -9 <PID>

# Usar puerto alternativo
python3 -m uvicorn app.main:app --reload --port 8001
```

### Error: "Database locked" o problemas de SQLite
```bash
# Eliminar base de datos y recrear
rm test.db

# Repoblar datos
python3 scripts/init_database.py
```

### Error: "ModuleNotFoundError"
```bash
# Verificar instalación en directorio correcto
cd fitmotiv-backend
python3 -m pip install -r requirements.txt

# Verificar versión de Python
python3 --version  # Debe ser 3.9+
```

### Advertencias de Pydantic v2
```bash
# Las advertencias sobre 'orm_mode' → 'from_attributes' son normales
# No afectan el funcionamiento de la API
```

## 📊 Métricas y Estadísticas del Proyecto

### 🏗️ Arquitectura
- **60+ endpoints** distribuidos en 12 routers especializados
- **25+ modelos** de base de datos con relaciones complejas
- **80+ esquemas** Pydantic para validación estricta
- **4 sistemas principales** integrados (Auth, Motivation, Progress, Workouts)

### 📈 Funcionalidades
- **15 quotes motivacionales** categorizados y localizados
- **10 desafíos diarios** con gamificación completa
- **7 rutinas semanales** con diferentes niveles y categorías
- **5 niveles de motivación** progresivos con recompensas
- **8 logros desbloqueables** por diferentes hitos

### 🔧 Rendimiento
- **Respuesta promedio**: <100ms para endpoints básicos
- **Documentación automática**: 100% de cobertura de endpoints
- **Validación de datos**: 100% de esquemas tipados
- **Compatibilidad**: React Native, Flutter, Web, Mobile

## 🤝 Contribución al Proyecto

### Cómo Contribuir
1. **Fork** el repositorio
2. **Crear rama** para feature (`git checkout -b feature/nueva-funcionalidad`)
3. **Commit** cambios (`git commit -m 'Agregar nueva funcionalidad increíble'`)
4. **Push** a la rama (`git push origin feature/nueva-funcionalidad`)
5. **Crear Pull Request** con descripción detallada

### Estándares de Código
- **PEP 8** para estilo de Python
- **Type hints** obligatorios en funciones nuevas
- **Docstrings** para clases y métodos públicos
- **Tests** para funcionalidades críticas

### Areas de Contribución
- 🔧 **Backend Features**: nuevos endpoints y funcionalidades
- 📱 **Frontend Integration**: mejoras en compatibilidad móvil
- 🧪 **Testing**: cobertura de tests y validaciones
- 📖 **Documentación**: ejemplos y guías de uso
- 🎨 **UI/UX**: mejoras en responses y estructura de datos

## <span style="color: #dc2626;">🏆</span> Reconocimientos y Créditos

- **FastAPI Team** - Framework web excepcional
- **SQLAlchemy Team** - ORM robusto y flexible
- **Pydantic Team** - Validación de datos elegante
- **Uvicorn Team** - Servidor ASGI de alto rendimiento

## <span style="color: #2563eb;">📋</span> Changelog

### v1.0.0 (Octubre 2025) - **Primera Versión Estable** 🎉
- ✨ **Perfiles de usuario extendidos** con 40+ campos personalizables
- ✨ **Sistema de objetivos SMART** con seguimiento automático de progreso
- ✨ **Seguimiento avanzado de peso** con análisis de tendencias y proyecciones
- ✨ **Workout of the Day** con recomendaciones personalizadas y sistema de calificación
- ✨ **Dashboard inteligente** con análisis completo de progreso y estadísticas
- ✨ **Sistema de carga de archivos** para fotos de perfil, portada y progreso
- ✨ **API completamente compatible** con aplicaciones móviles modernas
- 🔧 **Autenticación JWT robusta** con refresh tokens y blacklist
- 💪 **Sistema de motivación gamificado** con quotes, desafíos y recompensas
- 🔔 **Sistema de notificaciones inteligentes** para FCM y APNS
- 📊 **Análisis y métricas avanzadas** con proyecciones estadísticas
- 🏃‍♂️ **Base de datos completa** de ejercicios y rutinas
- � **Documentación automática** con Swagger UI y ReDoc

### **Roadmap Futuro:**
- **v1.1.x** - Nuevas funcionalidades menores y mejoras
- **v1.x.x** - Correcciones de bugs y actualizaciones de seguridad
- **v2.0.x** - Funcionalidades principales adicionales (cuando sea necesario)

## <span style="color: #2563eb;">📄</span> Licencia

Este proyecto está bajo la **Licencia MIT**. Ver archivo `LICENSE` para más detalles.

## <span style="color: #059669;">📞</span> Soporte y Contacto

- **<span style="color: #2563eb;">📖</span> Documentación**: http://localhost:8000/docs
- **<span style="color: #dc2626;">🐛</span> Issues**: [GitHub Issues](https://github.com/GrullonDev/Fitmotiv-Backend/issues)
- **<span style="color: #7c3aed;">💬</span> Discusiones**: [GitHub Discussions](https://github.com/GrullonDev/Fitmotiv-Backend/discussions)
- **<span style="color: #059669;">📧</span> Email**: support@fitmotiv.app

---

## <span style="color: #2563eb;">👨‍💻</span> Desarrollador

**FitMotiv Backend v1.0** fue desarrollado por **[GrullonDev](https://github.com/GrullonDev)**

### <span style="color: #059669;">📬</span> Contacto Profesional:
- **<span style="color: #059669;">📧</span> Email**: [prosystem155@gmail.com](mailto:prosystem155@gmail.com)
- **<span style="color: #7c3aed;">💼</span> Portafolio**: [Ver proyectos y experiencia](https://jorgegrullondev.com)
- **<span style="color: #2563eb;">👨‍💻</span> GitHub**: [@GrullonDev](https://github.com/GrullonDev)
- **<span style="color: #059669;">🔗</span> LinkedIn**: [Conectar en LinkedIn](https://linkedin.com/in/grullondev)

### <span style="color: #dc2626;">🚀</span> Servicios de Desarrollo:
- **Backend APIs**: FastAPI, Django, Node.js
- **Mobile Development**: React Native, Flutter
- **Cloud & DevOps**: AWS, Docker, CI/CD
- **Database Design**: PostgreSQL, MongoDB, Redis

*¿Tienes un proyecto en mente? ¡Hablemos y hagámoslo realidad!*

---

<div align="center">
<h3><span style="color: #dc2626;">●</span> FitMotiv v1.0 - Tu compañero de fitness más inteligente y completo!</h3>

<p><em>Desarrollado con FastAPI, SQLAlchemy, mucha pasión por el fitness y dedicación al código limpio</em></p>
</div>