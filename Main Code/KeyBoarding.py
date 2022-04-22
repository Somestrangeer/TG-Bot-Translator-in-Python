import telebot

#---MAIN MENU---
keyboard2 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2.row('Start', "List of languages")
keyboard2.row('Select language')
keyboard2.row("Help")
