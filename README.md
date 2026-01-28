# 🤖 Conversacional Bot - Karma Agencia

Un sistema integral de captura de datos con un bot conversacional de Telegram y un dashboard administrativo para gestión de usuarios.

## 📋 Descripción General

Este proyecto implementa una solución completa que:
- **Bot de Telegram**: Recopila datos de usuarios de forma conversacional e inteligente
- **Dashboard Web**: Gestiona y edita todos los datos recopilados en tiempo real
- **Base de Datos Cloud**: Integración con Google Sheets para almacenamiento persistente
- **IA Conversacional**: Utiliza el modelo Llama 3.3 de Groq para interacciones naturales

## 🎯 Características Principales

### Bot Conversacional (bot_karma.py)
- ✅ Interfaz amable y natural con usuarios
- ✅ Validación automática de datos:
  - Teléfono: Exactamente 9 dígitos
  - Nombre/Apellidos: Sin números, máximo 1-2 palabras
  - **Valida entrada única por campo**: Rechaza si el usuario proporciona múltiples datos juntos (ej: "Juan López" cuando se pide solo nombre)
  - Evita confusiones entre campos solicitados
- ✅ Recopilación estructurada de datos:
  - Nombre
  - Apellidos
  - Teléfono
  - Dirección
- ✅ Sesiones independientes por usuario
- ✅ Guardado automático en Google Sheets al completar
- ✅ Respuestas personalizadas gracias a IA avanzada
- ✅ Multiidioma: Responde en el idioma del usuario

### Dashboard Administrativo (dashboard.py)
- 📊 Interfaz web moderna con Streamlit
- ✏️ Edición directa de registros en tiempo real
- ➕ Agregar nuevos registros manualmente
- 🗑️ Eliminar registros directamente desde la interfaz
- 🔄 Auto-refresh automático cada 15 segundos
- 💾 Sincronización automática con Google Sheets
- 🎨 Diseño responsive y amigable

## 🛠️ Stack Tecnológico

| Componente | Tecnología |
|-----------|-----------|
| **Bot de Telegram** | python-telegram-bot |
| **IA Conversacional** | Groq (Llama 3.3 70B) |
| **Dashboard Web** | Streamlit + Auto-refresh |
| **Base de Datos** | Google Sheets |
| **Autenticación** | OAuth2 (Google Service Account) |
| **Configuración** | python-dotenv |

## 📦 Requisitos

- Python 3.8+
- Cuota gratuita de Groq (IA sin costo)
- Bot de Telegram (desde BotFather)
- Credenciales de Google Sheets

### Dependencias Python

```bash
pip install -r requirements.txt
```

Archivo `requirements.txt`:
```
python-telegram-bot
groq
gspread
oauth2client
python-dotenv
streamlit
streamlit-autorefresh
pandas
google-auth-oauthlib
```


## 🚀 Instalación y Configuración

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tu-usuario/Conversacional_Bot.git
cd Conversacional_Bot
```

### 2. Crear Entorno Virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
TELEGRAM_TOKEN=Tu_Token_Del_Bot_De_Telegram
GROQ_API_KEY=Tu_API_Key_De_Groq
NOMBRE_EXCEL=Nombre_De_Tu_Hoja_De_Cálculo_En_Google_Sheets
```

### 5. Autenticación con Google Sheets

1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear un proyecto nuevo
3. Habilitar Google Sheets API y Google Drive API
4. Crear una "Service Account"
5. Descargar las credenciales en formato JSON
6. Guardar el archivo como `credenciales.json` en la raíz del proyecto
7. Compartir la hoja de Google Sheets con el correo de la Service Account (Se encuentra dentro del JSON)

## 💻 Cómo Usar

### Iniciar el Bot de Telegram

```bash
python bot_karma.py
```

El bot estará escuchando mensajes de Telegram. Cuando un usuario lo contacte:
1. El bot solicita los datos de forma amable
2. Valida cada campo
3. Al completarse, guarda automáticamente en Google Sheets
4. Envía un mensaje de confirmación

### Iniciar el Dashboard

