import os
import asyncio
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from telegram.constants import ChatAction
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
API_BASE_URL = 'https://5sim.net/v1'
API_HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def get_user_profile():
    try:
        response = requests.get(f'{API_BASE_URL}/user/profile', headers=API_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def buy_number(country, operator, product):
    try:
        url = f'{API_BASE_URL}/user/buy/activation/{country}/{operator}/{product}'
        response = requests.get(url, headers=API_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def check_order(order_id):
    try:
        response = requests.get(f'{API_BASE_URL}/user/check/{order_id}', headers=API_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def cancel_order(order_id):
    try:
        response = requests.get(f'{API_BASE_URL}/user/cancel/{order_id}', headers=API_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


def finish_order(order_id):
    try:
        response = requests.get(f'{API_BASE_URL}/user/finish/{order_id}', headers=API_HEADERS)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None


async def telegram_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = """
🤖 Welcome to 5SIM Bot!

This bot helps you buy phone numbers for SMS verification.

Available commands:
/buy - Buy a phone number
/check - Check order status
/cancel - Cancel an order
/finish - Finish an order
/balance - Check account balance
/help - Show help message
    """
    await update.message.reply_text(welcome_text)


async def telegram_balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        
        profile = get_user_profile()
        
        if profile:
            balance_text = f"""
💰 **Account Balance**

Balance: `${profile['balance']}`
Email: `{profile['email']}`
Rating: ⭐ {profile['rating']}
            """
            await update.message.reply_text(balance_text, parse_mode='Markdown')
        else:
            await update.message.reply_text('❌ Could not fetch balance.')
    
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')


async def telegram_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📖 **5SIM Bot Commands**

/buy - Buy a phone number
/check - Check order status
/cancel - Cancel an order
/finish - Finish an order
/balance - Check account balance
/help - Show this message

**Example usage:**
/buy us tmobile google
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def telegram_buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 3:
            await update.message.reply_text(
                '❌ Usage: /buy <country> <operator> <product>\n\nExample: /buy us tmobile google'
            )
            return
        
        country = context.args[0]
        operator = context.args[1]
        product = context.args[2]
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        
        order_data = buy_number(country, operator, product)
        
        if order_data:
            created_at = datetime.fromisoformat(order_data['created_at'].replace('Z', '+00:00'))
            expires = datetime.fromisoformat(order_data['expires'].replace('Z', '+00:00'))
            time_remaining = (expires - created_at).total_seconds() / 60
            
            purchase_text = f"""
✅ **Number Purchased Successfully!**

Order ID: `{order_data['id']}`
Country: {order_data['country']}
Phone: `{order_data['phone']}`
Operator: {order_data['operator']}
Product: {order_data['product']}
Price: `${order_data['price']}`
Status: {order_data['status']}
Expires In: {int(time_remaining)} minutes

⏳ Waiting for SMS...
            """
            await update.message.reply_text(purchase_text, parse_mode='Markdown')
            
            order_id = order_data['id']
            max_attempts = 120
            attempt = 0
            
            while attempt < max_attempts:
                await asyncio.sleep(5)
                check_data = check_order(order_id)
                
                if check_data and len(check_data.get('sms', [])) > 0:
                    sms_message = check_data['sms'][0]['text']
                    
                    sms_text = f"""
📨 **SMS Received!**

Order ID: `{order_id}`
SMS Code: `{sms_message}`
Product: {check_data['product']}
Status: {check_data['status']}

✅ Use /finish {order_id} to complete the order
                    """
                    await update.message.reply_text(sms_text, parse_mode='Markdown')
                    break
                
                attempt += 1
            
            if attempt >= max_attempts:
                await update.message.reply_text(
                    f'⏱️ SMS Timeout\n\nNo SMS received within {max_attempts * 5} seconds.\nUse /cancel {order_id} to cancel.'
                )
        else:
            await update.message.reply_text('❌ Failed to purchase number. Check country/operator/product.')
    
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')


async def telegram_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text('❌ Usage: /check <order_id>')
            return
        
        order_id = context.args[0]
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        
        order_data = check_order(order_id)
        
        if order_data:
            sms_text = "No SMS yet"
            if order_data.get('sms') and len(order_data['sms']) > 0:
                sms_text = order_data['sms'][0]['text']
            
            check_text = f"""
📋 **Order Status: {order_id}**

Order ID: `{order_data['id']}`
Country: {order_data['country']}
Phone: `{order_data['phone']}`
Operator: {order_data['operator']}
Product: {order_data['product']}
Price: `${order_data['price']}`
Status: {order_data['status']}
SMS: `{sms_text}`
            """
            await update.message.reply_text(check_text, parse_mode='Markdown')
        else:
            await update.message.reply_text('❌ Order not found.')
    
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')


async def telegram_cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text('❌ Usage: /cancel <order_id>')
            return
        
        order_id = context.args[0]
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        
        order_data = cancel_order(order_id)
        
        if order_data:
            cancel_text = f"""
🚫 **Order Canceled**

Order ID: `{order_data['id']}`
Country: {order_data['country']}
Phone: `{order_data['phone']}`
Price: `${order_data['price']}`
Status: {order_data['status']}

Order has been successfully canceled.
            """
            await update.message.reply_text(cancel_text, parse_mode='Markdown')
        else:
            await update.message.reply_text('❌ Order not found or cannot be canceled.')
    
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')


async def telegram_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if len(context.args) < 1:
            await update.message.reply_text('❌ Usage: /finish <order_id>')
            return
        
        order_id = context.args[0]
        
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
        
        order_data = finish_order(order_id)
        
        if order_data:
            finish_text = f"""
✅ **Order Finished**

Order ID: `{order_data['id']}`
Country: {order_data['country']}
Phone: `{order_data['phone']}`
Price: `${order_data['price']}`
Status: {order_data['status']}

Order has been successfully completed.
            """
            await update.message.reply_text(finish_text, parse_mode='Markdown')
        else:
            await update.message.reply_text('❌ Order not found or cannot be finished.')
    
    except Exception as e:
        await update.message.reply_text(f'❌ Error: {str(e)}')


async def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler('start', telegram_start))
    app.add_handler(CommandHandler('help', telegram_help))
    app.add_handler(CommandHandler('balance', telegram_balance))
    app.add_handler(CommandHandler('buy', telegram_buy))
    app.add_handler(CommandHandler('check', telegram_check))
    app.add_handler(CommandHandler('cancel', telegram_cancel))
    app.add_handler(CommandHandler('finish', telegram_finish))
    
    async with app:
        await app.start()
        print("✅ Telegram Bot Started")
        await app.updater.start_polling()


if __name__ == '__main__':
    print("🚀 Starting Telegram Bot...")
    asyncio.run(main())