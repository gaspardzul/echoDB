# Ejemplos de Uso - EchoDB

## 🚀 Ejemplo 1: Primera Configuración (Auto-Setup)

### Paso a Paso

1. **Instalar y ejecutar**:
```bash
cd "/Users/gaspardzul/Documents/proyectos labs/EchoDB"
./install.sh
./run.sh
```

2. **Configurar PostgreSQL automáticamente**:
   - Click en botón **"🔧 Auto-Setup"**
   - Ingresa credenciales:
     ```
     Host: localhost
     Port: 5432
     Database: postgres
     User: postgres
     Password: [tu_password]
     ```
   - Marca: ✅ **Configure logging parameters**
   - Click: **"Connect & Configure"**

3. **Resultado esperado**:
```
✅ Connected to PostgreSQL
⚙️  Configuring logging parameters...
Logging configured successfully. Changes:
  • log_min_duration_statement = 0
  • log_statement = 'all'
  • log_duration = 'on'
  • log_line_prefix = '%t [%p] '

📁 Log directory: /Users/gaspardzul/Library/Application Support/Postgres/var-16
✅ Found log file: /Users/gaspardzul/Library/Application Support/Postgres/var-16/postgresql.log
✅ Configuration complete!
```

4. **Iniciar monitoreo**:
   - Click: **"▶ Start Monitoring"**
   - ¡Listo! Verás logs en tiempo real

---

## 🔍 Ejemplo 2: Filtrar Queries de una Tabla Específica

### Escenario
Quieres ver solo las queries relacionadas con la tabla `timerecord`.

### Pasos
1. En el campo **Filter**, escribe: `timerecord`
2. Activa: ✅ **Show Queries Only**
3. Los logs mostrarán solo queries que contengan "timerecord"

### Ejemplo de Output
```sql
2026-03-31 15:23:45.123 CST [5678] LOG:  execute <unnamed>: 
SELECT timerecord.id, timerecord.created_at 
FROM timerecord 
WHERE timerecord.node_id = $1 
ORDER BY timerecord.created_at DESC 
LIMIT $2
    DETAIL:  parameters: $1 = 'NODO_01', $2 = '50'

2026-03-31 15:23:45.456 CST [5679] LOG:  execute <unnamed>: 
INSERT INTO timerecord (node_id, client_id, data) 
VALUES ($1, $2, $3)
    DETAIL:  parameters: $1 = 'NODO_02', $2 = 'CLI_123', $3 = '{"key": "value"}'
```

---

## 🐛 Ejemplo 3: Debugging - Encontrar Queries Lentas

### Escenario
Tu aplicación está lenta y quieres identificar queries problemáticas.

### Pasos
1. **Iniciar monitoreo** en EchoDB
2. **Ejecutar** la acción lenta en tu aplicación
3. En EchoDB, buscar en el campo **Filter**: `duration`
4. Observar las queries con mayor duración

### Ejemplo de Output
```sql
2026-03-31 15:30:12.123 CST [9012] LOG:  duration: 2543.234 ms  execute <unnamed>: 
SELECT * FROM large_table 
WHERE status = $1 
ORDER BY created_at DESC
    DETAIL:  parameters: $1 = 'active'
```

### Acción
- Identificaste que la query tarda 2.5 segundos
- Solución: Agregar índice en `large_table(status, created_at)`

---

## 📊 Ejemplo 4: Monitorear Inserts en Tiempo Real

### Escenario
Quieres ver todos los INSERT que se ejecutan en tu sistema.

### Pasos
1. En el campo **Filter**, escribe: `INSERT`
2. Activa: ✅ **Show Queries Only**
3. Observa los inserts en tiempo real

### Ejemplo de Output
```sql
2026-03-31 16:00:01.111 CST [1111] LOG:  execute <unnamed>: 
INSERT INTO users (email, name, created_at) 
VALUES ($1, $2, NOW())
    DETAIL:  parameters: $1 = 'user@example.com', $2 = 'John Doe'

2026-03-31 16:00:01.222 CST [1112] LOG:  execute <unnamed>: 
INSERT INTO audit_log (user_id, action, timestamp) 
VALUES ($1, $2, $3)
    DETAIL:  parameters: $1 = '123', $2 = 'login', $3 = '2026-03-31 16:00:01'
```

