import os
import gspread
from dotenv import load_dotenv
from groq import Groq  # Cambio aquí
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from oauth2client.service_account import ServiceAccountCredentials

# Cargar variables de entorno
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NOMBRE_EXCEL = os.getenv("NOMBRE_EXCEL")

# Usamos el cliente de Groq
client = Groq(api_key=GROQ_API_KEY)

# Función para guardar datos en Google Sheets
def guardar_en_sheets(lista_datos):
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name("credenciales.json", scope)
        gc = gspread.authorize(creds)
        sheet = gc.open(os.getenv("NOMBRE_EXCEL")).sheet1
        
        # Insertar la lista directamente
        sheet.append_row(lista_datos)
        return True
    except Exception as e:
        print(f"Error en Sheets: {e}")
        return False

SYSTEM_PROMPT = """
Eres el asistente de Karma Agencia. Tu objetivo es recoger: Nombre, Apellidos, Teléfono y Dirección. Atencion! Si el usuario inicia la conversacion en un idioma diferente al español, responde en ese mismo idioma.

REGLAS DE VALIDACIÓN:
1. Pide los datos uno a uno.
2. TELÉFONO: Debe tener exactamente 9 dígitos.
3. NOMBRE/APELLIDOS: Sin números ni caracteres fuera de lo común.
4. IMPORTANTE: Si el usuario proporciona varios datos en una sola entrada (ej: "Juan López 123456789"), rechaza la entrada amablemente y pide que solo ingrese el dato solicitado. Por ejemplo, si preguntaste por el nombre, solo debe enviar el nombre, no el nombre y apellidos juntos.
5. Valida que cada entrada sea coherente con lo que pediste:
   - Si pediste NOMBRE: Solo debe contener 1-2 palabras máximo
   - Si pediste APELLIDOS: Solo debe contener 1-2 palabras máximo
   - Si pediste TELÉFONO: Solo debe contener dígitos (9)
   - Si pediste DIRECCIÓN: Solo dirección, sin datos adicionales.

FLUJO DE CIERRE:
Cuando tengas los 4 datos válidos:
1. Primero, dale las gracias al usuario y confírmale que el registro ha sido un éxito de forma amable. Despídete.
2. En la ÚLTIMA LÍNEA de tu respuesta, escribe los datos exactamente así:
[DATOS]: Nombre|Apellidos|Teléfono|Dirección
"""

# Diccionario para manejar sesiones de usuario
user_sessions = {}

# Manejador de mensajes asíncrono
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_text = update.message.text

    # Inicializar sesión si no existe
    if user_id not in user_sessions:
        user_sessions[user_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    # Añadir mensaje del usuario a la sesión
    user_sessions[user_id].append({"role": "user", "content": user_text})

    # Llamada a Groq
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Modelo gratuito y potente
        messages=user_sessions[user_id]
    )
    
    # Obtener respuesta del bot
    bot_response = response.choices[0].message.content
    
    # Comprobar si la respuesta contiene datos para guardar
    if "[DATOS]:" in bot_response:
        partes = bot_response.split("[DATOS]:")
        mensaje_amable = partes[0].strip()
        
        datos_brutos = partes[1].strip() 
        lista_datos = [d.strip() for d in datos_brutos.split("|")]
        lista_datos_limpia = lista_datos[:4] 
        
        if guardar_en_sheets(lista_datos_limpia): 
            await update.message.reply_text(mensaje_amable)
            if user_id in user_sessions:
                del user_sessions[user_id]
    else:
        user_sessions[user_id].append({"role": "assistant", "content": bot_response})
        await update.message.reply_text(bot_response)

# Inicio del bot
if __name__ == '__main__':
    print("Bot activo...")
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()