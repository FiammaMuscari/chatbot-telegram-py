import os
import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

# Inicializar el bot con el token de Telegram proporcionado
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
# Eliminar el webhook for local testing
#bot.remove_webhook()
#print("Webhook eliminado.")

# Definir un gestor de mensajes para los comandos /start y /help.
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

# Definir un manejador de mensajes para el comando /products
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

# Definir un manejador de mensajes para el comando /prices
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

# Definir un manejador de mensajes para el comando /hours
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

# Definir un manejador de mensajes para el comando /contact
@bot.message_handler(commands=["contact"])
def show_contact(message):
    bot.reply_to(
        message,
        """
    Puedes contactarnos al siguiente número de teléfono: +123456789
    \n O visitarnos en nuestra tienda en la dirección: Calle Ficticia 123, Ciudad Ejemplo
    """
    )

# Definir un gestor de mensajes para textos generales y palabras sueltas
@bot.message_handler(content_types=["text"])
def respond_to_text(message):
    text = message.text.lower()
    
    # Respuestas para palabras sueltas
    responses = {
        "camisas": "¡Nuestras camisas están disponibles en varios colores y tallas!",
        "pantalones": "Tenemos pantalones en diferentes estilos y materiales.",
        "chaquetas": "Las chaquetas son perfectas para el clima frío.",
        "zapatos": "Nuestros zapatos están hechos para tu comodidad y estilo.",
        "oferta": "¡Estamos ofreciendo un 20% de descuento en todos los productos esta semana!",
        "envíos": "Los envíos son gratis para compras superiores a $100.",
    }
    
    # Chequear si el texto del mensaje coincide con alguna de las palabras clave
    for keyword, response in responses.items():
        if keyword in text:
            bot.reply_to(message, response)
            return

    # Responder a saludos comunes
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

# Empezar a recibir mensajes
bot.polling()
