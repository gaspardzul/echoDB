# Guía del Database Monitor - EchoDB

## 🔍 Introducción

El Database Monitor es una herramienta integrada en EchoDB que te permite monitorear en tiempo real el estado y rendimiento de tu base de datos PostgreSQL.

## 🚀 Cómo Acceder

1. Abre EchoDB
2. Menú: **Database > 🔍 Database Monitor**
3. Click en **🔌 Connect**
4. Ingresa credenciales de tu base de datos

## 📊 Tab 1: Overview

### Métricas Disponibles

#### 🔗 Connections
- **Active**: Número de conexiones activas actualmente
- **Max**: Máximo de conexiones permitidas (configurado en PostgreSQL)
- **Barra de progreso**: Visualización del uso de conexiones

**Interpretación:**
- 🟢 Verde (< 70%): Uso normal
- 🟡 Amarillo (70-90%): Atención
- 🔴 Rojo (> 90%): Crítico - considera aumentar max_connections

#### ⚡ Performance

**TPS (Transactions Per Second)**
- Número de transacciones (commits + rollbacks) por segundo
- **Bueno**: > 100 TPS para apps normales
- **Excelente**: > 1000 TPS para apps de alta carga

**Cache Hit Ratio**
- Porcentaje de lecturas que se sirven desde caché
- **Óptimo**: > 95%
- **Aceptable**: 90-95%
- **Problema**: < 90% (considera aumentar shared_buffers)

**Active Queries**
- Número de queries ejecutándose ahora mismo
- Útil para detectar picos de carga

**Locks**
- Número de locks en espera
- **Normal**: 0-5
- **Problema**: > 10 (posible deadlock o query lenta)

#### 💾 Database Size
- Tamaño total de todas las bases de datos
- Útil para planificar espacio en disco

## ⚡ Tab 2: Active Queries

### Información Mostrada

| Columna | Descripción |
|---------|-------------|
| **PID** | Process ID del backend de PostgreSQL |
| **User** | Usuario que ejecuta la query |
| **Database** | Base de datos donde se ejecuta |
| **State** | Estado actual (active, idle in transaction, etc.) |
| **Duration** | Tiempo que lleva ejecutándose (en segundos) |
| **Query** | Primeros 100 caracteres de la query |

### Acciones Disponibles

#### ❌ Kill Selected Query
1. Selecciona una query de la tabla
2. Click en "❌ Kill Selected Query"
3. Confirma la acción
4. La query se terminará inmediatamente

**⚠️ Precaución:**
- Terminar queries puede causar rollback de transacciones
- Solo termina queries problemáticas (ej: queries que llevan > 5 minutos)
- Verifica que no sea una query crítica del sistema

### Casos de Uso

**Detectar Queries Lentas:**
```
1. Ordena por Duration (click en header)
2. Identifica queries con > 60s
3. Analiza el query text
4. Optimiza o termina si es necesario
```

**Identificar Usuarios Problemáticos:**
```
1. Busca usuarios con múltiples queries activas
2. Verifica si están bloqueando recursos
3. Contacta al usuario o termina queries
```

## 📈 Tab 3: Database Stats

### Información por Base de Datos

| Columna | Descripción |
|---------|-------------|
| **Database** | Nombre de la base de datos |
| **Size** | Tamaño en disco (MB, GB) |
| **Tables** | Número de tablas en schema public |
| **Connections** | Conexiones activas a esta BD |

### Análisis

**Crecimiento de BD:**
- Monitorea el tamaño regularmente
- Planifica VACUUM y mantenimiento
- Identifica BDs que crecen rápido

**Distribución de Conexiones:**
- Verifica que las conexiones estén balanceadas
- Detecta BDs con muchas conexiones (posible problema)

## 🔄 Auto-Refresh

### Configuración

**Activar/Desactivar:**
- Click en "🔄 Auto-Refresh: ON/OFF"
- Verde = Activado (refresh cada 5 segundos)
- Gris = Desactivado (refresh manual)

**Refresh Manual:**
- Click en "🔃 Refresh Now"
- Actualiza datos inmediatamente

### Recomendaciones

**Cuándo usar Auto-Refresh:**
- ✅ Monitoreo activo de problemas
- ✅ Debugging de performance
- ✅ Durante deploys o migraciones

**Cuándo desactivarlo:**
- ❌ Solo necesitas un snapshot
- ❌ Quieres reducir carga en la BD
- ❌ Analizando datos históricos

## 💡 Casos de Uso Reales

### Caso 1: BD Lenta

**Síntomas:**
- TPS bajo (< 50)
- Cache Hit Ratio bajo (< 90%)
- Muchas queries activas (> 20)

**Diagnóstico:**
1. Tab Overview: Verifica métricas
2. Tab Active Queries: Identifica queries lentas
3. Analiza las queries problemáticas
4. Optimiza o agrega índices

