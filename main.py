import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv

load_dotenv()

# Initialize bot with Telegram token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Remove webhook for local testing
bot.remove_webhook()

# Conversion rates (relative to Arg)
rates = {
    'Arg': 1,               # Peso Argentino como base
    'Dollar': 1 / 1400,     # 1 Peso Argentino a Dólares
    'Euro': 1 / 1500,       # 1 Peso Argentino a Euros
    'Crypto': 1 / 1355,     # 1 Peso Argentino a Cripto
    'Usd_to_Arg': 1400,     # Factor de conversión de Dólares a Pesos
    'Euro_to_Arg': 1500,    # Factor de conversión de Euros a Pesos
    'Crypto_to_Arg': 1355   # Factor de conversión de Cripto a Pesos
}

# Main inline keyboard
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

# Contact keyboard
contact_keyboard = InlineKeyboardMarkup()
contact_keyboard.add(InlineKeyboardButton("🔙 Volver", callback_data="BackToMenu"))

# Create operation keyboard excluding the selected currency
def create_operation_keyboard(exclude_currency):
    currencies = ["Arg", "Euro", "Dollar", "Crypto"]
    remaining_currencies = [currency for currency in currencies if currency != exclude_currency]
    
    keyboard = InlineKeyboardMarkup()

    # Add buttons for remaining currencies
    for currency in remaining_currencies:
        keyboard.add(InlineKeyboardButton(f"💶 {currency}", callback_data=currency))
    
    return keyboard

# Dictionary to store user data
user_data = {}

# Handle /start and /help commands
@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    bot.reply_to(
        message,
        f"¡Hola {message.from_user.first_name}! Bienvenido a nuestro operador en línea. Para dudas y órdenes, presione los botones o use los comandos disponibles. Para más información, use /help.",
        reply_markup=inline_keyboard
    )

# Handle /hours command
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

# Handle /contact command
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

# Handle callback queries
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    callback_data = call.data
    user_id = call.from_user.id

    if callback_data == "Operate":
        bot.send_message(call.message.chat.id, "Selecciona una opción para operar:", reply_markup=create_operation_keyboard(None))
        bot.answer_callback_query(call.id, "Operar seleccionado!")
    elif callback_data in ["Arg", "Euro", "Dollar", "Crypto"]:
        if "selected_currency" not in user_data.get(user_id, {}):
            # User selects the base currency
            user_data[user_id] = {"selected_currency": callback_data}
            bot.send_message(call.message.chat.id, "Por favor, ingresa el monto que deseas cambiar:")
        else:
            # User selects the target currency
            user_data[user_id]["target_currency"] = callback_data
            selected_currency = user_data[user_id]["selected_currency"]
            target_currency = user_data[user_id]["target_currency"]
            amount = user_data[user_id]["amount"]

            # Perform the conversion
            if selected_currency == "Arg":
                # De Arg a otra moneda
                result = amount * rates[target_currency]
            elif target_currency == "Arg":
                # De otra moneda a Arg
                result = amount * rates[f'{selected_currency}_to_Arg']
            else:
                # De una moneda a otra (indirect conversion)
                result = amount * (rates[f'{selected_currency}_to_Arg']) * rates[target_currency]

            # Show result
            bot.send_message(
                call.message.chat.id,
                f"Usted desea cambiar {selected_currency} {amount} por {target_currency}: {result:.2f}"
            )
            # Clear user data after conversion
            user_data.pop(user_id, None)
    elif callback_data == "Countier":
        bot.answer_callback_query(call.id, "Countrier seleccionado!")
    elif callback_data == "LangSelect":
        bot.answer_callback_query(call.id, "Idioma seleccionado!")
    elif callback_data == "OurTeam":
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
        bot.send_message(
            call.message.chat.id,  
            f"¡Hola {call.from_user.first_name}! Bienvenido a nuestro operador en línea. Para dudas y órdenes, presione los botones o use los comandos disponibles. Para más información, use /help.", 
            reply_markup=inline_keyboard
        )
        bot.answer_callback_query(call.id, "Regresando al menú principal.")
    else:
        bot.answer_callback_query(call.id, "¡Acción desconocida!")

# Handle amount input
@bot.message_handler(func=lambda message: message.from_user.id in user_data and "selected_currency" in user_data[message.from_user.id] and "amount" not in user_data[message.from_user.id])
def handle_amount(message):
    user_id = message.from_user.id

    try:
        amount = float(message.text)
        user_data[user_id]["amount"] = amount

        user_currency = user_data[user_id]["selected_currency"]
        keyboard = create_operation_keyboard(user_currency)
        
        bot.send_message(
            message.chat.id,
            f"Usted desea cambiar {user_currency} {amount} por:",
            reply_markup=keyboard
        )
    except ValueError:
        bot.send_message(message.chat.id, "Por favor, ingresa un monto válido.")

# Start polling
bot.polling()
