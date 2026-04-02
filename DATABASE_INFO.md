# Base de Datos SQLite - EchoDB

## 📋 Información General

A partir de la versión 2.3.0, EchoDB utiliza SQLite para almacenar todas las configuraciones de forma más robusta y escalable.

## 🗄️ Ubicación

```
~/.echodb/echodb.db
```

## 📊 Estructura de la Base de Datos

### Tabla: `connections`

Almacena todas las conexiones configuradas.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID único (PRIMARY KEY) |
| `name` | TEXT | Nombre de la conexión (UNIQUE) |
| `log_path` | TEXT | Ruta al archivo de log |
| `auto_scroll` | INTEGER | Auto-scroll activado (0/1) |
| `queries_only` | INTEGER | Mostrar solo queries (0/1) |
| `font_size` | INTEGER | Tamaño de fuente (8-16) |
| `filter_text` | TEXT | Filtro por defecto |
| `created_at` | TIMESTAMP | Fecha de creación |
| `updated_at` | TIMESTAMP | Última actualización |

### Tabla: `app_settings`

Almacena configuraciones globales de la aplicación.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `key` | TEXT | Clave del setting (PRIMARY KEY) |
| `value` | TEXT | Valor del setting |
| `updated_at` | TIMESTAMP | Última actualización |

### Tabla: `connection_history`

Historial de acciones sobre conexiones (para futuras funcionalidades).

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | INTEGER | ID único (PRIMARY KEY) |
| `connection_id` | INTEGER | ID de la conexión (FOREIGN KEY) |
| `action` | TEXT | Acción realizada |
| `timestamp` | TIMESTAMP | Fecha/hora de la acción |

## 🔄 Migración desde JSON

### Proceso Automático

Al iniciar EchoDB por primera vez después de actualizar:

1. **Detecta** si existe `~/.echodb/echodb_config.json`
2. **Lee** todas las conexiones del archivo JSON
3. **Migra** cada conexión a la base de datos SQLite
4. **Crea backup** del JSON como `echodb_config.json.backup`
5. **Elimina** el archivo JSON original

### Ejemplo de Migración

**Antes (JSON):**
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
    }
  ]
}
```

**Después (SQLite):**
```sql
INSERT INTO connections (name, log_path, auto_scroll, queries_only, font_size, filter_text)
VALUES ('Production', '/var/log/postgresql/postgresql.log', 1, 0, 10, '');
```

## 💡 Ventajas de SQLite

### 1. **Robustez**
- Transacciones ACID
- Resistente a corrupción de datos
- Recuperación automática de errores

### 2. **Performance**
- Búsquedas más rápidas
- Actualizaciones atómicas
- Índices automáticos

### 3. **Escalabilidad**
- Soporta miles de conexiones
- Queries eficientes
- Historial de cambios

### 4. **Integridad**
- Constraints de unicidad
- Foreign keys
- Validación de datos

## 🔧 Operaciones Comunes

### Ver todas las conexiones

```sql
SELECT * FROM connections ORDER BY updated_at DESC;
```

### Buscar conexión por nombre

```sql
SELECT * FROM connections WHERE name = 'Production';
```

### Actualizar configuración

```sql
UPDATE connections 
SET log_path = '/new/path/postgresql.log',
    updated_at = CURRENT_TIMESTAMP
WHERE name = 'Production';
```

### Eliminar conexión

```sql
DELETE FROM connections WHERE name = 'Old Connection';
```

## 🛠️ Herramientas para Inspeccionar la BD

### 1. SQLite CLI

```bash
sqlite3 ~/.echodb/echodb.db

# Ver tablas
.tables

# Ver estructura de tabla
.schema connections

# Query
SELECT * FROM connections;

# Salir
.quit
```

### 2. DB Browser for SQLite

Aplicación gráfica para visualizar y editar bases de datos SQLite:
- Descarga: https://sqlitebrowser.org/
- Abre: `~/.echodb/echodb.db`

### 3. Python Script

```python
import sqlite3

conn = sqlite3.connect('~/.echodb/echodb.db')
cursor = conn.cursor()

cursor.execute("SELECT name, log_path FROM connections")
for row in cursor.fetchall():
    print(f"Connection: {row[0]}, Path: {row[1]}")

conn.close()
```

## 📝 Backup y Restauración

### Crear Backup

```bash
# Backup manual
cp ~/.echodb/echodb.db ~/.echodb/echodb.db.backup

# Con timestamp
cp ~/.echodb/echodb.db ~/.echodb/echodb.db.$(date +%Y%m%d_%H%M%S)
```

### Restaurar Backup

```bash
cp ~/.echodb/echodb.db.backup ~/.echodb/echodb.db
```

### Exportar a JSON

```python
import sqlite3
import json

conn = sqlite3.connect('~/.echodb/echodb.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM connections")
connections = [dict(row) for row in cursor.fetchall()]

with open('connections_export.json', 'w') as f:
    json.dump(connections, f, indent=2)

conn.close()
```

## ⚠️ Troubleshooting

### Base de datos corrupta

```bash
# Verificar integridad
sqlite3 ~/.echodb/echodb.db "PRAGMA integrity_check;"

# Si está corrupta, restaurar desde backup
cp ~/.echodb/echodb.db.backup ~/.echodb/echodb.db
```

### Resetear base de datos

```bash
# CUIDADO: Esto elimina todas las configuraciones
rm ~/.echodb/echodb.db

# EchoDB creará una nueva BD al iniciar
```

### Migración manual desde JSON

Si la migración automática falla:

```python
from src.database import EchoDatabase
from pathlib import Path
import json

db = EchoDatabase()

json_file = Path.home() / ".echodb" / "echodb_config.json"
with open(json_file) as f:
    config = json.load(f)

for tab in config['tabs']:
    db.save_connection(tab)

print("Migration completed!")
```

## 🔐 Seguridad

- La base de datos se almacena en el directorio home del usuario
- Permisos: Solo el usuario puede leer/escribir
- No contiene contraseñas (solo rutas de archivos)
- Backup automático al migrar desde JSON

## 📈 Futuras Mejoras

- [ ] Historial de cambios en conexiones
- [ ] Estadísticas de uso por conexión
- [ ] Exportar/importar configuraciones
- [ ] Sincronización entre dispositivos
- [ ] Perfiles de configuración