**Solución:**
```sql
-- Ejemplo: Agregar índice
CREATE INDEX idx_users_email ON users(email);

-- Aumentar shared_buffers en postgresql.conf
shared_buffers = 256MB  # aumentar según RAM disponible
```

### Caso 2: Conexiones Agotadas

**Síntomas:**
- Active connections cerca de max (> 90%)
- Errores "too many connections"

**Diagnóstico:**
1. Tab Overview: Verifica conexiones
2. Tab Active Queries: Identifica queries idle
3. Tab Database Stats: Ve qué BD consume más

**Solución:**
```sql
-- Terminar conexiones idle
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE state = 'idle in transaction'
AND state_change < now() - interval '10 minutes';

-- Aumentar max_connections en postgresql.conf
max_connections = 200  # ajustar según necesidad
```

### Caso 3: Query Bloqueada

**Síntomas:**
- Locks > 5
- Query con duration muy alta
- Otros queries esperando

**Diagnóstico:**
1. Tab Active Queries: Identifica query bloqueante
2. Verifica el PID
3. Analiza qué está haciendo

**Solución:**
```
1. Intenta esperar a que termine naturalmente
2. Si es crítico, usa "Kill Selected Query"
3. Investiga por qué se bloqueó
4. Optimiza la query o transacción
```

### Caso 4: BD Creciendo Rápido

**Síntomas:**
- Database size aumenta rápidamente
- Espacio en disco bajo

**Diagnóstico:**
1. Tab Database Stats: Identifica BD grande
2. Conecta a esa BD
3. Analiza tablas grandes

**Solución:**
```sql
-- Ver tablas más grandes
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 10;

-- Ejecutar VACUUM
VACUUM FULL ANALYZE;
```

## 🎯 Mejores Prácticas

### Monitoreo Regular

**Diario:**
- ✅ Revisa Overview para detectar tendencias
- ✅ Verifica que cache hit ratio > 95%
- ✅ Confirma que conexiones < 70% de max

**Semanal:**
- ✅ Analiza Database Stats para crecimiento
- ✅ Identifica queries que aparecen frecuentemente en Active Queries
- ✅ Planifica mantenimiento (VACUUM, ANALYZE)

**Mensual:**
- ✅ Revisa tendencias de TPS
- ✅ Evalúa si necesitas más recursos
- ✅ Optimiza queries más frecuentes

### Alertas Manuales

Considera tomar acción si:
- 🔴 Conexiones > 90% de max
- 🔴 Cache hit ratio < 90%
- 🔴 Locks > 10
- 🔴 Queries con duration > 300s
- 🔴 TPS cae súbitamente

## 🛠️ Troubleshooting

### "Connection Failed"
**Causa:** Credenciales incorrectas o BD no accesible
**Solución:** Verifica host, port, user, password

### "No data showing"
**Causa:** Usuario sin permisos
**Solución:** Conecta con usuario con permisos de superuser o pg_monitor

### "Queries table empty"
**Causa:** No hay queries activas
**Solución:** Normal si la BD está idle

### "Auto-refresh stopped"
**Causa:** Conexión perdida
**Solución:** Reconecta usando "🔌 Connect"

## 📚 Queries SQL Utilizadas

El monitor usa estas queries de PostgreSQL:

```sql
-- Conexiones activas
SELECT count(*) as active, 
       (SELECT setting::int FROM pg_settings WHERE name = 'max_connections') as max
FROM pg_stat_activity 
WHERE state != 'idle';

-- TPS
SELECT sum(xact_commit + xact_rollback) / 
       GREATEST(EXTRACT(EPOCH FROM (now() - stats_reset)), 1) as tps
FROM pg_stat_database;

-- Cache Hit Ratio
SELECT round(100.0 * sum(blks_hit) / NULLIF(sum(blks_hit + blks_read), 0), 2)
FROM pg_stat_database;

-- Active Queries
SELECT pid, usename, datname, state, 
       EXTRACT(EPOCH FROM (now() - query_start))::int as duration,
       query
FROM pg_stat_activity 
WHERE state != 'idle' AND pid != pg_backend_pid();

-- Database Stats
SELECT datname,
       pg_size_pretty(pg_database_size(datname)) as size,
       numbackends
FROM pg_stat_database
WHERE datname NOT IN ('template0', 'template1');
```

## 🔒 Seguridad

**Permisos Necesarios:**
- Lectura de `pg_stat_activity`
- Lectura de `pg_stat_database`
- Ejecución de `pg_terminate_backend()` (para kill queries)

**Recomendación:**
- Usa un usuario con rol `pg_monitor` para monitoreo
- Solo usa superuser si necesitas kill queries

---

**Nota:** El Database Monitor es una herramienta de observación. Siempre analiza antes de tomar acciones que puedan afectar la BD en producción.
