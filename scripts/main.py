from datetime import datetime
from win32con import VK_MEDIA_PLAY_PAUSE as play_button, VK_MEDIA_NEXT_TRACK as next_button, VK_MEDIA_PREV_TRACK as prev_button, VK_VOLUME_UP as vol_up, VK_VOLUME_DOWN as vol_down, KEYEVENTF_EXTENDEDKEY as ext_key
from telebot.types import Message
from winrt.windows.media.control import \
GlobalSystemMediaTransportControlsSessionManager as MediaManager


import telebot
import config
import time
import win32api
import threading
import asyncio

bot = telebot.TeleBot(config.token, parse_mode=None)
status = {0:'Нет открытых плееров',1:'Открыт плеер(ы)',2:'Переключение трека',3:'Остановлено',4:'Воспроизводится',5:'Приостановлено'}
failed = False

############## Функции ###################
def get_status():
    async def get_media_info():
        global failed
        try:
            sessions = await MediaManager.request_async()
            current_session = sessions.get_current_session()
            if current_session:
                info = current_session.get_playback_info()
                return info
            failed = False
            raise Exception('Невозможно получить сессию')
        except:
            failed = True
        asyncio.sleep(4)
    
    current_media_info = asyncio.run(get_media_info())    
    if failed == False:    
        return(current_media_info.playback_status)
    else:
        return(0)
def send_status(message):
    bot.send_message(message.chat.id, 'Текущий статус:\n"{}"'.format(status.get(get_status())))
def time_now():
    dt = datetime.now()
    return(dt.strftime("%D | %H:%M"))
##################################################################################################



try:
   bot.send_message(675474591, 'Бот запущен!\nВремя: {0}'.format(time_now()))
   print('Сообщение админу отправлено =)')
except:
    print('Бот не смог отправить приветствие')

if config.state == True:
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "{}, выбери действие)".format(message.chat.username))
        print('[{}]'.format(time_now()),message.chat.username,'здоровается с ботом!')
    
    
    @bot.message_handler(commands=['play'])
    def play_pause(message):
        win32api.keybd_event(play_button, 0, ext_key, 0)
        if get_status() == 4:
            bot.send_message(message.chat.id, 'Музыка запущена!')
        elif get_status() == 5:
            bot.send_message(message.chat.id, 'Музыка остановлена!')
        elif get_status() == 0:
            bot.send_message(message.chat.id, 'Нете запущенных плеров!')
        print('[{0}] {1} нажимает воспроизведение'.format(time_now(), message.chat.username))
    @bot.message_handler(commands=['next'])
    def next_track(message):
        win32api.keybd_event(next_button, 0, ext_key, 0)
        print('[{0}] {1} ставит следующий трек'.format(time_now(), message.chat.username))
    @bot.message_handler(commands=['prev'])
    def prev_track(message):
        win32api.keybd_event(prev_button, 0, ext_key, 0)
        print('[{0}] {1} возвращает предыдущий трек'.format(time_now(), message.chat.username))
    @bot.message_handler(commands=['info'])
    def prev_track(message):
        print('[{0}] {1} запросил информацию'.format(time_now(), message.chat.username))
        send_status(message)
    @bot.message_handler(content_types=['text'])
    def echo_messages(message: Message):
        text = message.text
        if message.text == 'Привет':
            bot.reply_to(message, "Кто ты?)")

        if text == 'Полина':
            config.easter_egg(bot, message)
            print('[{0}] {1} находит пасхалку!'.format(time_now(), message.chat.username))

        else:
            bot.send_message(message.chat.id, 'Может лучше ввёдешь /start?')    
    bot.polling(interval=0.5)
