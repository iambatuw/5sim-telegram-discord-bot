# 5SIM Bot - Telegram & Discord

A powerful bot for Telegram and Discord that integrates with the 5SIM API to buy and manage virtual phone numbers for SMS verification.

## 📋 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [API Integration](#api-integration)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Features

- ✅ **Telegram Bot** - Full command support on Telegram
- ✅ **Discord Bot** - Full command support on Discord servers
- ✅ **5SIM API Integration** - Latest API endpoints (v1)
- ✅ **Automatic SMS Tracking** - Real-time SMS monitoring
- ✅ **Order Management** - Buy, cancel, finish, and check orders
- ✅ **Balance Checking** - View account balance and rating
- ✅ **Environment Configuration** - Secure token management with .env
- ✅ **Error Handling** - Comprehensive error messages
- ✅ **Async Support** - Non-blocking operations for better performance

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** - Download from [python.org](https://www.python.org/downloads/)
- **pip** - Python package manager (comes with Python)
- **Git** - For version control (optional but recommended)

### Verify Installation

```bash
# Check Python version
python --version

# Check pip version
pip --version
```

## 💾 Installation

### Step 1: Clone the Repository

```bash
# Using Git
git clone https://github.com/yourusername/5sim-telegram-bot.git
cd 5sim-telegram-bot

# Or download as ZIP and extract
```

### Step 2: Create Virtual Environment (Recommended)

Creating a virtual environment isolates project dependencies:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

### Required Packages

The `requirements.txt` includes:

- **requests** (2.31.0) - HTTP library for API calls
- **discord.py** (2.3.2) - Discord bot framework
- **python-telegram-bot** (20.3) - Telegram bot framework
- **python-dotenv** (1.0.0) - Environment variable management

## ⚙️ Configuration

### Step 1: Create .env File

Copy the example file and create your own:

```bash
cp .env.example .env
```

### Step 2: Get Your Tokens

#### Discord Token

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name
3. Go to "Bot" section and click "Add Bot"
4. Under "TOKEN", click "Copy" to copy your token
5. Paste it in `.env` as `DISCORD_TOKEN`

**Important:** Never share your Discord token!

#### Telegram Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Send `/newbot` command
3. Follow the prompts:
   - Enter bot name (e.g., "5SIM Bot")
   - Enter bot username (must end with "bot", e.g., "my5simbot")
4. Copy the token provided
5. Paste it in `.env` as `TELEGRAM_TOKEN`

#### 5SIM API Token

1. Visit [5SIM.net](https://5sim.net)
2. Create an account or log in
3. Go to [API Settings](https://5sim.net/settings/api)
4. Copy your API token
5. Paste it in `.env` as `API_TOKEN`

### Step 3: Configure .env File

Edit `.env` with your tokens:

```env
# Discord Bot Token
DISCORD_TOKEN=your-discord-token-here

# Telegram Bot Token
TELEGRAM_TOKEN=your-telegram-token-here

# 5SIM API Token
API_TOKEN=your-5sim-api-token-here
```

## 🎮 Usage

### Running Telegram Bot

```bash
python telegram_bot.py
```

Expected output:
```
🚀 Starting Telegram Bot...
✅ Telegram Bot Started
```

### Running Discord Bot

```bash
python discord_bot.py
```

Expected output:
```
🚀 Starting Discord Bot...
Discord Bot Connected: YourBotName
Bot ID: 123456789
```

### Running Both Bots Simultaneously

Open two terminal windows:

**Terminal 1:**
```bash
python telegram_bot.py
```

**Terminal 2:**
```bash
python discord_bot.py
```

## 📖 Commands

### Telegram Commands

All commands start with `/`:

| Command | Usage | Description |
|---------|-------|-------------|
| `/start` | `/start` | Welcome message and bot info |
| `/buy` | `/buy <country> <operator> <product>` | Buy a phone number |
| `/check` | `/check <order_id>` | Check order status and SMS |
| `/cancel` | `/cancel <order_id>` | Cancel an active order |
| `/finish` | `/finish <order_id>` | Mark order as completed |
| `/balance` | `/balance` | Check account balance and rating |
| `/help` | `/help` | Show all available commands |

### Discord Commands

All commands start with `.`:

| Command | Usage | Description |
|---------|-------|-------------|
| `.buy` | `.buy <country> <operator> <product>` | Buy a phone number |
| `.check` | `.check <order_id>` | Check order status and SMS |
| `.cancel` | `.cancel <order_id>` | Cancel an active order |
| `.finish` | `.finish <order_id>` | Mark order as completed |
| `.balance` | `.balance` | Check account balance and rating |
| `.help` | `.help` | Show all available commands |

### Command Examples

#### Telegram

```
/buy us tmobile google
/check 12345
/cancel 12345
/finish 12345
/balance
/help
```

#### Discord

```
.buy us tmobile google
.check 12345
.cancel 12345
.finish 12345
.balance
.help
```

## 🔌 API Integration

### 5SIM API Endpoints

The bot uses the following 5SIM API v1 endpoints:

#### User Profile
```
GET /user/profile
```
Returns user balance, email, and rating.

#### Buy Number
```
GET /user/buy/activation/{country}/{operator}/{product}
```
Purchases a phone number for SMS verification.

#### Check Order
```
GET /user/check/{order_id}
```
Retrieves order status and received SMS messages.

#### Cancel Order
```
GET /user/cancel/{order_id}
```
Cancels an active order and refunds the balance.

#### Finish Order
```
GET /user/finish/{order_id}
```
Marks an order as completed.

### API Response Format

All responses are in JSON format:

```json
{
  "id": 12345,
  "country": "us",
  "operator": "tmobile",
  "product": "google",
  "phone": "+1234567890",
  "price": 0.50,
  "status": "active",
  "created_at": "2024-01-01T12:00:00Z",
  "expires": "2024-01-01T12:15:00Z",
  "sms": [
    {
      "text": "123456",
      "received_at": "2024-01-01T12:05:00Z"
    }
  ]
}
```

## 🐛 Troubleshooting

### Bot Not Starting

**Problem:** `ModuleNotFoundError: No module named 'telegram'`

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Invalid Token Error

**Problem:** `Unauthorized` or `Invalid token`

**Solution:**
1. Verify token is correct in `.env`
2. Check for extra spaces or quotes
3. Regenerate token from bot settings
4. Ensure `.env` file is in the project root

### No SMS Received

**Problem:** Bot waits but no SMS arrives

**Solution:**
1. Check order status with `/check <order_id>`
2. Verify country/operator/product combination is valid
3. Check 5SIM account balance
4. Try a different operator or product

### Connection Timeout

**Problem:** `Connection timeout` or `Request timeout`

**Solution:**
1. Check internet connection
2. Verify API token is valid
3. Check 5SIM API status
4. Try again after a few seconds

### Discord Bot Not Responding

**Problem:** Bot is online but doesn't respond to commands

**Solution:**
1. Verify bot has message permissions in the server
2. Check bot role is above user roles
3. Ensure command prefix is `.` (dot)
4. Restart the bot

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the Troubleshooting section

## 🔗 Useful Links

- [5SIM API Documentation](https://5sim.net/docs)
- [Discord.py Documentation](https://discordpy.readthedocs.io/)
- [Python Telegram Bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Python Documentation](https://docs.python.org/3/)

---

**Last Updated:** 22.05.2026
**Version:** 1.0.0
