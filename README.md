# EchoDB - PostgreSQL Real-time Logger

**EchoDB** es una aplicación desktop desarrollada en Python con PyQt6 que permite monitorear logs de PostgreSQL en tiempo real sin necesidad de configuraciones complejas.

## 📋 Requisitos

- **Python 3.9+**
- **PostgreSQL** instalado y corriendo
- **macOS** 10.14+ (Mojave o superior)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd EchoDB
```

### 2. Instalar dependencias

```bash
./install.sh
```

O manualmente:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Ejecutar la aplicación

```bash
./run.sh
```

O manualmente:

```bash
source venv/bin/activate
python main.py
```

## ⚙️ Configuración Rápida

1. Abre EchoDB
2. Click en **"🔧 Auto-Setup"**
3. Ingresa las credenciales de PostgreSQL:
   - Host: `localhost`
   - Port: `5432`
   - Database: `postgres`
   - User: tu usuario
   - Password: tu contraseña
4. Marca **"Configure logging parameters"**
5. Click **"Connect & Configure"**
6. Click **"▶ Iniciar"** para comenzar a monitorear

## 🎯 Características

- **🔧 Auto-Setup**: Conecta a PostgreSQL y configura automáticamente todos los parámetros de logging
- **⚡ Zero Configuration**: No necesitas editar `postgresql.conf` manualmente
- **🔄 Gestión de Logging**: Activa, desactiva o restaura la configuración de logging de PostgreSQL desde la app
- **🔴 Desactivación Rápida**: Botón en cada tab para desactivar logging instantáneamente
- **🤖 Análisis con IA**: Pregunta a OpenAI, Claude o DeepSeek sobre tus logs
- **� Database Monitor**: Monitorea en tiempo real conexiones, performance, queries activas y estadísticas
- **� Múltiples Conexiones**: Sistema de tabs para monitorear varias bases de datos simultáneamente
- **⚙️ Configuración por Tab**: Edita nombre, ruta, filtros y opciones de visualización de cada tab
- **💾 Persistencia con SQLite**: Base de datos SQLite para almacenar configuraciones de forma robusta
- **👋 Pantalla de Bienvenida**: Interfaz intuitiva cuando no hay conexiones configuradas
- **Monitoreo en Tiempo Real**: Lee logs de PostgreSQL usando técnica tail-f sin bloquear la UI
- **Syntax Highlighting**: Resaltado de sintaxis SQL con colores para mejor legibilidad
- **Filtros Avanzados**: Filtra por tabla, palabra clave o tipo de consulta (independiente por tab)
- **Parsing Inteligente**: Detecta y asocia parámetros (`$1`, `$2`, etc.) con sus queries
- **Interfaz Moderna**: UI limpia y oscura optimizada para desarrolladores
- **Auto-scroll**: Desplazamiento automático a las últimas entradas
- **Multi-threading**: Lectura no bloqueante usando QThread

## 📋 Requisitos

- Python 3.8+
- macOS (probado en MacBook Pro)
- PostgreSQL 16 (vía Postgres.app)

## 🚀 Instalación

1. Clona o descarga el proyecto:
```bash
cd /Users/gaspardzul/Documents/proyectos\ labs/EchoDB
```

2. Crea un entorno virtual (recomendado):
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## 🎮 Uso

### Opción 1: Auto-Setup (Recomendado) 🚀

1. Ejecuta la aplicación:
```bash
python main.py
```

2. Haz clic en el botón **"🔧 Auto-Setup"** (o menú Database > Auto-Setup PostgreSQL Logging)

3. Ingresa las credenciales de tu base de datos:
   - **Host**: localhost (por defecto)
   - **Port**: 5432
   - **Database**: postgres
   - **User**: postgres (debe tener permisos de superusuario)
   - **Password**: tu contraseña

4. Marca las opciones deseadas:
   - ✅ **Configure logging parameters**: Configura automáticamente `log_statement`, `log_min_duration_statement`, etc.
   - ⬜ **Enable pg_stat_statements**: (Opcional) Habilita la extensión para estadísticas de queries

5. Haz clic en **"Connect & Configure"**

6. ¡Listo! La aplicación configurará PostgreSQL automáticamente y detectará la ruta del log

7. Haz clic en **"▶ Start Monitoring"** para comenzar a ver los logs en tiempo real

### Opción 2: Manual

1. Ejecuta la aplicación:
```bash
python main.py
```

2. La aplicación cargará automáticamente la ruta por defecto:
```
/Users/gaspardzul/Library/Application Support/Postgres/var-16/postgresql.log
```

3. Haz clic en **"▶ Start Monitoring"** para comenzar a ver los logs en tiempo real

### Múltiples Conexiones (Tabs)

**Agregar nueva conexión:**
- Click en **"➕ New Connection"** en la barra superior
- O usa el menú: File > New Connection Tab (Ctrl+T)
- O usa **"🔧 Auto-Setup"** para configurar automáticamente

**Navegar entre tabs:**
- Click en el tab deseado
- Ctrl+Tab: Siguiente tab
- Ctrl+Shift+Tab: Tab anterior

**Cerrar tab:**
- Click en la X del tab
- O usa Ctrl+W

### Filtros y Opciones

Cada tab tiene sus propios filtros independientes:
- **Filter**: Busca por nombre de tabla o palabra clave (ej: `timerecord`, `SELECT`)
- **Queries Only**: Muestra solo las queries SQL, omitiendo otros logs
- **Auto-scroll**: Mantiene el scroll al final para ver las últimas entradas

## 🎨 Características de la Interfaz

### Syntax Highlighting
- **Keywords SQL**: Azul (`SELECT`, `FROM`, `WHERE`, etc.)
- **Strings**: Naranja (`'valor'`)
- **Números**: Verde
- **Parámetros**: Cyan (`$1`, `$2`)
- **Timestamps**: Gris
- **LOG/DETAIL**: Verde agua
- **ERROR**: Rojo

### Controles (por Tab)
- **▶ Start/Stop**: Inicia o detiene el monitoreo de ese tab
- **🗑 Clear**: Limpia la pantalla de logs de ese tab
- **🔴 Disable DB Logging**: Desactiva rápidamente el logging de PostgreSQL
- **🤖 AI Chat**: Abre chat con IA para analizar los logs
- **⚙️ Settings**: Abre el diálogo de configuración del tab

### Controles Globales
- **➕ New Connection**: Agrega un nuevo tab de conexión
- **🔧 Auto-Setup**: Configura automáticamente PostgreSQL y crea un nuevo tab

### Configuración de Tabs

Cada tab puede ser configurado individualmente haciendo click en **⚙️ Settings**:

**Opciones disponibles:**
- **Tab Name**: Renombrar el tab
- **Log Path**: Cambiar la ruta del archivo de log
- **Auto-scroll**: Activar/desactivar scroll automático
- **Show queries only**: Mostrar solo queries SQL
- **Font Size**: Ajustar tamaño de fuente (8-16pt)
- **Default Filter**: Establecer un filtro por defecto

**Guardado de configuración:**
- **Automático**: Al cerrar la aplicación y al modificar tabs
- **Manual**: File > Save Tabs Configuration (Ctrl+S)
- **Base de datos**: `~/.echodb/echodb.db` (SQLite)
- **Migración automática**: Convierte configuraciones JSON antiguas a SQLite

### Gestión de Logging de PostgreSQL

**Acceso:** Database > Manage PostgreSQL Logging

Permite gestionar la configuración de logging directamente desde EchoDB:

**Opciones disponibles:**
- **✅ Enable Full Logging**: Activa logging completo de todas las queries
- **❌ Disable Logging**: Desactiva el logging (útil para producción o reducir overhead)
- **🔄 Reset to Defaults**: Restaura la configuración por defecto de PostgreSQL

**Casos de uso:**
- Activar logging solo cuando necesites debuggear
- Desactivar logging en producción para mejorar performance
- Restaurar configuración después de pruebas

### Análisis de Logs con IA 🤖

**Acceso:** Botón "🤖 AI Chat" en cada tab o menú AI > Configure AI Providers

**Proveedores soportados:**
- **OpenAI** (GPT-4o, GPT-4o-mini, GPT-3.5-turbo)
- **Claude** (Claude 3.5 Sonnet, Opus, Haiku)
- **DeepSeek** (DeepSeek Chat, DeepSeek Coder)

**Funcionalidades:**
- Pregunta en lenguaje natural sobre tus logs
- Identifica errores y patrones
- Encuentra queries lentas
- Obtiene resúmenes y análisis
- Sugerencias de optimización

**Configuración:**
1. AI > Configure AI Providers
2. Selecciona tu proveedor preferido
3. Ingresa tu API key
4. Selecciona el modelo
5. ¡Listo! Usa el botón "🤖 AI Chat" en cualquier tab

### Database Monitor 🔍

**Acceso:** Database > 🔍 Database Monitor

**3 Tabs de Monitoreo:**

**📊 Overview:**
- Conexiones activas vs máximo permitido
- TPS (Transacciones por segundo)
- Cache Hit Ratio (eficiencia de caché)
- Queries activas
- Locks en espera
- Tamaño total de bases de datos

**⚡ Active Queries:**
- Lista en tiempo real de queries ejecutándose
- PID, usuario, base de datos, estado
- Duración de cada query
- Opción para terminar queries (kill)

**📈 Database Stats:**
- Tamaño de cada base de datos
- Número de tablas
- Conexiones por base de datos

**Funcionalidades:**
- Auto-refresh cada 5 segundos (activable/desactivable)
- Refresh manual con botón
- Interfaz estilo terminal oscuro
- Barras de progreso visuales
- Métricas en tiempo real

## 📁 Estructura del Proyecto

```
EchoDB/
├── main.py                      # Punto de entrada de la aplicación
├── requirements.txt             # Dependencias Python
├── config.py                    # Configuración de la aplicación
├── install.sh                   # Script de instalación
├── run.sh                       # Script para ejecutar la app
├── README.md                    # Este archivo
├── QUICKSTART.md               # Guía rápida de inicio
├── EXAMPLES.md                 # Ejemplos de uso
├── context.md                   # Contexto del proyecto
└── src/
    ├── __init__.py
    ├── main_window_tabs.py     # Ventana principal con sistema de tabs
    ├── database_tab.py         # Widget de tab individual para cada BD
    ├── connection_dialog.py    # Diálogo de conexión a PostgreSQL
    ├── db_connector.py         # Conector y configurador de PostgreSQL
    ├── log_reader.py           # Lector de logs en tiempo real (QThread)
    ├── log_parser.py           # Parser de logs PostgreSQL
    └── syntax_highlighter.py   # Resaltado de sintaxis SQL
