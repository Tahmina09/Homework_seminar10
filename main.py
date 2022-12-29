from aiogram import *
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from pytube import *
import os
from bot import dp,bot

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, 'Вас приветствует бот для скачивания видео и аудио с Youtube. Отправьте ссылку.')
    
@dp.message_handler()
async def text_message(message: types.Message):
    chat_id = message.chat.id
    url = message.text
    youtube = YouTube(url)
                
    if 'https://www.youtube.com/' or 'https://www.youtu.be/' in message:
        await bot.send_message(chat_id, f'Идёт загрузка видео: {youtube.title}\n'f'С канала: {youtube.author}\nС сылка на канал: {youtube.channel_url}')
    
    await bot.send_message(chat_id,'Чтобы скачать видео нажмите /video \
            \nЧтобы скачать аудио нажмите /audio\
                \nЧтобы вывести справку нажмите /help')
         
    get_text_messages(message)

@dp.message_handler()
async def get_text_messages(message):
    if message.text == '/video':
        await download_video(url, message, bot)
    elif message.text == '/audio':
        await download_audio(url, message, bot)
    elif message.text == '/help':
        await help_message(message)

@dp.message_handler(commands=['video'])
async def download_video(url, message, bot):
    chat_id = message.chat.id
    url = message.text
    youtube = YouTube(url)
    stream = youtube.streams.filter(progressive=True, file_extension='mp4')
    stream.get_highest_resolution().download('Downloading video', f'{chat_id}')
    with open(f'Downloading video\{chat_id}', 'rb') as video:
        await bot.send_video(chat_id, video, caption='Получите и распишитесь')
        os.remove(f'Downloading video\{chat_id}')


@dp.message_handler(commands=['audio'])
async def download_audio(url, message, bot):
    chat_id = message.chat.id
    url = message.text
    youtube = YouTube(url)
    stream = youtube.streams.filter(progressive=True, file_extension='mp3')
    stream.get_highest_resolution().download('Downloading audio', f'{chat_id}')
    with open(f'Downloading audio\{chat_id}', 'rb') as audio:
        await bot.send_video(chat_id, audio, caption='Получите и распишитесь')
        os.remove(f'Downloading audio\{chat_id}')
        
        
@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, '/start -> Запустить бота\n\
        /help -> Вывести справку\n \
        /video -> Скачать видео с Youtube\n\
            /audio -> Скачать аудио из видео Youtube') 

if __name__ == '__main__':
    executor.start_polling(dp)