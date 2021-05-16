
from datetime import datetime
from telebot.apihelper import get_sticker_set
from win32con import VK_MEDIA_PLAY_PAUSE as play_button, VK_MEDIA_NEXT_TRACK as next_button, VK_MEDIA_PREV_TRACK as prev_button, VK_VOLUME_UP as vol_up, VK_VOLUME_DOWN as vol_down, KEYEVENTF_EXTENDEDKEY as ext_key
from telebot import types
from telebot.types import Message
from winrt.windows.media.control import \
GlobalSystemMediaTransportControlsSessionManager as MediaManager

import os
import sys
import telebot
import config
import time
import win32api
import asyncio



#logging.warning('This will get logged to a file')

bot = telebot.TeleBot(config.token, parse_mode=None)
status_dict = {0:'❌ Нет открытых плееров',1:'Открыт плеер(ы)',2:'Переключение трека',3:'Остановлено',4:'▶️ Воспроизводится',5:'⏸ Приостановлено'}
failed = False


############## Функции и другая куча кода ###################
def get_status():
    async def get_playback_status():
        sessions = await MediaManager.request_async()
        current_session = sessions.get_current_session()
        if current_session:
            status = current_session.get_playback_info()
            return status
    func = asyncio.run(get_playback_status())
    return func.playback_status
current_volume = '"Work in Progress"'
def get_info():
    async def get_media_info():
        sessions = await MediaManager.request_async()
        current_session = sessions.get_current_session()
        if current_session:  # there needs to be a media session running
            info = await current_session.try_get_media_properties_async()
            info_dict = {song_attr: info.__getattribute__(song_attr) for song_attr in dir(info) if song_attr[0] != '_'}
            return info_dict
    return asyncio.run(get_media_info())
def send_status(message):
    status = get_status()
    artist = get_info().get('artist')
    title = get_info().get('title')
    if status == 4 or status == 5:
        bot.send_message(message.chat.id, '{0}\n🎵 {1} - {2}'.format(status_dict.get(status),artist,title))
    else:
        bot.send_message(message.chat.id, 'Нет открытых плееров')
def time_now():
    dt = datetime.now()
    return(dt.strftime("%D | %H:%M"))
def try_play():
    async def play():
        sessions = await MediaManager.request_async()
        current_session = sessions.get_current_session()
        if current_session:
            reply = await current_session.try_play_async()
    asyncio.run(play())
def try_pause():
    async def pause():
        sessions = await MediaManager.request_async()
        current_session = sessions.get_current_session()
        if current_session:
            reply = await current_session.try_pause_async()
    asyncio.run(pause())
markup = types.ReplyKeyboardMarkup()
btn_play = types.KeyboardButton('▶️ Play')
btn_pause = types.KeyboardButton('⏸ Pause')
btn_next = types.KeyboardButton('⏭')
btn_prev = types.KeyboardButton('⏮')
btn_up = types.KeyboardButton('🔊')
btn_down = types.KeyboardButton('🔉')
markup.row(btn_play, btn_pause)
markup.row(btn_prev, btn_down, btn_up, btn_next)




###################################################################################################



try:
   bot.send_message(675474591, 'Бот запущен!\n[{0}]'.format(time_now()))
   print('[{}] Бот запущен'.format(time_now()))
except:
    print('Бот не смог отправить приветствие')

if config.state == True:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "{}, выбери действие".format(message.chat.username), reply_markup = markup)
        print('[{}]'.format(time_now()),message.chat.username,'здоровается с ботом!')
    
    
    @bot.message_handler(commands=['play'])
    def play(message):
        try_play()
        #win32api.keybd_event(play_button, 0, ext_key, 0)
        time.sleep(0.5)
        if get_status() == 4:
            bot.send_message(message.chat.id, 'Музыка запущена!')
        elif get_status() == 5:
            bot.send_message(message.chat.id, 'Музыка остановлена!')
        elif get_status() == 0:
            bot.send_message(message.chat.id, 'Нет открытых плееров')
        print('[{0}] {1} нажимает воспроизведение'.format(time_now(), message.chat.username))
    @bot.message_handler(commands=['pause'])
    def pause(message):
        try_pause()
        #win32api.keybd_event(play_button, 0, ext_key, 0)
        time.sleep(0.5)
        if get_status() == 4:
            bot.send_message(message.chat.id, 'Музыка запущена!')
        elif get_status() == 5:
            bot.send_message(message.chat.id, 'Музыка остановлена!')
        elif get_status() == 0:
            bot.send_message(message.chat.id, 'Нет открытых плееров')
        print('[{0}] {1} нажимает паузу'.format(time_now(), message.chat.username))
    @bot.message_handler(commands=['next'])
    def next_track(message):
        win32api.keybd_event(next_button, 0, ext_key, 0)
        time.sleep(1)
        bot.send_message(message.chat.id, 'Трек переключен вперёд!\n🎵 {0} - {1}'.format(get_info().get('artist'),get_info().get('title')))
        print('[{0}] {1} ставит следующий трек'.format(time_now(), message.chat.username))
    @bot.message_handler(commands=['volup'])
    def volume_up(message):
        try:
            count = int(message.text.split(' ')[1])
        except:
            count = 2
        
        for i in range (1, int(count/2)+1):
            win32api.keybd_event(vol_up, 0, ext_key, 0)
            time.sleep(0.1)
        bot.send_message(message.chat.id, '🔊 Громкость прибавлена!')
        print('[{0}] {1} прибавил громкость'.format(time_now(), message.chat.username))
    @bot.message_handler(commands=['voldown'])
    def volume_down(message):
        try:
            count = int(message.text.split(' ')[1])
        except:
            count = 2
        for i in range (1, int(count/2)+1):
            win32api.keybd_event(vol_down, 0, ext_key, 0)
            time.sleep(0.1)
        bot.send_message(message.chat.id, '🔉 Громкость убавлена!')
        print('[{0}] {1} убавил громкость'.format(time_now(), message.chat.username))
    
    @bot.message_handler(commands=['prev'])
    def prev_track(message):
        win32api.keybd_event(prev_button, 0, ext_key, 0)
        prev = get_info().get('title')
        time.sleep(0.7)
        if get_info().get('title') == prev:
            bot.send_message(message.chat.id, 'Трек перемонтан в начало!')
        else:
            bot.send_message(message.chat.id, 'Трек переключен назад!\n🎵 {0} - {1}'.format(get_info().get('artist'),get_info().get('title')))
        print('[{0}] {1} возвращает предыдущий трек'.format(time_now(), message.chat.username))
    
    @bot.message_handler(commands=['info'])
    def info_get(message):
        print('[{0}] {1} запросил информацию'.format(time_now(), message.chat.username))
        send_status(message)
     
    @bot.message_handler(commands=['restart'])
    def restart(message):
        os.execl('/scripts/main.py', '','')   
    
    @bot.message_handler(content_types=['text'])
    def echo_messages(message: Message):
        text = message.text
        if message.text == '▶️ Play':
            play(message)
        if message.text == '⏸ Pause':
            pause(message)
        if message.text == '🔊':
            volume_up(message)
        if message.text == '🔉':
            volume_down(message)
        if message.text == '⏭':
            next_track(message)
        if message.text == '⏮':
            prev_track(message)        
        if message.text == 'Привет':
            bot.reply_to(message, "Кто ты?)")

        if text == config.easter_trigger:
            config.easter_egg(bot, message)
            print('[{0}] {1} нашёл пасхалку!'.format(time_now(), message.chat.username))    
    bot.polling()
