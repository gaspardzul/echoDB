# 🚀 Quick Start Guide - EchoDB

## Instalación Rápida (3 pasos)

### 1. Instalar dependencias
```bash
cd "/Users/gaspardzul/Documents/proyectos labs/EchoDB"
./install.sh
```

### 2. Ejecutar la aplicación
```bash
./run.sh
```

O manualmente:
```bash
source venv/bin/activate
python main.py
```

### 3. Usar la aplicación

#### Opción A: Auto-Setup (Recomendado) 🚀
1. Click en **"🔧 Auto-Setup"**
2. Ingresa credenciales de PostgreSQL (user: postgres, password: tu_password)
3. Click en **"Connect & Configure"**
4. Click en **"▶ Start Monitoring"**
5. ¡Listo! Verás los logs en tiempo real

#### Opción B: Manual
1. La ruta del log se carga automáticamente
2. Click en **"▶ Start Monitoring"**
3. ¡Listo! Verás los logs en tiempo real

## 🎯 Casos de Uso Comunes

### Ver solo queries SQL
✅ Activa el checkbox **"Show Queries Only"**

### Buscar queries de una tabla específica
🔍 En el campo **Filter** escribe: `timerecord`

### Ver queries con errores
🔍 En el campo **Filter** escribe: `ERROR`

### Pausar el monitoreo
⏸ Click en **"⏸ Stop Monitoring"**

### Limpiar la pantalla
🗑 Click en **"🗑 Clear"**

## 💡 Tips

- **Auto-scroll**: Mantén activado para ver siempre las últimas entradas
- **Filtros**: Son case-insensitive (no distinguen mayúsculas/minúsculas)
- **Parámetros**: Se muestran automáticamente debajo de cada query
- **Syntax Highlighting**: Los colores te ayudan a identificar rápidamente elementos SQL

## ⚠️ Troubleshooting

### "Log file not found"
Verifica que PostgreSQL esté corriendo y que la ruta sea correcta:
```bash
ls -la ~/Library/Application\ Support/Postgres/var-16/postgresql.log
```

### La aplicación no muestra logs nuevos
1. Usa el **Auto-Setup** para configurar automáticamente
2. O verifica manualmente que `postgresql.conf` tenga:
   ```
   log_min_duration_statement = 0
   ```
3. Reinicia PostgreSQL
4. Reinicia el monitoreo en EchoDB

### "Connection failed" en Auto-Setup
1. Verifica que PostgreSQL esté corriendo:
   ```bash
   pg_isready
   ```
2. Verifica credenciales (usuario debe ser superusuario)
3. Verifica que el puerto sea correcto (por defecto 5432)

### "User does not have superuser privileges"
El usuario necesita permisos de superusuario para configurar parámetros:
```sql
ALTER USER postgres WITH SUPERUSER;
```

### No se instalan las dependencias
```bash
python3 -m pip install --upgrade pip
pip install PyQt6
```

## 📞 Soporte

Para cualquier problema, contacta al equipo de desarrollo.
