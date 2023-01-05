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
        await bot.send_message(chat_id,'Чтобы скачать видео нажмите /video \
            \nЧтобы скачать аудио нажмите /audio\
                \nЧтобы вывести справку нажмите /help \
                    \nЧтобы начать нажмите /start')


@dp.message_handler(commands=['video'])
async def download_video(url, message, bot):
    await bot.send_message(chat_id, f'Идёт загрузка видео: {youtube.title}\n'f'С канала: {youtube.author}\nСсылка на канал: {youtube.channel_url}')
    chat_id = message.chat.id
    url = message.text
    youtube = YouTube(url)
    stream = youtube.streams.filter(progressive= True, file_extension='mp4')
    stream.get_highest_resolution().download('Downloading video', f'{youtube.title}')
    with open(f'Downloading video\{youtube.title}', 'rb') as video:
        await bot.send_video(chat_id, video, caption='Получите и распишитесь')
        os.remove(f'Downloading video\{youtube.title}')


@dp.message_handler(commands=['audio'])
async def download_audio(url, message, bot):
    await bot.send_message(chat_id, f'Идёт загрузка аудио: {youtube.title}\n'f'С канала: {youtube.author}\nСсылка на канал: {youtube.channel_url}')
    chat_id = message.chat.id
    url = message.text
    youtube = YouTube(url)
    stream = youtube.streams.filter(only_audio=True)
    stream.get_audio_only().download('Downloading audio', f'{youtube.title}')
    with open(f'Downloading audio\{youtube.title}', 'rb') as audio:
        await bot.send_audio(chat_id, audio, caption='Получите и распишитесь')
        os.remove(f'Downloading audio\{youtube.title}')
        
        
@dp.message_handler(commands=['help'])
async def help_message(message: types.Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id, '/start -> Запустить бота\n\
        /help -> Вывести справку\n \
        /video -> Скачать видео с Youtube\n\
            /audio -> Скачать аудио из видео Youtube') 

if __name__ == '__main__':
    executor.start_polling(dp)