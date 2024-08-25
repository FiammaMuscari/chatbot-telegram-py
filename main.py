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

# Crear el teclado en línea principal
inline_keyboard = InlineKeyboardMarkup()
inline_buttons = [
    ("📥 Operar", "Operate"),
    ("📬 Countrier", "Countier"),
    ("📩 Español", "LangSelect"),
    ("📤 Nosotros", "OurTeam"),
]
inline_keyboard.row(
    InlineKeyboardButton(inline_buttons[0][0], callback_data=inline_buttons[0][1]),
    InlineKeyboardButton(inline_buttons[1][0], callback_data=inline_buttons[1][1])
)
inline_keyboard.row(
    InlineKeyboardButton(inline_buttons[2][0], callback_data=inline_buttons[2][1]),
    InlineKeyboardButton(inline_buttons[3][0], callback_data=inline_buttons[3][1])
)

# Crear el teclado para el mensaje de contacto con el botón de volver
contact_keyboard = InlineKeyboardMarkup()
contact_keyboard.add(InlineKeyboardButton("🔙 Volver", callback_data="BackToMenu"))

# Definir un gestor de mensajes para los comandos /start y /help.
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        f"¡Hola {message.from_user.first_name}! Bienvenido a nuestro operador en línea. Para dudas y órdenes, presione los botones o use los comandos disponibles. Para más información, use /help.",
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

# Define el teclado para operaciones
operation_keyboard = InlineKeyboardMarkup()
operation_buttons = [
    ("💶 Arg", "Arg"),
    ("💶 Euro", "Euro"),
    ("💵 Dólar", "Dollar"),
    ("💵 Crypto", "Crypto"),
]
operation_keyboard.row(
    InlineKeyboardButton(operation_buttons[0][0], callback_data=operation_buttons[0][1]),
    InlineKeyboardButton(operation_buttons[1][0], callback_data=operation_buttons[1][1])
)
operation_keyboard.row(
    InlineKeyboardButton(operation_buttons[2][0], callback_data=operation_buttons[2][1]),
    InlineKeyboardButton(operation_buttons[3][0], callback_data=operation_buttons[3][1])
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
        reply_markup=contact_keyboard
    )

# Manejar los callbacks de los botones
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    callback_data = call.data

    if callback_data == "Operate":
        bot.send_message(call.message.chat.id, "Selecciona una opción para operar:", reply_markup=operation_keyboard)
        bot.answer_callback_query(call.id, "Operar seleccionado!")
    elif callback_data == "Countier":
        bot.answer_callback_query(call.id, "Countrier seleccionado!")
    elif callback_data == "LangSelect":
        bot.answer_callback_query(call.id, "Idioma seleccionado!")
    elif callback_data == "OurTeam":
        # Enviar la información de contacto al usuario con el botón de volver
        bot.send_message(
            call.message.chat.id,
            """
    Puedes contactarnos al siguiente número de teléfono: +123456789
    \n O visitarnos en nuestra tienda en la dirección: Calle Ficticia 123, Ciudad Ejemplo
    """,
            reply_markup=contact_keyboard
        )
        bot.answer_callback_query(call.id, "Información de contacto enviada!")
    elif callback_data == "BackToMenu":
        bot.send_message(call.message.chat.id, "Volviendo al menú principal.", reply_markup=inline_keyboard)
        bot.answer_callback_query(call.id, "Regresando al menú principal.")
    elif callback_data in ["Euro", "Arg", "Dollar", "Crypto"]:
        bot.answer_callback_query(call.id, f"{callback_data} seleccionado!")
    else:
        bot.answer_callback_query(call.id, "¡Acción desconocida!")

# Empezar a recibir mensajes
bot.polling()