```bash
streamlit run dashboard.py
```

Accede a `http://localhost:8501` en tu navegador:
1. Ver todos los registros en una tabla
2. Editar cualquier dato directamente
3. Agregar nuevas filas
4. Eliminar registros
5. Guardar cambios en la nube con un clic

## 🔧 Estructura del Código

### bot_karma.py

```python
# Variables clave:
SYSTEM_PROMPT      # Instrucciones para la IA (prompt)
user_sessions      # Diccionario de sesiones por usuario
client            # Cliente de Groq API (Llama 3.3 70B)

# Funciones principales:
guardar_en_sheets() # Inserta datos en Google Sheets
handle_message()    # Procesa mensajes del usuario
```

**Características**:
- ✅ Respuestas en el mismo idioma del usuario
- ✅ Validación automática de datos (9 dígitos para teléfono, nombres coherentes)
- ✅ Sesiones independientes por usuario
- ✅ Integración directa con Groq API

**Flujo de Funcionamiento**:
1. Usuario envía mensaje
2. Se crea/recupera sesión del usuario
3. Se envía a Groq con context histórico
4. Se recibe respuesta de la IA
5. Si contiene `[DATOS]:`, se extraen y guardan
6. Se limpia la sesión tras completación

### dashboard.py

```python
# Componentes principales:
st_autorefresh()     # Auto-actualización cada 15 segundos
st.data_editor()     # Tabla editable interactiva (permite añadir/eliminar filas)
sheet.update()       # Sincronización con Google Sheets
st.button()          # Botones de acción
```

**Características**:
- 🔄 Actualización automática cada 15 segundos
- ✏️ Edición inline de cualquier celda
- ➕ Adición de nuevas filas dinámicamente
- 🗑️ Eliminación de registros desde la interfaz
- 💾 Guardado con un clic en Google Sheets

**Flujo de Funcionamiento**:
1. Carga datos actuales de Google Sheets
2. Muestra tabla editable con auto-refresh
3. Permite edición, adición y eliminación de filas
4. Al guardar, sincroniza con Google Sheets

## 📊 Formato de Datos

Los datos se guardan en Google Sheets con la siguiente estructura:

| Nombre | Apellidos | Teléfono | Dirección |
|--------|-----------|----------|-----------|
| Juan | García López | 612345678 | Calle Principal 123 |
| María | Rodríguez | 687654321 | Avenida Central 456 |

## 🔐 Seguridad

- ✅ Las credenciales de Google están en `credenciales.json` (no en el código)
- ✅ Las variables sensibles están en `.env` (no en versión)
- ✅ Validación de datos en cliente y servidor
- ✅ Sesiones independientes por usuario

## 📈 Mejoras Futuras

- [ ] Filtros y búsqueda en el dashboard
- [ ] Autenticación de usuarios
- [ ] Historial de cambios
- [ ] Notificaciones por email
- [ ] API REST para integración
- [ ] Validación más compleja de datos

## 📝 Licencia

Este proyecto está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado por Agustín Rubí Hernández

---

## 🔗 Enlaces Útiles

- [Documentación de python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [Documentación de Streamlit](https://docs.streamlit.io/)
- [API de Groq](https://console.groq.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)

## 💬 Soporte

Para reportar problemas o sugerencias, crea un issue en el repositorio.

---

**Última actualización**: 27/01/2026

### 🆕 Cambios Recientes

- ✅ Migración a **Groq API** (Llama 3.3 70B) para mejor rendimiento
- ✅ Adición de **auto-refresh** en dashboard cada 15 segundos
- ✅ Interfaz mejorada del editor de datos con **soporte dinámico** para añadir/eliminar filas
- ✅ Soporte **multiidioma** en el bot conversacional
- ✅ Validación mejorada para entrada de datos:
  - Ahora rechaza entradas múltiples (ej: "Juan López" cuando solo se pide el nombre)
  - Valida que cada campo contenga solo el dato solicitado
  - Verifica coherencia: Nombre/Apellidos máximo 1-2 palabras, Teléfono solo dígitos
  - Evita que direcciones contengan números de teléfono
