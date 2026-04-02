# Changelog - EchoDB

## Version 2.5.0 (2026-03-31)

### 🎉 Major Features

#### Database Monitor 🔍
- **Monitor en tiempo real** de PostgreSQL
- **3 tabs de información**:
  - Overview: Métricas generales (conexiones, TPS, cache, locks)
  - Active Queries: Queries ejecutándose en tiempo real
  - Database Stats: Estadísticas por base de datos
- **Auto-refresh** cada 5 segundos (configurable)
- **Kill queries**: Termina queries problemáticas desde la UI
- **Visualización moderna**: Barras de progreso, métricas grandes
- **Interfaz oscura**: Estilo terminal profesional

### ✨ UI/UX Improvements

#### Chat de IA Mejorado
- **Estilo terminal/consola**: Más limpio y legible
- **Prefijos tipo shell**: `> USER`, `$ ASSISTANT`, `# SYSTEM`
- **QLabel en lugar de QTextEdit**: Mejor renderizado de texto
- **Markdown support**: Respuestas formateadas
- **Botón Copy**: Copia respuestas de IA al portapapeles

### 🔧 Technical Changes

- Nuevo archivo: `src/db_monitor_dialog.py` - Monitor de base de datos
- Queries SQL optimizadas para métricas de PostgreSQL
- QTimer para auto-refresh de datos
- Mejoras en ai_chat_panel.py para mejor visualización

### 📚 Features Added

- Monitoreo de conexiones activas
- TPS (Transactions Per Second)
- Cache Hit Ratio
- Active queries con detalles
- Database size tracking
- Lock monitoring
- Query termination capability

---

## Version 2.4.0 (2026-03-31)

### 🎉 Major Features

#### Análisis de Logs con IA 🤖
- **Integración con 3 proveedores de IA**:
  - OpenAI (GPT-4o, GPT-4o-mini, GPT-3.5-turbo)
  - Claude/Anthropic (Claude 3.5 Sonnet, Opus, Haiku)
  - DeepSeek (DeepSeek Chat, DeepSeek Coder)
- **Chat interactivo**: Pregunta en lenguaje natural sobre tus logs
- **Análisis inteligente**: Identifica errores, patrones, queries lentas
- **Configuración segura**: API keys almacenadas localmente en SQLite
- **Botón en cada tab**: Acceso rápido al chat de IA

#### Desactivación Rápida de Logging 🔴
- **Botón "Disable DB Logging"** en cada tab
- **Proceso simplificado**: Solo pide credenciales y desactiva
- **Previene crecimiento de logs**: Ideal cuando terminas de debuggear
- **Feedback inmediato**: Confirma cuando el logging está desactivado

### ✨ UI/UX Improvements

