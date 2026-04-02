# Gestión de Logging de PostgreSQL - EchoDB

## 📋 Introducción

EchoDB incluye una herramienta integrada para gestionar la configuración de logging de PostgreSQL sin necesidad de editar archivos de configuración manualmente.

## 🎯 ¿Por qué gestionar el logging?

### Ventajas de Activar Logging
- ✅ **Debugging**: Ver todas las queries que se ejecutan
- ✅ **Auditoría**: Registrar todas las operaciones en la BD
- ✅ **Análisis de performance**: Identificar queries lentas
- ✅ **Desarrollo**: Entender el comportamiento de tu aplicación

### Ventajas de Desactivar Logging
- ✅ **Performance**: Reduce overhead en producción
- ✅ **Espacio en disco**: No genera archivos de log grandes
- ✅ **Privacidad**: No registra datos sensibles en logs
- ✅ **Producción**: Configuración típica para ambientes productivos

## 🚀 Cómo Usar

### Acceder al Gestor de Logging

**Método 1: Menú**
1. Database > Manage PostgreSQL Logging

**Método 2: Durante Auto-Setup**
- El Auto-Setup también permite activar logging

### Opciones Disponibles

#### 1. ✅ Enable Full Logging

**Qué hace:**
```sql
ALTER SYSTEM SET log_min_duration_statement = 0;
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_duration = 'on';
ALTER SYSTEM SET log_line_prefix = '%t [%p] ';
SELECT pg_reload_conf();
```

**Resultado:**
- Registra TODAS las queries ejecutadas
- Incluye parámetros de las queries preparadas
- Registra duración de cada query
- Formato de timestamp legible

**Cuándo usar:**
- Durante desarrollo
- Para debugging de problemas
- Para análisis de performance
- Para auditoría completa

#### 2. ❌ Disable Logging

**Qué hace:**
```sql
ALTER SYSTEM SET log_min_duration_statement = -1;
ALTER SYSTEM SET log_statement = 'none';
ALTER SYSTEM SET log_duration = 'off';
SELECT pg_reload_conf();
```

**Resultado:**
- NO registra queries en los logs
- Reduce overhead de I/O
- Mejora performance ligeramente
- Ahorra espacio en disco

**Cuándo usar:**
- En producción (si no necesitas logs)
- Cuando el performance es crítico
- Para reducir uso de disco
- Después de terminar debugging

#### 3. 🔄 Reset to Defaults

**Qué hace:**
```sql
ALTER SYSTEM RESET log_min_duration_statement;
ALTER SYSTEM RESET log_statement;
ALTER SYSTEM RESET log_duration;
ALTER SYSTEM RESET log_line_prefix;
SELECT pg_reload_conf();
```

**Resultado:**
- Restaura valores por defecto de PostgreSQL
- Configuración balanceada
- Útil si no estás seguro qué configuración usar

**Cuándo usar:**
- Después de pruebas o debugging
- Para volver a configuración estándar
- Si algo salió mal con la configuración

## 📝 Paso a Paso

### Ejemplo 1: Activar Logging para Debugging

1. **Abrir el gestor:**
   - Database > Manage PostgreSQL Logging

2. **Conectar a la BD:**
   - Host: localhost
   - Port: 5432
   - Database: postgres
   - User: postgres (debe ser superusuario)
   - Password: [tu_password]

3. **Verificar configuración actual:**
   - Click en "🔍 Check Current Settings"
   - Verás la configuración actual en "Current Settings"

4. **Activar logging:**
   - Selecciona: ✅ **Enable Full Logging**
   - Click en "✅ Apply Changes"

5. **Resultado:**
   ```
   ✅ Connected to PostgreSQL
   ⚙️  Enabling full logging...
   Logging configured successfully. Changes:
     • log_min_duration_statement = 0
     • log_statement = 'all'
     • log_duration = 'on'
     • log_line_prefix = '%t [%p] '
   ✅ Changes applied successfully!
   ```

6. **Verificar:**
   - Los cambios se aplican inmediatamente
   - Ahora puedes usar EchoDB para ver los logs en tiempo real

### Ejemplo 2: Desactivar Logging en Producción

1. **Abrir el gestor:**
   - Database > Manage PostgreSQL Logging

2. **Conectar a la BD de producción:**
   - Ingresa credenciales de producción

3. **Desactivar logging:**
   - Selecciona: ❌ **Disable Logging**
   - Click en "✅ Apply Changes"

