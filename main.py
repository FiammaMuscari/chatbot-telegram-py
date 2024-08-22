import os
import telebot
from flask import Flask, request
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

# Inicializar el bot con el token de Telegram proporcionado
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not TELEGRAM_TOKEN or not WEBHOOK_URL:
    logger.error("Faltan variables de entorno TELEGRAM_TOKEN o WEBHOOK_URL.")
    exit(1)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Define una aplicación Flask
app = Flask(__name__)

# Define la ruta para el webhook
@app.route(f'/{TELEGRAM_TOKEN}', methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return '', 200

# Configura el webhook cuando el script se ejecuta
def set_webhook():
    try:
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        logger.info("Webhook establecido.")
    except Exception as e:
        logger.error(f"Error al establecer el webhook: {e}")

set_webhook()

# Definir los manejadores de mensajes
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        """
    ¡Hola! Bienvenido a la tienda de ropa. Estos son los comandos disponibles:
    \n /products - Ver los productos disponibles
    \n /prices - Consultar los precios
    \n /hours - Consultar el horario de la tienda
    \n /contact - Información de contacto
    \n /start - Mensaje de bienvenida
    """
    )

@bot.message_handler(commands=["products"])
def show_products(message):
    bot.reply_to(
        message,
        """
    Tenemos los siguientes productos:
    \n - Camisas
    \n - Pantalones
    \n - Chaquetas
    \n - Zapatos
    """
    )

@bot.message_handler(commands=["prices"])
def show_prices(message):
    bot.reply_to(
        message,
        """
    Nuestros precios son los siguientes:
    \n - Camisas: $20
    \n - Pantalones: $30
    \n - Chaquetas: $50
    \n - Zapatos: $40
    """
    )

@bot.message_handler(commands=["hours"])
def show_hours(message):
    bot.reply_to(
        message,
        """
    Nuestro horario de atención es:
    \n Lunes a Viernes: 9:00 AM - 7:00 PM
    \n Sábados: 10:00 AM - 5:00 PM
    \n Domingos: Cerrado
    """
    )

@bot.message_handler(commands=["contact"])
def show_contact(message):
    bot.reply_to(
        message,
        """
    Puedes contactarnos al siguiente número de teléfono: +123456789
    \n O visitarnos en nuestra tienda en la dirección: Calle Ficticia 123, Ciudad Ejemplo
    """
    )

@bot.message_handler(content_types=["text"])
def respond_to_text(message):
    text = message.text.lower()
    
    responses = {
        "camisas": "¡Nuestras camisas están disponibles en varios colores y tallas!",
        "pantalones": "Tenemos pantalones en diferentes estilos y materiales.",
        "chaquetas": "Las chaquetas son perfectas para el clima frío.",
        "zapatos": "Nuestros zapatos están hechos para tu comodidad y estilo.",
        "oferta": "¡Estamos ofreciendo un 20% de descuento en todos los productos esta semana!",
        "envíos": "Los envíos son gratis para compras superiores a $100.",
    }
    
    for keyword, response in responses.items():
        if keyword in text:
            bot.reply_to(message, response)
            return

    if text in ["hola", "hello", "hi"]:
        bot.send_message(
            message.chat.id,
            f"Hola {message.from_user.first_name}, ¿en qué puedo ayudarte hoy?",
        )
    else:
        bot.send_message(
            message.chat.id,
            "Lo siento, no entiendo tu mensaje. Usa /help para ver los comandos disponibles.",
        )

# Iniciar el servidor Flask
if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    except Exception as e:
        logger.error(f"Error al iniciar el servidor Flask: {e}")
