import telebot #install the pyTelegramBotAPI library and import
import os #to delete audiofiles
import  KeyBoarding as navv #import the python file that contains the buttons so as not to pollute the code
from list_langs import LANGUAGES #import the python file, where there's the list of available languages ​​is located
import requests
import subprocess #to convert audio ogg into wav
import speech_recognition as sr #recognition the speech
from gtts import gTTS #text voice acting
token = '-' #bot works thanks to token
KeyAPI = '-' #API key for translator work
folder_id = '-' #id of the folder with the project in Yandex cloud
bot = telebot.TeleBot(token) #declaring a class
@bot.message_handler(commands=['start'])
#-----------------------------------------------------------
def start(message):
    bot.send_message(message.chat.id, 'Welcome to Telegram Translator!\n'
                                    '\n'
                                    'What can this bot do??\n'
                                      '\n'
                                      '🈳 It can translate a text from any language to any other language\n'
                                      '\n'
                                      '📳 It can recognise a voice message and convert into text(it works with only Russian)\n'
                                      '\n'
                                      '⚛ It can voice a foreign language for better perception\n'
                                      '\n'
                                      '*And the most important, it is extremely fast and convenient to use.*\n'
                                      '\n'
                                      '\n'
                                    'If you do not understand anything, just click on the *"Help"* button.',
                     reply_markup=navv.keyboard2, parse_mode="Markdown")
                      # in reply_markup we pass a variable from navv,
                      # in which the buttons are placed (the keyboard)
#--------------List-------------------------------
@bot.message_handler(commands=['list']) 
def list_lan(message):
    LANGUAGES_TEXT = "*LANGUAGES*\n" #title
    count = [] #create an empty list to count the number of languages
    for language in LANGUAGES: #loop through the keys in the dictionary (list of languages ​​in the list_langs file, LANGUAGES variable)
        count.append(language) #I add keys (ru, en, de...) to the list

        #I add lines to the variable with the title. It works like this: I refer to the dictionary by the index of the key obtained in the cycle {LANGUAGES[language]
        #and then I insert the {language} key itself. The output is something like: English --> en or a more explicit example
        #{LANGUAGES[en or ru].capitalize()}_ --> {en or ru}

        LANGUAGES_TEXT += f"_\n{LANGUAGES[language].capitalize()}_ --> {language}"
    bot.send_message(message.chat.id, text=f'{LANGUAGES_TEXT}\n' #passing a variable with a ready list to the message
                                           f'\n'
                                           f'*Количество языков*: {len(count)}', parse_mode="Markdown") #parse_mode="Markdown" для шрифта
                              #*авав* - bold text, а  _апвв_ - cursiv
#------------------Help--------------------
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text="*-->Commands<--*\n"
                                           "\n"
                                           "/languages -> to get the lif of supported languages.\n"
                                                  "/choose -> to choose tha target language.\n"
                                                  '/start -> to return in "Start".\n'
                                                  '/help -> to get the introductory information.\n'
                                                  '/111 -> manual selection of langauge.\n'
                                                  '*Example:* /111 Franch\n'
                                                  '\n'
                                                  '\n'
                                                  '_Translation from any language into any other language is enabled by default_', parse_mode="Markdown")
#---------------------------Selection. 1st page----------------------------------------------
@bot.message_handler(commands=['choose'])
def choose_lang(message):
    global flatten #declaring a variable with language keys (list)
    global flatten1 #declaring a variable with language names (list)
    global jjj #declare the variable amount of languages as ​​global (can be used everywhere in our code)
    d = LANGUAGES #in variable 'd' I asign the dict variableLANGUAGES
    button_demo = [] #create the list of buttons
    b = [] #the list for keys
    bb = [] #the list for values
    for k, v in d.items(): #through the loop I get a key(k) and a value(v), passing the dict
        a = k
        b.append(a)
        s = v
        bb.append(s)
    flatten = [str(sub) for sub in b] #iterate through the list of keys and convert them to a string (each element)
    flatten1 = [str(sub) for sub in bb] #the same, but of valuse (value is the name of language like Englisch)
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
#---------------------------Selection. 2nd page----------------------------------------------
#Everything here is identical to the previous and following such functions, I only change
#the indexing of the beginning of the sorting by the list, according to our page capacity    
@bot.message_handler(commands=['choose2'])
def choose_lang2(message):
    i = 16
    ii = 17
    button_demo = []
    for ix in range(int(jjj/2)):
        butto = [
        telebot.types.InlineKeyboardButton(text=f"{flatten1[i]}".capitalize(), callback_data=f'{flatten[i]}'),
        telebot.types.InlineKeyboardButton(text=f"{flatten1[ii]}".capitalize(), callback_data=f'{flatten[ii]}')
            ]
        i += 2
        ii += 2
        button_demo.append(butto)
        if len(button_demo) == 8:
            b = [telebot.types.InlineKeyboardButton(text=f"1", callback_data=f'1'),
                 telebot.types.InlineKeyboardButton(text=f"2", callback_data=f'2'),
                 telebot.types.InlineKeyboardButton(text=f"3", callback_data=f'3'),
                 telebot.types.InlineKeyboardButton(text=f"4", callback_data=f'4'),
                 telebot.types.InlineKeyboardButton(text=f"5", callback_data=f'5'),
                 telebot.types.InlineKeyboardButton(text=f"6", callback_data=f'6')]
            button_demo.append(b)
            break
    markup = telebot.types.InlineKeyboardMarkup(button_demo)
    bot.send_message(message.chat.id, text='Choose the language:', reply_markup=markup)
