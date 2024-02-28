from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import requests

# Define API endpoints (replace with your actual URLs)
API_BASE_URL = "https://flagshiptelegram.000webhostapp.com/api"
POINTS_ENDPOINT = "get_points_balance.php"
REFERRAL_STATS_ENDPOINT = "get_referee_stats"
VAULT_BALANCE_ENDPOINT = "get_vault_balance.php"

def get_user_profile_data(user_id):
    points_url = f"{API_BASE_URL}/{POINTS_ENDPOINT}?{user_id}"
    referral_stats_url = f"{API_BASE_URL}/{REFERRAL_STATS_ENDPOINT}?{user_id}"
    vault_balance_url = f"{API_BASE_URL}/{VAULT_BALANCE_ENDPOINT}?{user_id}"

    try:
        points_response = requests.get(points_url)
        if points_response.status_code == 200:
            points = points_response.json()["balance"]
        else:
            raise Exception(f"Error fetching points: {points_response.status_code}")

        referral_stats_response = requests.get(referral_stats_url)
        if referral_stats_response.status_code == 200:
            referral_stats = referral_stats_response.json()["referees"]
        else:
            raise Exception(f"Error fetching referral stats: {referral_stats_response.status_code}")

        vault_balance_response = requests.get(vault_balance_url)
        if vault_balance_response.status_code == 200:
            vault_balance = vault_balance_response.json()["balance"]
        else:
            raise Exception(f"Error fetching vault balance: {vault_balance_response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return None

    return {
        "points_balance": points,
        "referral_stats": referral_stats,
        "vault_balance": vault_balance
    }

def profile_stats_callback(update, context):
    user_id = update.effective_user.id
    profile_data = get_user_profile_data(user_id)

    if profile_data is None:
        return

    message = f"""
    * Points Balance: {profile_data['points_balance']}
    * Referral Stats: {profile_data['referral_stats']}
    * Vault Balance: {profile_data['vault_balance']}
    """

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def join_vault_callback(update, context):
    user_id = update.effective_user.id
    join_vault_url = "https://flagshipbetta24.000webhostapp.com/index.html?id=" + str(user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Click here to join the vault:", reply_markup=InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Join Vault", url=join_vault_url)
    ))

def start(update, context):
    # Get user's first name for personalization
    user_name = update.effective_user.first_name

    # Send a welcome message with a photo and buttons
    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo="https://example.com/welcome_image.jpg",  # URL of the welcome image
        caption=f"Hey {user_name}, welcome to a new world! Get ready to join other communities.",
        reply_markup=InlineKeyboardMarkup.from_button(
            InlineKeyboardButton("Profile Stats", callback_data="profile_stats"),
            InlineKeyboardButton("Join Vault", callback_data="join_vault")
        )
    )

def button_callback(update, context):
    query = update.callback_query
    query.answer()

    if query.data == "profile_stats":
        # Simulate the /profilestats command
        context.bot.dispatch_message(update.effective_user.id, '/profilestats')
    elif query.data == "join_vault":
        # Simulate the /joinvault command
        context.bot.dispatch_message(update.effective_user.id, '/joinvault')

def profilestats_command(update, context):
    profile_stats_callback(update, context)

def joinvault_command(update, context):
    user_id = update.effective_user.id
    join_vault_url = "https://flagshipbetta24.000webhostapp.com/index.html?id=" + str(user_id)
    message = "Get ready to join our vault:"
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=InlineKeyboardMarkup.from_button(
        InlineKeyboardButton("Join Vault", url=join_vault_url)
    ))

def main():
    updater = Updater(token='YOUR_TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('profilestats', profilestats_command))
    dp.add_handler(CommandHandler('joinvault', joinvault_command))
    dp.add_handler(CallbackQueryHandler(button_callback))

    updater.start_polling()
    updater.idle()

if _name_ == '_main_':
    main()