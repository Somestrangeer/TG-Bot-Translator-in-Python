import telebot

#---MAIN MENU---
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Старт', "Список языков")
keyboard2.row('Выбор языка')
keyboard2.row("Помощь")