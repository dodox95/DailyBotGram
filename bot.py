import telebot
import time
import threading
import datetime
import pytz

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

active_chats = []

message_text = "Dobrego dnia i dużych zwrotów! 💸,\nŻyczy Wasz zaprzyjaźniony kantor https://www.cashify.eu/"

HOUR_TO_SEND = 8  # Godzina wysyłania wiadomości
MINUTE_TO_SEND = 00  # Minuta wysyłania wiadomości

# Zamiast odpowiadać na /start, dodajemy chat do listy
@bot.message_handler(commands=['yo', 'help'])
def add_to_active_chats(message):
    if message.chat.id not in active_chats:
        active_chats.append(message.chat.id)

def send_periodic_messages():
    message_sent_today = False
    while True:
        # Pobierz aktualny czas w strefie czasowej Polski
        now = datetime.datetime.now(pytz.timezone('Europe/Warsaw'))

        if now.hour == HOUR_TO_SEND and now.minute == MINUTE_TO_SEND and not message_sent_today:
            print(f"It's {HOUR_TO_SEND}:{MINUTE_TO_SEND}! Sending the message to all active chats.")
            for chat in active_chats:
                try:
                    bot.send_message(chat, message_text)
                    print(f"Message sent to chat {chat}.")
                except Exception as e:
                    print(f"Error sending message to chat {chat}: {e}")
            message_sent_today = True
            time.sleep(70)  # Czekaj trochę dłużej niż minutę, aby uniknąć wielokrotnego wysyłania wiadomości

        elif now.hour > HOUR_TO_SEND or (now.hour == HOUR_TO_SEND and now.minute > MINUTE_TO_SEND):
            message_sent_today = False

        time.sleep(50)  # Czekaj 50 sekund przed ponownym sprawdzeniem czasu

print("Bot starting...")
# Create a separate thread to send periodic messages
threading.Thread(target=send_periodic_messages, daemon=True).start()

bot.polling()
