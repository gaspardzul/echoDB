# Guía de Análisis con IA - EchoDB

## 🤖 Introducción

EchoDB integra inteligencia artificial para ayudarte a analizar tus logs de PostgreSQL de manera inteligente. Puedes hacer preguntas en lenguaje natural y obtener insights valiosos.

## 🎯 Proveedores Soportados

### 1. OpenAI
- **Modelos**: GPT-4o, GPT-4o-mini, GPT-4-turbo, GPT-3.5-turbo
- **Mejor para**: Análisis general, explicaciones detalladas
- **Costo**: Medio-Alto
- **API Key**: https://platform.openai.com/api-keys

### 2. Claude (Anthropic)
- **Modelos**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
- **Mejor para**: Análisis técnico profundo, código SQL
- **Costo**: Medio
- **API Key**: https://console.anthropic.com/

### 3. DeepSeek
- **Modelos**: DeepSeek Chat, DeepSeek Coder
- **Mejor para**: Análisis de código, debugging
- **Costo**: Bajo
- **API Key**: https://platform.deepseek.com/

## 🚀 Configuración Inicial

### Paso 1: Obtener API Key

**OpenAI:**
1. Ve a https://platform.openai.com/api-keys
2. Crea una cuenta o inicia sesión
3. Click en "Create new secret key"
4. Copia la key (empieza con `sk-...`)

**Claude:**
1. Ve a https://console.anthropic.com/
2. Crea una cuenta
3. Ve a "API Keys"
4. Genera una nueva key (empieza con `sk-ant-...`)

**DeepSeek:**
1. Ve a https://platform.deepseek.com/
2. Regístrate
3. Ve a API Keys
4. Crea una nueva key

### Paso 2: Configurar en EchoDB

1. Abre EchoDB
2. Menú: **AI > Configure AI Providers**
3. Selecciona tu proveedor
4. Pega tu API key
5. Selecciona el modelo
6. Click en "💾 Save Configuration"

## 💬 Usando el Chat de IA

### Abrir el Chat

**Opción 1: Desde un tab**
1. Asegúrate de tener logs en el tab
2. Click en el botón **"🤖 AI Chat"**

**Opción 2: Desde el menú**
1. AI > Configure AI Providers
2. Configura tu proveedor

### Ejemplos de Preguntas

#### Análisis de Errores
```
¿Qué errores ocurrieron en los últimos logs?
```

```
Identifica los errores más críticos y explica sus causas
```

```
¿Hay algún patrón en los errores que estoy viendo?
```

#### Queries Lentas
```
¿Cuáles son las queries más lentas?
```

```
Analiza las queries que tardan más de 1 segundo
```

```
¿Qué queries debería optimizar primero?
```

#### Análisis de Patrones
```
¿Hay algún patrón inusual en estos logs?
```

```
¿Qué tablas se están consultando más frecuentemente?
```

```
Identifica posibles problemas de performance
```

#### Optimización
```
Sugiere optimizaciones para las queries más lentas
```

```
¿Cómo puedo mejorar el performance de estas queries?
```

```
¿Debería agregar índices? ¿En qué columnas?
```

#### Resúmenes
```
Resume los principales problemas en estos logs
```

```
Dame un resumen ejecutivo de lo que está pasando
```

```
¿Qué debería revisar primero?
```

## 🎨 Interfaz del Chat

### Elementos

1. **Header**: Muestra el proveedor y modelo actual
2. **Chat Display**: Conversación con la IA
3. **Quick Questions**: Botones con preguntas sugeridas
4. **Input Field**: Escribe tu pregunta
5. **Send Button**: Envía la pregunta
6. **Clear Button**: Limpia la conversación

### Sugerencias Rápidas

- **Summarize errors**: Resume los errores encontrados
- **Find slow queries**: Identifica queries lentas
- **Analyze patterns**: Busca patrones inusuales

## 💡 Tips y Mejores Prácticas

### 1. Sé Específico
❌ "¿Qué ves aquí?"
✅ "¿Qué errores de conexión hay en estos logs?"

### 2. Contexto
❌ "¿Está lento?"
✅ "¿Hay queries que tarden más de 500ms? ¿Cuáles son?"

