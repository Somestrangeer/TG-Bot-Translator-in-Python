import telebot
from list_langs import LANGUAGES


def choose_lang(message):
    global flatten #declaring a variable with language keys (list)
    global flatten1 #declaring a variable with language names (list)
    global jjj #declare the variable amount of languages as ​​global (can be used everywhere in our code)
    d = LANGUAGES #in variable 'd' I asign the dict variableLANGUAGES
    button_demo = [] #create the list of buttons
    b = [] #the list for keys
    bb = [] #the list for values
    for k, v in d.items():#through the loop I get a key(k) and a value(v), passing the dict
        a = k
        b.append(a)
        s = v
        bb.append(s)
    flatten = [str(sub) for sub in b] #iterate through the list of keys and convert them to a string (each element)
    flatten1 = [str(sub) for sub in bb]#the same, but of valuse (value is the name of language like Englisch)
    jjj = len(flatten) #I count the amount of languages
    i = 0 #this and the next are the indexes that we will operate on during the loop
    ii = 1
    for ix in range(int(jjj/2)): #divide the number by two, converting to a number
    	#in list 'butto' I place inlines. 
    	#text=f"{flatten1[i]}".capitalize() - I take the values by indexes
    	#callback_data=f'{flatten[i]}' - callback. When you click on the button, the program receives the language key
    	#by clicking on Russian, the program receives ru. The index of the language name is the same as the index of the key
        butto = [
        telebot.types.InlineKeyboardButton(text=f"{flatten1[i]}".capitalize(), callback_data=f'{flatten[i]}'),
        telebot.types.InlineKeyboardButton(text=f"{flatten1[ii]}".capitalize(), callback_data=f'{flatten[ii]}')
            ]
        i += 2 #each time I increase indexes by 2.
        ii += 2
        button_demo.append(butto)#I list I place our buttons(2 buttons in one lisy, which means button_demo is a nested list) each time.

        #further condition. If the number of lists (in one it has 2 buttons) in the list is equal to 8, then->
        #i create the list b, in which, with the same method, I place the number
        #This is a language selection. Button 1 is the first language selection list and 2 is the second selection list. There are 6 in total.
        if len(button_demo) == 8:
            b = [telebot.types.InlineKeyboardButton(text=f"1", callback_data=f'1'),
                 telebot.types.InlineKeyboardButton(text=f"2", callback_data=f'2'),
                 telebot.types.InlineKeyboardButton(text=f"3", callback_data=f'3'),
                 telebot.types.InlineKeyboardButton(text=f"4", callback_data=f'4'),
                 telebot.types.InlineKeyboardButton(text=f"5", callback_data=f'5'),
                 telebot.types.InlineKeyboardButton(text=f"6", callback_data=f'6')]
            button_demo.append(b)
            break #terminate the loop with 'break'
    #in the markup, I put the keyboard, in which I put our list of language and number buttons for the select of pages (it's better to call it as page, yes)
    markup = telebot.types.InlineKeyboardMarkup(button_demo) 
    #The bot sends a message, where our markup already comes out, that is, a full-fledged menu for selecting a language
    bot.send_message(message.chat.id, text='Выберите язык:', reply_markup=markup)


    