#---------------------------Selection. 3 page----------------------------------------------
def choose_lang3(message):
    i = 32
    ii = 33
    button_demo = []
    for ix in range(int(jjj/2)):
        butto = [
        telebot.types.InlineKeyboardButton(text=f"{flatten1[i]}".capitalize(), callback_data=f'{flatten[i]}'),
        telebot.types.InlineKeyboardButton(text=f"{flatten1[ii]}".capitalize(), callback_data=f'{flatten[ii]}')
            ]
        i += 2
        ii += 2
        button_demo.append(butto)
        if len(button_demo) == 8:
            b = [telebot.types.InlineKeyboardButton(text=f"1", callback_data=f'1'),
                 telebot.types.InlineKeyboardButton(text=f"2", callback_data=f'2'),
                 telebot.types.InlineKeyboardButton(text=f"3", callback_data=f'3'),
                 telebot.types.InlineKeyboardButton(text=f"4", callback_data=f'4'),
                 telebot.types.InlineKeyboardButton(text=f"5", callback_data=f'5'),
                 telebot.types.InlineKeyboardButton(text=f"6", callback_data=f'6')]
            button_demo.append(b)
            break
    markup = telebot.types.InlineKeyboardMarkup(button_demo)
    bot.send_message(message.chat.id, text='Choose the language:', reply_markup=markup)
#---------------------------Selection. 4 page----------------------------------------------
def choose_lang4(message):
    i = 48
    ii = 49
    button_demo = []
    for ix in range(int(jjj/2)):
        butto = [
        telebot.types.InlineKeyboardButton(text=f"{flatten1[i]}".capitalize(), callback_data=f'{flatten[i]}'),
        telebot.types.InlineKeyboardButton(text=f"{flatten1[ii]}".capitalize(), callback_data=f'{flatten[ii]}')
            ]
        i += 2
        ii += 2
        button_demo.append(butto)
        if len(button_demo) == 8:
            b = [telebot.types.InlineKeyboardButton(text=f"1", callback_data=f'1'),
                 telebot.types.InlineKeyboardButton(text=f"2", callback_data=f'2'),
                 telebot.types.InlineKeyboardButton(text=f"3", callback_data=f'3'),
                 telebot.types.InlineKeyboardButton(text=f"4", callback_data=f'4'),
                 telebot.types.InlineKeyboardButton(text=f"5", callback_data=f'5'),
                 telebot.types.InlineKeyboardButton(text=f"6", callback_data=f'6')]
            button_demo.append(b)
            break
    markup = telebot.types.InlineKeyboardMarkup(button_demo)
    bot.send_message(message.chat.id, text='Choose the language:', reply_markup=markup)
