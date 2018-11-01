import matplotlib
matplotlib.use('Agg')
import pylab
from pylab import rcParams
import matplotlib.pyplot as plt
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import pandas as pd
from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
from io import BytesIO
import os

yf.pdr_override()

def start(bot, update):
  update.message.reply_text("Hai, yuk cek record stocks pilihanmu. \n Caranya ketik /help dulu ya")

def helps(bot, update):
  update.message.reply_text("Caranya: <Simbol perusahaan> <tgl mulai> <tgl selesai> \n Format tanggalnya YYYY-MM-DD")
  
def get_stock(bot, update):
  update.message.reply_text("Sedang diproses, mohon ditunggu...")
  idchat = update['message']['chat']['id']
  text = update['message']['text']
  texts = text.split(" ")
  if (len(texts) == 3):
    s = texts[1]
    e = texts[2]
    data = pdr.get_data_yahoo(texts[0], start=s, end=e)
    close = data['Close']
    all_weekdays = pd.date_range(start=s, end=e, freq='B')
    close = close.reindex(all_weekdays)
    fig = plt.figure(figsize=(15,8))
    ax = fig.add_subplot(111)
    plt.ylabel('Close Price')
    plt.xlabel('Date')
    plt.title("Close Price Stocks: "+str(texts[0]))
    # buffer = BytesIO()
    ax.plot(close.index,close)
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    bot.send_photo(idchat, photo=buffer)
  elif (len(texts) == 4):
    get_stock_multi(bot, update)

def get_stock_multi(bot, update):
  idchat = update['message']['chat']['id']
  text = update['message']['text']
  texts = text.split(" ")
  s = texts[2]
  e = texts[3]
  print("get")
  data1 = pdr.get_data_yahoo(texts[0], start=s, end=e)
  data2 = pdr.get_data_yahoo(texts[1], start=s, end=e)
  close1 = data1['Close']
  close2 = data2['Close']
  all_weekdays = pd.date_range(start=s, end=e, freq='B')
  close1 = close1.reindex(all_weekdays)
  close2 = close2.reindex(all_weekdays)
  fig = plt.figure(figsize=(15,8))
  ax = fig.add_subplot(111)
  plt.ylabel('Close Price')
  plt.xlabel('Date')
  plt.title("Close Price Stocks: "+str(texts[0])+" & "+str(texts[1]))
  ax.plot(close1.index,close1,'r')
  ax.plot(close2.index,close2,'b')
  ax.legend([texts[0], texts[1]])
  buffer = BytesIO()
  fig.savefig(buffer, format='png')
  buffer.seek(0)
  print("get")
  bot.send_photo(idchat, photo=buffer)

def main():
  # Create Updater object and attach dispatcher to it
  TOKEN = "781975723:AAEIsAhOsFRnlGOwbVJJY9nTwWGgSw7-Pc8"
  PORT = int(os.environ.get('PORT','5000'))
  updater = Updater(TOKEN)
  updater.start_webhook(listen="0.0.0.0",
                    port = PORT,
                    url_path=TOKEN)
  dispatcher = updater.dispatcher
  print("Bot started")

  # Add command handler to dispatcher
  start_handler = CommandHandler('start',start)
  help_handler = CommandHandler('help',helps)
  stock_case = MessageHandler(Filters.text, get_stock)
  dispatcher.add_handler(start_handler)
  dispatcher.add_handler(stock_case)
  dispatcher.add_handler(help_handler)

  # Start the bot
  updater.bot.set_webhook("https://still-bastion-47471.herokuapp.com/"+TOKEN)
  updater.idle()
  # updater.start_polling()

  # Run the bot until you press Ctrl-C
  # updater.idle()

if __name__ == '__main__':
  main()
