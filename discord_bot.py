import os
import discord
import asyncio
import requests
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
API_TOKEN = os.getenv('API_TOKEN')
API_BASE_URL = 'https://5sim.net/v1'
API_HEADERS = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='.', case_insensitive=True, intents=intents)
bot.remove_command('help')


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


@bot.event
async def on_ready():
    print(f'Discord Bot Connected: {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.listening, name='5sim.net')
    )


@bot.command(name='buy')
async def discord_buy(ctx, country: str, operator: str, product: str):
    try:
        await ctx.send(f"🔄 Buying number for {country}/{operator}/{product}...")
        
        order_data = buy_number(country, operator, product)
        
        if order_data:
            created_at = datetime.fromisoformat(order_data['created_at'].replace('Z', '+00:00'))
            expires = datetime.fromisoformat(order_data['expires'].replace('Z', '+00:00'))
            time_remaining = (expires - created_at).total_seconds() / 60
            
            embed = discord.Embed(
                title='✅ Number Purchased Successfully!',
                color=discord.Color.green(),
                description=f"""
**Order ID:** `{order_data['id']}`
**Country:** {order_data['country']}
**Phone Number:** `{order_data['phone']}`
**Operator:** {order_data['operator']}
**Product:** {order_data['product']}
**Price:** ${order_data['price']}
**Status:** {order_data['status']}
**Expires In:** {int(time_remaining)} minutes

⏳ Waiting for SMS...
                """
            )
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
            
            order_id = order_data['id']
            max_attempts = 120
            attempt = 0
            
            while attempt < max_attempts:
                await asyncio.sleep(5)
                check_data = check_order(order_id)
                
                if check_data and len(check_data.get('sms', [])) > 0:
                    sms_message = check_data['sms'][0]['text']
                    
                    sms_embed = discord.Embed(
                        title='📨 SMS Received!',
                        color=discord.Color.blue(),
                        description=f"""
**Order ID:** `{order_id}`
**SMS Code:** `{sms_message}`
**Product:** {check_data['product']}
**Status:** {check_data['status']}

✅ Use `.finish {order_id}` to complete the order
                        """
                    )
                    sms_embed.timestamp = datetime.utcnow()
                    await ctx.send(f"{ctx.author.mention}", embed=sms_embed)
                    break
                
                attempt += 1
            
            if attempt >= max_attempts:
                timeout_embed = discord.Embed(
                    title='⏱️ SMS Timeout',
                    color=discord.Color.red(),
                    description=f"No SMS received within {max_attempts * 5} seconds. Use `.cancel {order_id}` to cancel."
                )
                await ctx.send(embed=timeout_embed)
        else:
            error_embed = discord.Embed(
                title='❌ Error',
                color=discord.Color.red(),
                description='Failed to purchase number. Check country/operator/product.'
            )
            await ctx.send(embed=error_embed)
    
    except Exception as e:
        error_embed = discord.Embed(
            title='❌ Error',
            color=discord.Color.red(),
            description=f'{str(e)}'
        )
        await ctx.send(embed=error_embed)


@bot.command(name='check')
async def discord_check(ctx, order_id: str):
    try:
        order_data = check_order(order_id)
        
        if order_data:
            sms_text = "No SMS yet"
            if order_data.get('sms') and len(order_data['sms']) > 0:
                sms_text = order_data['sms'][0]['text']
            
            embed = discord.Embed(
                title=f'📋 Order Status: {order_id}',
                color=discord.Color.blue(),
                description=f"""
**Order ID:** `{order_data['id']}`
**Country:** {order_data['country']}
**Phone Number:** `{order_data['phone']}`
**Operator:** {order_data['operator']}
**Product:** {order_data['product']}
**Price:** ${order_data['price']}
**Status:** {order_data['status']}
**SMS:** `{sms_text}`
                """
            )
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            error_embed = discord.Embed(
                title='❌ Error',
                color=discord.Color.red(),
                description='Order not found.'
            )
            await ctx.send(embed=error_embed)
    
    except Exception as e:
        error_embed = discord.Embed(
            title='❌ Error',
            color=discord.Color.red(),
            description=f'{str(e)}'
        )
        await ctx.send(embed=error_embed)


@bot.command(name='cancel')
async def discord_cancel(ctx, order_id: str):
    try:
        order_data = cancel_order(order_id)
        
        if order_data:
            embed = discord.Embed(
                title='🚫 Order Canceled',
                color=discord.Color.red(),
                description=f"""
**Order ID:** `{order_data['id']}`
**Country:** {order_data['country']}
**Phone Number:** `{order_data['phone']}`
**Price:** ${order_data['price']}
**Status:** {order_data['status']}

Order has been successfully canceled.
                """
            )
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            error_embed = discord.Embed(
                title='❌ Error',
                color=discord.Color.red(),
                description='Order not found or cannot be canceled.'
            )
            await ctx.send(embed=error_embed)
    
    except Exception as e:
        error_embed = discord.Embed(
            title='❌ Error',
            color=discord.Color.red(),
            description=f'{str(e)}'
        )
        await ctx.send(embed=error_embed)


@bot.command(name='finish')
async def discord_finish(ctx, order_id: str):
    try:
        order_data = finish_order(order_id)
        
        if order_data:
            embed = discord.Embed(
                title='✅ Order Finished',
                color=discord.Color.green(),
                description=f"""
**Order ID:** `{order_data['id']}`
**Country:** {order_data['country']}
**Phone Number:** `{order_data['phone']}`
**Price:** ${order_data['price']}
**Status:** {order_data['status']}

Order has been successfully completed.
                """
            )
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            error_embed = discord.Embed(
                title='❌ Error',
                color=discord.Color.red(),
                description='Order not found or cannot be finished.'
            )
            await ctx.send(embed=error_embed)
    
    except Exception as e:
        error_embed = discord.Embed(
            title='❌ Error',
            color=discord.Color.red(),
            description=f'{str(e)}'
        )
        await ctx.send(embed=error_embed)


@bot.command(name='balance')
async def discord_balance(ctx):
    try:
        profile = get_user_profile()
        
        if profile:
            embed = discord.Embed(
                title='💰 Account Balance',
                color=discord.Color.gold(),
                description=f"""
**Balance:** ${profile['balance']}
**Email:** {profile['email']}
**Rating:** ⭐ {profile['rating']}
                """
            )
            embed.timestamp = datetime.utcnow()
            await ctx.send(embed=embed)
        else:
            error_embed = discord.Embed(
                title='❌ Error',
                color=discord.Color.red(),
                description='Could not fetch balance.'
            )
            await ctx.send(embed=error_embed)
    
    except Exception as e:
        error_embed = discord.Embed(
            title='❌ Error',
            color=discord.Color.red(),
            description=f'{str(e)}'
        )
        await ctx.send(embed=error_embed)


@bot.command(name='help')
async def discord_help(ctx):
    embed = discord.Embed(
        title='📖 5SIM Bot Commands',
        color=discord.Color.blue(),
        description="""
**.buy <country> <operator> <product>** - Buy a phone number
**.check <order_id>** - Check order status
**.cancel <order_id>** - Cancel an order
**.finish <order_id>** - Finish an order
**.balance** - Check account balance
**.help** - Show this message

**Example:** `.buy us tmobile google`
        """
    )
    embed.timestamp = datetime.utcnow()
    await ctx.send(embed=embed)


if __name__ == '__main__':
    print("🚀 Starting Discord Bot...")
    bot.run(DISCORD_TOKEN)