#---------------------------Selection. 5 page----------------------------------------------
def choose_lang5(message):
    i = 64
    ii = 65
    button_demo = []
    for ix in range(int(jjj/2)):
        butto = [
        telebot.types.InlineKeyboardButton(text=f"{flatten1[i]}".capitalize(), callback_data=f'{flatten[i]}'),
        telebot.types.InlineKeyboardButton(text=f"{flatten1[ii]}".capitalize(), callback_data=f'{flatten[ii]}')
            ]
        i += 2
        ii += 2
        button_demo.append(butto)
        if len(button_demo) == 8:
            b = [telebot.types.InlineKeyboardButton(text=f"1", callback_data=f'1'),
                 telebot.types.InlineKeyboardButton(text=f"2", callback_data=f'2'),
                 telebot.types.InlineKeyboardButton(text=f"3", callback_data=f'3'),
                 telebot.types.InlineKeyboardButton(text=f"4", callback_data=f'4'),
                 telebot.types.InlineKeyboardButton(text=f"5", callback_data=f'5'),
                 telebot.types.InlineKeyboardButton(text=f"6", callback_data=f'6')]
            button_demo.append(b)
            break
    markup = telebot.types.InlineKeyboardMarkup(button_demo)
    bot.send_message(message.chat.id, text='Choose the language:', reply_markup=markup)
#---------------------------Selection. 6 page----------------------------------------------
def choose_lang6(message):
    i = 80
    ii = 81
    button_demo = []
    for ix in range(int(jjj/2)):
        butto = [
        telebot.types.InlineKeyboardButton(text=f"{flatten1[i]}".capitalize(), callback_data=f'{flatten[i]}'),
        telebot.types.InlineKeyboardButton(text=f"{flatten1[ii]}".capitalize(), callback_data=f'{flatten[ii]}')
            ]
        i += 2
        ii += 2
        button_demo.append(butto)
        if len(button_demo) == 4:
            b = [telebot.types.InlineKeyboardButton(text=f"1", callback_data=f'1'),
                 telebot.types.InlineKeyboardButton(text=f"2", callback_data=f'2'),
                 telebot.types.InlineKeyboardButton(text=f"3", callback_data=f'3'),
                 telebot.types.InlineKeyboardButton(text=f"4", callback_data=f'4'),
                 telebot.types.InlineKeyboardButton(text=f"5", callback_data=f'5'),
                 telebot.types.InlineKeyboardButton(text=f"6", callback_data=f'6')]
            button_demo.append(b)
            break
    markup = telebot.types.InlineKeyboardMarkup(button_demo)
    bot.send_message(message.chat.id, text='Choose the language:', reply_markup=markup)
#-------------------------------Query_handler--------------------------------------------------------------
#query_handler performs processing of received data
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global q #global variable with language key
    global qq #global variable with page number
    #here and after - checking through a condition. Если полученное значение будет 1, 2, 3...
    #then we put this value in the qq variable and delete the last message from the bot,
    #the choice of language and do a redirect (flipping) to the function with which we have changed the numbering
    #in simple terms - if you click on 1, the program will process it and transfer you to the choose_lang2(call.message) function
    if call.data == '1':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang(call.message)
        return
    elif call.data == '2':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang2(call.message)
        return
    elif call.data == '3':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang3(call.message)
        return
    elif call.data == '4':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang4(call.message)
        return
    elif call.data == '5':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang5(call.message)
        return
    elif call.data == '6':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang6(call.message)
        return
    #if you clicked not on the buttons 1, 2, 3.., but on the language, then the bot also deletes its last message
    #and passes the language key stored in callback_data for processing
    #and passes this key to the variable q
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(callback_query_id=call.id, text='❗❗❗Язык выбран - ' + (call.data).capitalize() + '❗❗❗')
        q = call.data
#-------------------------------Voice--------------------------------------------------------
#in this function we process Voice Message(vm)
@bot.message_handler(content_types=['voice'])
def repeat_all_message(message):

  #if VM is sent, then we put it into the file_info variable and get the file itself for future download
  #in variable 'file', using requests, with the data transfer 'get',
  #we'r going to starting a download process. 
  #Create the file 'new_voice.ogg'(288) and open it for writing down, writing file.content there

  file_info = bot.get_file(message.voice.file_id)
  file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
  with open('new_voice.ogg','wb') as f:
    f.write(file.content)
  src_filename = 'new_voice.ogg'#place downloaded VM, in format ogg, in variable
  dest_filename = 'output.wav' #place the future title of audio in var
  process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename]) #converting file ogg into wav
  if process.returncode != 0: #if we get an error, then the user receives a message about this and is redirected to the error_message() function
      bot.send_message(message.chat.id, text="Голосовое сообщение не распознано.")
      error_message(message)
      return
  r = sr.Recognizer() #creating the class of recognition
  will_convert = sr.AudioFile('output.wav') #prefering
  with will_convert as source: #it converts VM into text
      audio = r.record(source)
  try:#trying to avoid possible mistakes. We put the prepared file into recognition, indicating the language
      converted_soundfile = r.recognize_google(audio, language='ru-RU')
  except:
      os.remove('output.wav')#if there is an error, then delete all audio files
      os.remove('new_voice.ogg')
      error_message(message)#and redirect to function with an error message
      return
  #the bot sends a recognized message
  bot.send_message(message.chat.id, text="*Оригинал.*\n"
                                         f"\n"
                                         f"{converted_soundfile}.", parse_mode="Markdown")
  os.remove('output.wav')
  os.remove('new_voice.ogg')#delete all files
  #trying to transfer to the process_of_translation(),
  #passing the recognized text and the previously selected language, but if no language was selected, then an error will be generated,
  #and to eliminate it, I wrap everything in a try, giving the language as English
  try:
      process_of_translation(message, f'{converted_soundfile}', q)
  except:
      process_of_translation(message, f'{converted_soundfile}','en')

