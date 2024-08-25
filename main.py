import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

# Inicializar el bot con el token de Telegram proporcionado
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Eliminar el webhook para pruebas locales
bot.remove_webhook()

# Crear el teclado en línea usando InlineKeyboardMarkup
inline_keyboard = InlineKeyboardMarkup()

# Botones en un diccionario
inline_buttons = [
    ("📥 Operar", "Operate"),
    ("📬 Countrier", "Countier"),
    ("📩 Español", "LangSelect"),
    ("📤 Nosotros", "OurTeam"),
    ("❌ Close", "Close"),
]

# Agregar los botones al teclado en línea, 2 botones por fila
inline_keyboard.row(
    InlineKeyboardButton(inline_buttons[0][0], callback_data=inline_buttons[0][1]),
    InlineKeyboardButton(inline_buttons[1][0], callback_data=inline_buttons[1][1])
)
inline_keyboard.row(
    InlineKeyboardButton(inline_buttons[2][0], callback_data=inline_buttons[2][1]),
    InlineKeyboardButton(inline_buttons[3][0], callback_data=inline_buttons[3][1])
)
# Agregar el último botón en una fila separada
inline_keyboard.add(InlineKeyboardButton(inline_buttons[4][0], callback_data=inline_buttons[4][1]))

# Definir un gestor de mensajes para los comandos /start y /help.
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        f"¡Hola {message.from_user.first_name}! Bienvenido a nuestro operador en línea. Para dudas y órdenes, presione los botones o use los comandos disponibles. Para más información, use /help.",
        reply_markup=inline_keyboard
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
    """,
        reply_markup=inline_keyboard
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
    """,
        reply_markup=inline_keyboard
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
    """,
        reply_markup=inline_keyboard
    )

# Definir un manejador de mensajes para el comando /contact
@bot.message_handler(commands=["contact"])
def show_contact(message):
    bot.reply_to(
        message,
        """
    Puedes contactarnos al siguiente número de teléfono: +123456789
    \n O visitarnos en nuestra tienda en la dirección: Calle Ficticia 123, Ciudad Ejemplo
    """,
        reply_markup=inline_keyboard
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
            bot.reply_to(message, response, reply_markup=inline_keyboard)
            return

    # Responder a saludos comunes
    if text in ["hola", "hello", "hi"]:
        bot.send_message(
            message.chat.id,
            f"Hola {message.from_user.first_name}, ¿en qué puedo ayudarte hoy?",
            reply_markup=inline_keyboard
        )
    else:
        bot.send_message(
            message.chat.id,
            "Lo siento, no entiendo tu mensaje. Usa /help para ver los comandos disponibles.",
            reply_markup=inline_keyboard
        )

# Manejar los callback_query para botones en línea
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    callback_data = call.data

    if callback_data == "Operate":
        bot.answer_callback_query(call.id, "Operar seleccionado!")
    elif callback_data == "Countier":
        bot.answer_callback_query(call.id, "Countrier seleccionado!")
    elif callback_data == "LangSelect":
        bot.answer_callback_query(call.id, "Idioma seleccionado!")
    elif callback_data == "OurTeam":
        bot.answer_callback_query(call.id, "Nosotros seleccionado!")
    elif callback_data == "Close":
        bot.answer_callback_query(call.id, "Cerrando...")
    else:
        bot.answer_callback_query(call.id, "¡Acción desconocida!")

# Empezar a recibir mensajes
bot.polling()
