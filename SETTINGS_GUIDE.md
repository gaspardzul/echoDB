# Guía de Configuración - EchoDB

## 📋 Tabla de Contenidos

1. [Configuración de Tabs](#configuración-de-tabs)
2. [Guardado y Carga](#guardado-y-carga)
3. [Opciones Disponibles](#opciones-disponibles)
4. [Casos de Uso](#casos-de-uso)

---

## ⚙️ Configuración de Tabs

### Acceder a la Configuración

Cada tab tiene su propio botón **⚙️ Settings** que abre el diálogo de configuración.

**Formas de acceder:**
1. Click en el botón **⚙️ Settings** dentro del tab
2. El diálogo muestra la configuración actual del tab

### Opciones Disponibles

#### 1. **Tab Name** (Nombre del Tab)
- Renombra el tab con un nombre descriptivo
- Ejemplos: "Production", "Development", "Local DB", "Customer DB"
- El cambio se refleja inmediatamente en la pestaña

#### 2. **Log Path** (Ruta del Log)
- Especifica la ruta completa al archivo de log de PostgreSQL
- Usa el botón **Browse...** para seleccionar el archivo
- Ejemplo: `/Users/user/Library/Application Support/Postgres/var-16/postgresql.log`

#### 3. **Display Options** (Opciones de Visualización)

**Auto-scroll to bottom:**
- ✅ Activado: Scroll automático a las últimas entradas
- ⬜ Desactivado: Scroll manual (útil para analizar logs históricos)

**Show queries only:**
- ✅ Activado: Muestra solo queries SQL (oculta LOG, INFO, etc.)
- ⬜ Desactivado: Muestra todos los logs

**Font Size:**
- Rango: 8pt - 16pt
- Por defecto: 10pt
- Útil para pantallas grandes o presentaciones

#### 4. **Default Filter** (Filtro por Defecto)
- Establece un filtro que se aplica automáticamente
- Ejemplos:
  - `users` - Solo logs relacionados con tabla users
  - `SELECT` - Solo queries SELECT
  - `ERROR` - Solo errores

---

## 💾 Guardado y Carga

### Guardado Automático

La configuración se guarda automáticamente cuando:
- Cierras la aplicación
- Todos los tabs y sus configuraciones se guardan

### Guardado Manual

**Método 1: Menú**
- File > Save Tabs Configuration

**Método 2: Atajo de teclado**
- `Ctrl+S` (macOS: Cmd+S)

**Confirmación:**
- Mensaje mostrando cuántos tabs se guardaron
- Ubicación del archivo de configuración

### Carga Automática

Al iniciar EchoDB:
1. Busca el archivo de configuración en `~/.echodb/echodb_config.json`
2. Si existe, carga todos los tabs guardados
3. Si no existe, crea un tab por defecto

### Ubicación del Archivo

```
~/.echodb/echodb_config.json
```

**Ejemplo de contenido:**
```json
{
  "version": "2.0",
  "tabs": [
    {
      "name": "Production",
      "log_path": "/var/log/postgresql/postgresql.log",
      "auto_scroll": true,
      "queries_only": false,
      "font_size": 10,
      "filter_text": ""
    },
    {
      "name": "Development",
      "log_path": "/Users/dev/postgres/logs/dev.log",
      "auto_scroll": true,
      "queries_only": true,
      "font_size": 12,
      "filter_text": "users"
    }
  ]
}
```

---

## 🎯 Casos de Uso

### Caso 1: Monitorear Producción y Desarrollo

**Setup:**
1. Tab 1: "Production"
   - Log Path: `/var/log/postgresql/production.log`
   - Queries Only: ❌ (ver todos los logs)
   - Filter: `ERROR` (solo errores)

2. Tab 2: "Development"
   - Log Path: `/Users/dev/postgres/dev.log`
   - Queries Only: ✅ (solo queries)
   - Auto-scroll: ✅

**Beneficio:** Monitorea errores en producción mientras desarrollas

### Caso 2: Análisis de Tabla Específica

**Setup:**
1. Tab: "Users Table Analysis"
   - Queries Only: ✅
   - Default Filter: `users`
   - Font Size: 12pt (mejor legibilidad)
   - Auto-scroll: ❌ (para analizar con calma)

**Beneficio:** Enfoque total en queries de una tabla

### Caso 3: Debugging de Performance

**Setup:**
1. Tab: "Slow Queries"
   - Default Filter: `duration`
   - Queries Only: ✅
   - Font Size: 10pt

**Beneficio:** Identifica queries lentas rápidamente

### Caso 4: Múltiples Clientes

**Setup:**
1. Tab: "Client A - DB1"
2. Tab: "Client A - DB2"
3. Tab: "Client B - DB1"

**Beneficio:** Monitorea múltiples bases de datos de diferentes clientes

---

## 💡 Tips y Mejores Prácticas

### 1. Nombres Descriptivos
Usa nombres que identifiquen claramente el propósito:
- ✅ "Production - Main DB"
- ✅ "Dev - Feature Branch"
- ❌ "Connection 1"

### 2. Filtros por Defecto
Establece filtros para casos de uso específicos:
- `ERROR` - Para monitoreo de errores
- `INSERT` - Para auditoría de inserts
- `table_name` - Para análisis de tabla específica

### 3. Tamaño de Fuente
- **8-9pt**: Para ver más contenido en pantalla
- **10-11pt**: Uso normal
- **12-16pt**: Presentaciones o pantallas grandes

### 4. Auto-scroll
- **Activado**: Monitoreo en tiempo real
- **Desactivado**: Análisis de logs históricos

### 5. Queries Only
- **Activado**: Cuando solo te interesan las queries SQL
- **Desactivado**: Cuando necesitas ver errores, warnings, etc.

---

## 🔧 Troubleshooting

### La configuración no se guarda
1. Verifica permisos en `~/.echodb/`
2. Guarda manualmente con `Ctrl+S`
3. Revisa que el archivo `echodb_config.json` exista

### Los tabs no se cargan al iniciar
1. Verifica que el archivo de configuración exista
2. Revisa el formato JSON (debe ser válido)
3. Si hay error, se creará un tab por defecto

### El cambio de nombre no se refleja
1. Asegúrate de hacer click en "Save Settings"
2. El nombre debe actualizarse inmediatamente
3. Si no, cierra y reabre el diálogo de settings

---

## 📝 Notas Importantes

- La configuración es **por usuario** (en tu directorio home)
- Cada tab es **completamente independiente**
- Los cambios se aplican **inmediatamente** al guardar
- El archivo de configuración es **JSON legible**
- Puedes **editar manualmente** el archivo si lo deseas