#### Diseño Más Fresco y Moderno
- **Colores Tailwind CSS**: Paleta moderna y profesional
- **Botones redondeados**: Border-radius de 6-8px
- **Efectos hover**: Feedback visual al pasar el mouse
- **Mejor espaciado**: Padding mejorado en todos los botones
- **Colores vibrantes**:
  - Verde (#10B981) para Start
  - Rojo (#EF4444) para Stop
  - Naranja (#F59E0B) para Clear
  - Rosa (#EC4899) para Disable Logging
  - Morado (#8B5CF6) para AI Chat
  - Azul (#3B82F6) para Auto-Setup

### 🔧 Technical Changes

- Nuevo archivo: `src/ai_config_dialog.py` - Configuración de IA
- Nuevo archivo: `src/ai_chat_panel.py` - Panel de chat con IA
- Agregado `requests==2.31.0` a requirements.txt
- Método `quick_disable_logging()` en DatabaseTab
- Método `open_ai_chat()` en DatabaseTab
- Menú "AI" en la barra de menú principal

### 📚 Dependencies

- Agregado: `requests` para llamadas a APIs de IA

---

## Version 2.3.0 (2026-03-31)

### 🎉 New Features

#### Base de Datos SQLite
- **Migración de JSON a SQLite**: Configuraciones ahora se almacenan en base de datos SQLite
- **Mejor persistencia**: Más robusta y escalable que JSON
- **Migración automática**: Convierte automáticamente configuraciones JSON existentes
- **Backup automático**: Crea backup del archivo JSON al migrar

#### Pantalla de Bienvenida
- **Welcome Screen**: Interfaz amigable cuando no hay conexiones
- **Guía visual**: Botones grandes y claros para agregar primera conexión
- **Dos opciones**:
  - 🔧 Auto-Setup (Recomendado)
  - ➕ Agregar Conexión Manual
- **Tips integrados**: Información útil para nuevos usuarios

### ✨ Improvements

- Mejor experiencia de usuario para primera vez
- No más pantalla vacía al iniciar sin configuraciones
- Transición suave entre welcome screen y tabs
- Al cerrar último tab, vuelve a welcome screen (no cierra la app)

### 🔧 Technical Changes

- Nuevo archivo: `src/database.py` - Gestión de SQLite
- Nuevo archivo: `src/welcome_widget.py` - Pantalla de bienvenida
- `ConfigManager` ahora usa SQLite internamente
- `MainWindow` usa `QStackedWidget` para alternar entre welcome y tabs

---

## Version 2.2.0 (2026-03-31)

### 🎉 New Features

#### Gestión de Logging de PostgreSQL
- **Nuevo diálogo**: Database > Manage PostgreSQL Logging
- **Activar logging**: Configura PostgreSQL para logging completo
- **Desactivar logging**: Desactiva el logging de queries (mejora performance)
- **Reset a defaults**: Restaura configuración por defecto
- **Verificación en tiempo real**: Muestra la configuración actual antes de aplicar cambios

### ✨ Improvements

- Mejor control sobre el overhead de logging en producción
- Interfaz intuitiva con opciones claramente explicadas
- Validación de permisos de superusuario
- Mensajes detallados de los cambios aplicados

### 🔧 Technical Changes

- Nuevos métodos en `db_connector.py`:
  - `disable_logging()`: Desactiva logging
  - `reset_logging_to_defaults()`: Restaura defaults
- Nuevo archivo: `src/logging_manager_dialog.py`

---

## Version 2.1.0 (2026-03-31)

### 🎉 New Features

#### Configuración Editable por Tab
- **Botón ⚙️ Settings** en cada tab para editar configuración
- **Diálogo de configuración** con opciones completas:
  - Renombrar tab
  - Cambiar ruta de log
  - Ajustar opciones de visualización
  - Configurar tamaño de fuente (8-16pt)
  - Establecer filtro por defecto

#### Persistencia de Configuración
- **Guardado automático** al cerrar la aplicación
- **Guardado manual** con Ctrl+S
- **Carga automática** al iniciar la aplicación
- **Archivo de configuración**: `~/.echodb/echodb_config.json`
- Restaura todos los tabs con sus configuraciones

### ✨ Improvements

- Cada tab mantiene su configuración independiente
- Los cambios de nombre se reflejan inmediatamente en el tab
- Configuración persistente entre sesiones
- Mejor UX con tooltips y mensajes informativos

---

## Version 2.0.0 (2026-03-31)

### 🎉 Major Features

#### Sistema de Tabs para Múltiples Conexiones
- **Múltiples bases de datos simultáneamente**: Ahora puedes monitorear varias BDs al mismo tiempo
- **Tabs independientes**: Cada tab tiene sus propios filtros, configuración y estado de monitoreo
- **Navegación con teclado**: Ctrl+Tab y Ctrl+Shift+Tab para cambiar entre tabs
- **Gestión de tabs**: Cerrar tabs individuales con Ctrl+W o click en la X

#### Mejoras en la UI
- **Fondo oscuro en Status**: Área de status del diálogo de conexión ahora tiene fondo oscuro (#2B2B2B) para mejor legibilidad
- **Nombre de conexión**: Campo para nombrar cada conexión (ej: "Production", "Development")
- **Toolbar mejorado**: Botones "➕ New Connection" y "🔧 Auto-Setup" en la parte superior
- **Tabs con estilo**: Diseño moderno con colores que indican el tab activo

### ✨ New Features

- **Campo "Connection Name"** en el diálogo de auto-setup
- **Botón "➕ New Connection"** para agregar tabs rápidamente
- **Menú File** con atajos de teclado:
  - Ctrl+T: Nueva conexión
  - Ctrl+O: Abrir log en nuevo tab
  - Ctrl+W: Cerrar tab actual
  - Ctrl+Q: Salir
- **Menú View** para navegación entre tabs
- **Confirmación al cerrar**: Pregunta antes de cerrar tabs con monitoreo activo

### 🔧 Improvements

- Cada tab es completamente independiente
- Mejor organización del código con `DatabaseTab` y `MainWindow`
- Status bar global que muestra información de la aplicación
- Mejor manejo de recursos al cerrar tabs

### 🐛 Bug Fixes

- Fondo blanco en área de Status ahora es oscuro y legible
- Mejor manejo de cierre de aplicación con múltiples tabs activos

---

## Version 1.0.0 (2026-03-31)

### Initial Release

- Auto-configuración de PostgreSQL
- Monitoreo de logs en tiempo real
- Syntax highlighting para SQL
- Filtros avanzados
- Parsing de parámetros
- Interfaz moderna con PyQt6