```

## 🔧 Configuración de PostgreSQL

### Auto-Configuración (Recomendado)

EchoDB puede configurar automáticamente PostgreSQL por ti. Solo necesitas:

1. Credenciales de un usuario con permisos de superusuario
2. Hacer clic en el botón **"🔧 Auto-Setup"**

La aplicación configurará automáticamente:
- `log_min_duration_statement = 0` (captura todas las queries)
- `log_statement = 'all'` (registra todas las sentencias)
- `log_duration = 'on'` (registra duración de queries)
- `log_line_prefix = '%t [%p] '` (formato de timestamp)

### Configuración Manual (Alternativa)

Si prefieres configurar manualmente, edita `postgresql.conf`:

```conf
log_min_duration_statement = 0
log_statement = 'all'
log_duration = on
log_line_prefix = '%t [%p] '
```

Luego reinicia PostgreSQL:
```bash
pg_ctl reload
```

## 💡 Ejemplo de Log Procesado

```
2026-03-31 13:48:04.123 CST [1234] LOG:  execute <unnamed>: SELECT timerecord.id ... WHERE timerecord.node_id = $1 AND timerecord.client_id = $2 ORDER BY timerecord.created_at DESC LIMIT $3 OFFSET $4
    DETAIL:  parameters: $1 = 'NODO_01', $2 = 'CLIENTE_ABC', $3 = '50', $4 = '0'
