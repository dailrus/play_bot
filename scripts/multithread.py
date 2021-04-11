from datetime import datetime
from win32con import VK_MEDIA_PLAY_PAUSE as play_button, VK_MEDIA_NEXT_TRACK as next_button, VK_MEDIA_PREV_TRACK as prev_button, VK_VOLUME_UP as vol_up, VK_VOLUME_DOWN as vol_down, KEYEVENTF_EXTENDEDKEY as ext_key
from typing import Text
from telebot.types import Message
import telebot
import config
import time
import win32api
import threading
dt = datetime.now()
time_now = dt.strftime("%D | %H:%M")

time_update = threading.Thread
def bot_update(time_now):
    
    bot = telebot.TeleBot(config.token, parse_mode=None)
    
    try:
        bot.send_message(675474591, 'Бот запущен!\nВремя: {0}'.format(dt.strftime("%H:%M")))
        print('Сообщение админу отправлено =)')
    except:
        print('Бот не смог отправить приветствие')
   
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        bot.reply_to(message, "{}, выбери действие)".format(message.chat.username))
        print('[{}]'.format(time_now),message.chat.username,'здоровается с ботом!')
    
    
    @bot.message_handler(commands=['play'])
    def play_pause(message):
        win32api.keybd_event(play_button, 0, ext_key, 0)
        print('[{0}] {1} нажимает воспроизведение'.format(time_now, message.chat.username))
    @bot.message_handler(commands=['next'])
    def next_track(message):
        win32api.keybd_event(next_button, 0, ext_key, 0)
        print('[{0}] {1} ставит следующий трек'.format(time_now, message.chat.username))
    @bot.message_handler(commands=['prev'])
    def prev_track(message):
        win32api.keybd_event(prev_button, 0, ext_key, 0)
        print('[{0}] {1} возвращает предыдущий трек'.format(time_now, message.chat.username))
    
    @bot.message_handler(content_types=['text'])
    def echo_messages(message: Message):
        text = message.text
        if message.text == 'Привет':
            bot.reply_to(message, "Кто ты?)")

        if text == 'Полина':
            config.easter_egg(bot, message)
            print('[{0}] {1} находит пасхалку!'.format(time_now, message.chat.username))

        else:
            bot.send_message(message.chat.id, 'Может лучше ввёдешь /start?')    
    bot.polling(interval=0.5)
def time_update()