import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
import requests, json
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
  title = update.message.text
  res = requests.get('http://www.omdbapi.com/?t='+ title +'&apikey=aa2008f6')
  resp = json.loads(res.text)
 
  stringsR = """
  """
  strN = " "
  
  response = "" 
  if resp['Response'] == 'True':
    for i in resp['Ratings']:
      stringsR += f"{i['Source']} {i['Value']} \n"
    response = f"""
    {"Poster is not applicable" if resp['Poster'] == 'N/A' else resp['Poster']}
    
    {"Type is not applicable" if resp['Type'] == 'N/A' else 'Type-' + resp['Type']}
    
    {"Title are not applicable" if resp['Title'] == 'N/A' else 'Title-' + resp['Title']}
    
    {"Year is not applicable" if resp['Year'] == 'N/A' else 'Year-' + resp['Year']}
    
    {"Released are not applicable" if resp['Released'] == 'N/A' else 'Released Year-' + resp['Released']}
  
  {"Directors are not applicable" if resp['Director'] == 'N/A' else 'Directors-' + resp['Director']}
  
  {"Writers are not applicable" if resp['Writer'] == 'N/A' else 'Writers-' + resp['Writer']}
  
  {"Actors are not applicable" if resp['Actors'] == 'N/A' else 'Actors-' + resp['Actors']}
  
  {"Runtime is not applicable" if resp['Runtime'] == 'N/A' else 'Runtime-' + resp['Runtime']}
  
  {"Genre is not applicable" if resp['Genre'] == 'N/A' else 'Genre-' + resp['Genre']}
  
  {"Plot is not applicable" if resp['Plot'] == 'N/A' else 'Plot-' + resp['Plot']}
  
  {"Language is not applicable" if resp['Language'] == 'N/A' else 'Language-' + resp['Language']}
  
  {"Awards are not applicable" if resp['Awards'] == 'N/A' else 'Award-' + resp['Awards']}
  
{"Ratings are not applicable" if resp['Ratings'] == 'N/A' else stringsR }
  """
  else:
    response = "Doesn't Exist"
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response) 

if __name__ == '__main__':
    tokens = os.environ.get("TOKEN")
    application = ApplicationBuilder().token(tokens).build()
    movie_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), movie) 
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    application.add_handler(movie_handler)
    application.run_polling()