```

## 🛠️ Desarrollo

### Arquitectura

- **LogReader**: Thread separado que lee el archivo de log usando técnica tail-f
- **LogParser**: Parsea las líneas del log y extrae timestamp, tipo y mensaje
- **SQLSyntaxHighlighter**: Aplica resaltado de sintaxis usando QSyntaxHighlighter
- **MainWindow**: Interfaz gráfica principal con PyQt6

### Extensiones Futuras

- [x] Auto-configuración de PostgreSQL
- [x] Conexión directa a base de datos
- [ ] Exportar logs filtrados a archivo
- [ ] Estadísticas de queries (más lentas, más frecuentes) usando pg_stat_statements
- [ ] Soporte para múltiples archivos de log simultáneos
- [ ] Notificaciones para errores críticos
- [ ] Gráficas de rendimiento en tiempo real
- [ ] Modo "Query Analyzer" con métricas de rendimiento

## 📝 Notas

- La aplicación usa `pathlib` para manejar rutas con espacios en macOS
- El threading asegura que la UI nunca se congele durante la lectura
- Los parámetros se asocian automáticamente con su query correspondiente

## 🤝 Contribuciones

Este proyecto está diseñado para uso interno del equipo de desarrollo. Si encuentras bugs o tienes sugerencias, comunícalas al equipo.

## 📄 Licencia

Uso interno - Todos los derechos reservados