#------------------------TRANSLATION----------------------------------------------------------
#In this function we place the procces of translating, using Yandex API
#Also we use gTTS to get the pronouncing

def process_of_translation(message, text, q):
    target = q #assign the language
    #work with Yandex API. in the body dictionary I put the text and the language 
    #to which I need to translate and the ID of the folder with the project
    body = {
        "targetLanguageCode": target,
        "texts": text, 
        "folderId": folder_id,
    }
    #pass API key
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Api-Key {0}".format(KeyAPI)
    }
    #here we send the prepared data through the requests, using the post method, and put back
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    str_dict = response.text #get the response text
    done_dict = eval(str_dict) #convert str into dict type
    qq = LANGUAGES1.get(target) #get the value by key
    #in resulting dict, I need to filter out everything superfluous. I turn to the dict and then to its key ['translations']
    #the to the array, in which there's another dict, at index 0, and already to the key 'text, where we'll get our main text
    bot.send_message(message.chat.id, text=f"*Translated in {qq}.*\n"
                                           f"\n"
                                           f"{done_dict['translations'][0]['text'].replace('&#39;', '')}.", parse_mode="Markdown")
    #Here we make the pronouncing audiofile. I wrap it in try to prevent errors
    #it tts I turn to the gTTs lib, inserting the translated text and selecting the language I need
    #I save the audio as pronouncing.ogg
    #send to a user an audiofile
    #terminate the proces
    try:
        tts = gTTS(f" {done_dict['translations'][0]['text'].replace('&#39;', '')}", lang=f'{target}')
        tts.save('pronouncing.ogg')
        audio = open(r'pronouncing.ogg', 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
        os.remove('pronouncing.ogg')
    except ValueError:
        bot.send_message(message.chat.id, text='Language playback is not supported.')
#----------------------------Error--------------------------------------------------------------------------------
# for correctness, I redirect here in case of a similar error
def error_message(message):
    bot.send_message(message.chat.id, text="The voice message is not recognised.")
#-----------------------------All------------------------------------------------------------------------------------
#all messages go here
@bot.message_handler()
def any_message(message):
    global q #selected language
    text = message.text #wrap
    list_of_cut = '/111' #command if the user enters the language himself
    if text == 'Start':
        start(message)
        return
    elif text == 'List of languages':
        list_lan(message)
        return
    elif text == 'Select language':
        choose_lang(message)
        return
    elif text == 'Help':
        help(message)
        return
    elif text[0] in list_of_cut[0] and text[1] in list_of_cut[1] and text[2] in list_of_cut[2]:
      #everything that starts with /111 goes here...
      #q will put the language
        q = ''
        new_list = text.split()#split the text to make a list right there and then
        try:
            new1 = new_list[1].capitalize()#select the element at index 1, there is always a language
        except:
            new1 = new_list[0]
        if new1 in LANGUAGES1.values(): #check: if our element at index 1 is in the values ​​of the LANGUAGES dictionary, then we go further
            for k, v in LANGUAGES1.items():
                if v == new1: #if value = our element, then...
                    q = k #assign
                    bot.send_message(message.chat.id, text='The language is chosen - ' + (q).capitalize())
                    return
        else:
            bot.send_message(message.chat.id, "The language, like that, does not exist.")
            return
    else: #if the user has not entered any of this, then
        try:#wrapping in try, we are redirected to func for translation (explained above)
            process_of_translation(message, text, q)
        except:
            process_of_translation(message, text, 'en')
print('WE WORK')
bot.polling() #turn on the bot