### 3. Iterativo
```
Usuario: ¿Qué errores hay?
IA: Hay 3 errores de timeout...
Usuario: ¿Qué causa esos timeouts?
IA: Los timeouts son causados por...
Usuario: ¿Cómo los soluciono?
```

### 4. Usa el Historial
La IA recuerda la conversación, puedes hacer preguntas de seguimiento.

### 5. Limita el Alcance
Si tienes muchos logs, filtra primero:
- Usa el filtro de texto
- Activa "Queries Only"
- Luego abre el AI Chat

## 🔒 Seguridad y Privacidad

### Almacenamiento de API Keys
- Las API keys se guardan en SQLite local: `~/.echodb/echodb.db`
- Solo tú tienes acceso
- No se comparten con nadie
- Están en tu máquina

### Datos Enviados
- Solo se envían los logs visibles en el tab actual
- Máximo ~8000 caracteres de logs
- No se envía información de tu sistema
- No se almacenan logs en los servidores de IA

### Recomendaciones
- ⚠️ No uses en logs con datos sensibles (passwords, tokens)
- ⚠️ Filtra información confidencial antes de usar AI Chat
- ✅ Usa en logs de desarrollo/staging
- ✅ Revisa los logs antes de enviarlos

## 💰 Costos Estimados

### OpenAI (GPT-4o-mini)
- ~$0.15 por millón de tokens de entrada
- ~$0.60 por millón de tokens de salida
- **Costo típico por pregunta**: $0.001 - $0.01

### Claude (Claude 3.5 Sonnet)
- ~$3.00 por millón de tokens de entrada
- ~$15.00 por millón de tokens de salida
- **Costo típico por pregunta**: $0.01 - $0.05

### DeepSeek
- ~$0.14 por millón de tokens de entrada
- ~$0.28 por millón de tokens de salida
- **Costo típico por pregunta**: $0.0005 - $0.005

**Nota**: Los costos son aproximados y pueden variar.

## 🛠️ Troubleshooting

### "AI Not Configured"
**Solución**: Configura tu proveedor en AI > Configure AI Providers

### "No API Key"
**Solución**: Agrega tu API key en la configuración

### "Error: 401 Unauthorized"
**Causa**: API key inválida
**Solución**: Verifica que copiaste la key correctamente

### "Error: 429 Too Many Requests"
**Causa**: Límite de rate excedido
**Solución**: Espera unos minutos y vuelve a intentar

### "No logs available"
**Causa**: El tab no tiene logs aún
**Solución**: Inicia el monitoreo primero con "▶ Start"

### La IA no responde
**Posibles causas**:
1. Problema de conexión a internet
2. API del proveedor caída
3. Timeout (queries muy largas)

**Solución**: Verifica tu conexión y vuelve a intentar

## 📊 Casos de Uso Reales

### Caso 1: Debugging de Producción
```
Situación: Errores intermitentes en producción
Pregunta: "¿Hay algún patrón temporal en estos errores?"
Resultado: IA identifica que errores ocurren cada 5 minutos
Acción: Revisar cron jobs que corren cada 5 minutos
```

### Caso 2: Optimización de Performance
```
Situación: App lenta
Pregunta: "¿Qué queries están causando el mayor impacto en performance?"
Resultado: IA identifica 3 queries sin índices
Acción: Agregar índices sugeridos
```

### Caso 3: Análisis de Carga
```
Situación: Preparar para Black Friday
Pregunta: "¿Qué tablas reciben más tráfico y podrían ser cuellos de botella?"
Resultado: IA identifica tabla 'products' con 80% de queries
Acción: Implementar caché para productos
```

## 🎓 Aprende Más

### Recursos
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Claude API Docs](https://docs.anthropic.com/)
- [DeepSeek Docs](https://platform.deepseek.com/docs)

### Comunidad
- Comparte tus mejores prompts
- Aprende de otros usuarios
- Contribuye con ejemplos

---

**Nota**: El análisis con IA es una herramienta de ayuda. Siempre verifica las sugerencias antes de implementarlas en producción.