---

## ⚠️ Ejemplo 5: Detectar Errores SQL

### Escenario
Quieres ver solo los errores que ocurren en la base de datos.

### Pasos
1. En el campo **Filter**, escribe: `ERROR`
2. Observa los errores en tiempo real

### Ejemplo de Output
```sql
2026-03-31 16:15:30.123 CST [2222] ERROR:  duplicate key value violates unique constraint "users_email_key"
2026-03-31 16:15:30.124 CST [2222] DETAIL:  Key (email)=(user@example.com) already exists.
2026-03-31 16:15:30.125 CST [2222] STATEMENT:  INSERT INTO users (email, name) VALUES ($1, $2)
```

### Acción
- Identificaste un error de constraint violation
- Solución: Implementar validación antes del insert

---

## 🔄 Ejemplo 6: Monitorear Updates Masivos

### Escenario
Estás ejecutando un script de migración y quieres ver los updates.

### Pasos
1. En el campo **Filter**, escribe: `UPDATE`
2. Activa: ✅ **Show Queries Only**
3. Ejecuta tu script de migración
4. Observa los updates en tiempo real

### Ejemplo de Output
```sql
2026-03-31 17:00:00.001 CST [3333] LOG:  execute <unnamed>: 
UPDATE products SET price = price * $1 WHERE category = $2
    DETAIL:  parameters: $1 = '1.10', $2 = 'electronics'

2026-03-31 17:00:00.002 CST [3333] LOG:  execute <unnamed>: 
UPDATE inventory SET stock = stock - $1 WHERE product_id = $2
    DETAIL:  parameters: $1 = '5', $2 = 'PROD_001'
```

---

## 🎯 Ejemplo 7: Análisis de Parámetros

### Escenario
Quieres ver qué valores se están pasando a una query específica.

### Pasos
1. En el campo **Filter**, escribe el nombre de la tabla o query
2. Observa la sección **DETAIL** que muestra los parámetros

### Ejemplo de Output
```sql
2026-03-31 18:00:00.123 CST [4444] LOG:  execute <unnamed>: 
SELECT * FROM orders 
WHERE customer_id = $1 
  AND status IN ($2, $3) 
  AND created_at > $4
    DETAIL:  parameters: $1 = 'CUST_123', $2 = 'pending', $3 = 'processing', $4 = '2026-03-01'
```

### Análisis
- Customer ID: CUST_123
- Status buscados: pending, processing
- Fecha desde: 2026-03-01

---

## 💡 Tips Profesionales

### 1. Combinar Filtros
Usa palabras clave específicas para filtrar mejor:
- `SELECT * FROM users` → Ver solo selects de users
- `WHERE user_id =` → Ver queries con condición específica

### 2. Auto-scroll
- **Activado**: Para monitoreo en tiempo real
- **Desactivado**: Para analizar logs históricos sin que se muevan

### 3. Clear Frecuente
Usa el botón **🗑 Clear** para limpiar la pantalla cuando haya muchos logs y quieras empezar de nuevo.

### 4. Syntax Highlighting
Los colores te ayudan a identificar rápidamente:
- **Azul**: Keywords SQL (SELECT, WHERE, etc.)
- **Naranja**: Strings ('valores')
- **Cyan**: Parámetros ($1, $2)
- **Rojo**: Errores

---

## 🔧 Workflow Recomendado para Desarrollo

1. **Inicio del día**:
   - Ejecutar EchoDB
   - Click en **"▶ Start Monitoring"**
   - Dejar corriendo en segundo plano

2. **Durante desarrollo**:
   - Cuando algo falla, revisar EchoDB
   - Filtrar por tabla o tipo de query
   - Analizar parámetros y errores

3. **Debugging**:
   - Reproducir el bug
   - Observar queries en tiempo real
   - Identificar query problemática
   - Copiar query y parámetros para testing

4. **Optimización**:
   - Filtrar por `duration` para ver queries lentas
   - Identificar N+1 queries
   - Analizar índices faltantes

---

## 📝 Notas Importantes

- EchoDB **NO modifica** tu base de datos, solo lee logs
- Los logs se muestran en tiempo real con ~100ms de delay
- Puedes tener EchoDB corriendo mientras desarrollas
- Compatible con cualquier aplicación que use PostgreSQL
