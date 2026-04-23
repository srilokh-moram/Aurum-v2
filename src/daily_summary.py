import MetaTrader5 as mt5
from datetime import datetime, timedelta
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# ================= CONFIG =================
SYMBOL = os.getenv("SYMBOL")

TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
WHATSAPP_FROM = "whatsapp:+14155238886"

# 👉 Add multiple recipients (comma-separated in .env)
RECIPIENTS = os.getenv("WHATSAPP_TO_LIST", "").split(",")

MT5_LOGIN = int(os.getenv("MT5_LOGIN"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD")
MT5_SERVER = os.getenv("MT5_SERVER")

# ================= CONNECT =================
if not mt5.initialize(login=MT5_LOGIN, password=MT5_PASSWORD, server=MT5_SERVER):
    print("MT5 connection failed")
    quit()

# ================= TIME RANGE =================
now = datetime.now()
start_of_day = datetime(now.year, now.month, now.day)

# ================= TODAY DEALS =================
deals_today = mt5.history_deals_get(start_of_day, now)

today_profit = 0
today_count = 0

if deals_today:
    for d in deals_today:
        if d.entry == 1:  # closed trades
            today_profit += d.profit
            today_count += 1

# ================= TOTAL PROFIT =================
all_deals = mt5.history_deals_get(datetime(2000, 1, 1), now)

total_profit = 0
if all_deals:
    for d in all_deals:
        if d.entry == 1:
            total_profit += d.profit

# ================= OPEN POSITIONS =================
positions = mt5.positions_get()

open_count = 0
floating_pl = 0

if positions:
    open_count = len(positions)
    floating_pl = sum(p.profit for p in positions)

# ================= MESSAGE =================
msg = f"""
📊 Trading Summary – {SYMBOL}

Date: {now.strftime('%Y-%m-%d')}

Deals Today: {today_count}
Profit Today: ${round(today_profit, 2)}
Total Profit: ${round(total_profit, 2)}

Open Positions: {open_count}
Floating P/L: ${round(floating_pl, 2)}
"""

# ================= SEND WHATSAPP =================
client = Client(TWILIO_SID, TWILIO_TOKEN)

for number in RECIPIENTS:
    number = number.strip()
    if not number:
        continue

    try:
        message = client.messages.create(
            body=msg,
            from_=WHATSAPP_FROM,
            to=f"whatsapp:{number}"
        )
        print(f"Message sent to {number}: {message.sid}")
    except Exception as e:
        print(f"Failed to send to {number}: {e}")

mt5.shutdown()