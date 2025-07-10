import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Configuration
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHANNEL_USERNAME = "@yourchannel"  # Change to your channel username
GROUP_USERNAME = "@yourgroup"  # Change to your group username
TWITTER_USERNAME = "yourtwitter"  # Change to your Twitter username

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_message = f"""
    🚀 Welcome {user.first_name} to our Airdrop Bot! 🚀

    To participate in the airdrop, please complete these simple steps:
    """
    
    keyboard = [
        [InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("Join Group", url=f"https://t.me/{GROUP_USERNAME[1:]}")],
        [InlineKeyboardButton("Follow Twitter", url=f"https://twitter.com/{TWITTER_USERNAME}")],
        [InlineKeyboardButton("I've Completed All Steps ✅", callback_data="completed_steps")]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# Callback for completed steps
async def completed_steps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    await query.edit_message_text("""
    🎉 Great! You've completed all the steps.

    Now, please send your Solana wallet address where you'd like to receive your 10 SOL airdrop.
    
    Example: 7eY5vx5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5v5
    """)

# Handle wallet address submission
async def handle_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    wallet_address = update.message.text.strip()
    
    # Very basic validation (just checks length)
    if len(wallet_address) < 30 or len(wallet_address) > 60:
        await update.message.reply_text("⚠️ That doesn't look like a valid Solana wallet address. Please try again.")
        return
    
    # In a real bot, you would validate the address properly
    
    congrat_message = f"""
    🎊 Congratulations! 🎊

    You've successfully registered for our airdrop!
    
    Wallet: {wallet_address}
    Amount: 10 SOL
    
    Your tokens are on their way! (This is a simulation)
    
    Thank you for participating!
    """
    
    await update.message.reply_text(congrat_message)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"Update {update} caused error {context.error}")

def main():
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    
    # Callbacks
    app.add_handler(CallbackQueryHandler(completed_steps, pattern="completed_steps"))
    
    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_wallet))
    
    # Errors
    app.add_error_handler(error)
    
    # Start polling
    print("Polling...")
    app.run_polling(poll_interval=3)

if __name__ == "__main__":
    main()