4. **Resultado:**
   ```
   ✅ Connected to PostgreSQL
   ⚙️  Disabling logging...
   Logging disabled successfully. Changes:
     • log_min_duration_statement = -1 (disabled)
     • log_statement = 'none'
     • log_duration = 'off'
   ✅ Changes applied successfully!
   ```

5. **Beneficio:**
   - Mejor performance en producción
   - Menos uso de disco
   - No se registran queries sensibles

### Ejemplo 3: Workflow de Desarrollo

**Durante desarrollo:**
```
1. Activar logging (Enable Full Logging)
2. Desarrollar y probar
3. Usar EchoDB para ver queries en tiempo real
4. Debuggear problemas
```

**Antes de deploy a producción:**
```
1. Desactivar logging (Disable Logging)
2. O configurar logging selectivo (solo errores)
```

**Después de deploy (si hay problemas):**
```
1. Activar logging temporalmente
2. Reproducir el problema
3. Analizar logs
4. Desactivar logging nuevamente
```

## ⚠️ Consideraciones Importantes

### Permisos

- **Requiere superusuario**: El usuario debe tener privilegios de superusuario
- **ALTER SYSTEM**: Necesita permisos para modificar configuración del sistema
- **pg_reload_conf()**: Necesita permisos para recargar configuración

### Performance

**Con logging activado:**
- Overhead de I/O por escribir logs
- Uso de CPU para formatear mensajes
- Uso de disco para almacenar logs
- Impacto: ~5-10% en queries simples

**Con logging desactivado:**
- Performance óptima
- Sin overhead de logging
- Ideal para producción

### Espacio en Disco

**Logging completo puede generar:**
- 100 MB - 1 GB por día en aplicaciones pequeñas
- 1 GB - 10 GB por día en aplicaciones medianas
- 10+ GB por día en aplicaciones grandes

**Recomendación:**
- Monitorea el espacio en disco
- Configura rotación de logs
- Considera logging selectivo (solo queries lentas)

## 💡 Mejores Prácticas

### 1. Desarrollo Local
```
✅ Enable Full Logging
- Ver todas las queries
- Debuggear problemas
- Optimizar queries
```

### 2. Staging/QA
```
✅ Enable Full Logging o Reset to Defaults
- Probar con configuración similar a producción
- Capturar problemas antes de producción
```

### 3. Producción
```
❌ Disable Logging o configuración selectiva
- Solo registrar errores
- Solo registrar queries lentas (> 1000ms)
- Minimizar overhead
```

### 4. Debugging en Producción
```
1. Activar logging temporalmente
2. Reproducir el problema
3. Capturar logs necesarios
4. Desactivar logging inmediatamente
```

## 🔧 Troubleshooting

### "User does not have superuser privileges"

**Solución:**
```sql
-- Conectar como superusuario y ejecutar:
ALTER USER tu_usuario WITH SUPERUSER;
```

### "Failed to configure logging"

**Causas posibles:**
1. Usuario sin permisos suficientes
2. PostgreSQL en modo read-only
3. Problemas de conexión

**Solución:**
- Verifica permisos del usuario
- Verifica que PostgreSQL esté corriendo
- Revisa logs de PostgreSQL

### Los cambios no se aplican

**Solución:**
1. Verifica que `pg_reload_conf()` se ejecutó correctamente
2. En algunos casos, reinicia PostgreSQL:
   ```bash
   pg_ctl restart
   ```

### Logs no aparecen después de activar

**Verifica:**
1. Que la configuración se aplicó correctamente
2. Que el archivo de log existe y tiene permisos
3. Que `logging_collector` esté activado en `postgresql.conf`

## 📊 Comparación de Opciones

| Opción | Queries Registradas | Performance | Uso de Disco | Caso de Uso |
|--------|-------------------|-------------|--------------|-------------|
| **Enable Full Logging** | Todas | -5-10% | Alto | Desarrollo, Debugging |
| **Disable Logging** | Ninguna | Óptimo | Mínimo | Producción |
| **Reset to Defaults** | Según defaults | Normal | Medio | General |

## 🎯 Recomendaciones Finales

1. **Desarrollo**: Siempre activa logging completo
2. **Producción**: Desactiva o usa logging selectivo
3. **Debugging**: Activa temporalmente, luego desactiva
4. **Monitoreo**: Revisa regularmente el espacio en disco
5. **Seguridad**: No registres queries con datos sensibles en producción

---

**Nota:** Los cambios se aplican inmediatamente con `pg_reload_conf()`, pero algunos parámetros pueden requerir reinicio de PostgreSQL para tomar efecto completo.
