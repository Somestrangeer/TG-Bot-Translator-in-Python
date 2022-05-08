import telebot #устанавливаем библиотеку pyTelegramBotAPI и имортируем
import os #для удаления аудиофайлов
import  KeyBoarding_in_ru as navv #имортируем файл python, в котором находятся кнопки, чтобы не загрязнять код
from ru_list_langs import LANGUAGES #импортируем файл питон, где находится список доступных языков
import requests
import subprocess #для конвертации аудио ogg в wav
import speech_recognition as sr #распознавание речи
from gtts import gTTS #озвучка текста
token = '-' #бот работает благодяр нему, токену
KeyAPI = '-' #ключ API для работы переводчика
folder_id = '-' #ид папки с проектом в яндекс клауд
bot = telebot.TeleBot(token) #объявляю класс
#------------------------Старт----------------------
@bot.message_handler(commands=['start']) #объявляем команду старт
def start(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в телеграм-переводчик!\n'
                                    '\n'
                                    'Что может этот бот?\n'
                                      '\n'
                                      '🈳 Переводить текст с любого языка на любой другой язык\n'
                                      '\n'
                                      '📳 Переводить ГС в текст\n'
                                      '\n'
                                      '⚛ Озвучивать иностранный язык для лучшего восприятия\n'
                                      '\n'
                                      '*А главное - крайне быстр и удобен в использовании.*\n'
                                      '\n'
                                      '\n'
                                    'Если вы что-либо не поняли, то просто кликните на кнопку *"Помощь"*.',
                     reply_markup=navv.keyboard2, parse_mode="Markdown") #в reply_markup мы передаём переменную из navv,
    																	 #в которой находятся кнопки, то есть клавиатура
#--------------Список-------------------------------
@bot.message_handler(commands=['list']) #объявляю команду лист
def list_lan(message):
    LANGUAGES_TEXT = "*LANGUAGES*\n" #загаловок
    count = [] #создаю пустой список для счёта кол-ва языков
    for language in LANGUAGES: #иду циклом по ключам в словаре (список ящыков в файле while2, переменная LANGUAGES)
        count.append(language) #Добавляю ключи (ru, en, de...) в список
        #в переменную с заголовком добавляю строки. Работает так: обращаюсь к слвоарю по индексу полученного в цикле ключа {LANGUAGES[language]
        #и после вставляю сам ключ {language}. На выходе что-то вроде: Английский --> en  или более явный пример
        #{LANGUAGES[en or ru].capitalize()}_ --> {en or ru}
        LANGUAGES_TEXT += f"_\n{LANGUAGES[language].capitalize()}_ --> {language}"
    bot.send_message(message.chat.id, text=f'{LANGUAGES_TEXT}\n' #передаю в сообщение переменную с готовым списком
                                           f'\n'
                                           f'*Количество языков*: {len(count)}', parse_mode="Markdown") #parse_mode="Markdown" для шрифта
    													#*авав* - жирный текст, а  _апвв_ - курсив
#------------------Команда помощи--------------------
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, text="*-->КОМАНДЫ<--*\n"
                                           "\n"
                                           "/languages -> получить список доступных языков.\n"
                                                  "/choose -> Выбор языка.\n"
                                                  '/start -> Вернуться в "старт".\n'
                                                  '/help -> Получить ознакомительную информацию.\n'
                                                  '\n'
                                                  '_По умолчанию включён перевод с любого языка на английский_', parse_mode="Markdown")
#---------------------------Выбор языка-Фундамент-Первая страница----------------------------------------------
@bot.message_handler(commands=['choose']) #объявляю команду выбора, самое важное здесь
def choose_lang(message, nn, mm):
    global flatten #бъявляю переменную с ключами языков
    global flatten1 #бъявляю переменную с названиями языков
    global jjj #объявляю переменную кол-ва языков глобальной(можно использовать всюду в нашем коде)
    d = LANGUAGES #переменной d присваиваю перменную словаря LANGUAGES
    button_demo = [] #создаю список для кнопок
    b = [] #список для ключей
    bb = [] #список для значений
    for k, v in d.items():#через цикл поулчаю ключ(k) и значение v, проходясь по словарю
        a = k
        b.append(a)
        s = v
        bb.append(s)
    flatten = [str(sub) for sub in b] #прохожусь по списку из ключей и преобразую их в строку(каждый элемент)
    flatten1 = [str(sub) for sub in bb]#то же самое, но со значениями (значение - просто название языка)
    jjj = len(flatten) #делаю подсчёт кол-ва языков
    i = nn #это и next - индексы, которыми мы будеи оперировать при цикле
    ii = mm
    for ix in range(int(jjj/2)): #делю кол-во на два, преобразуя в число
    	#в список butto помещаю инлайн кнопки. 
    	#text=f"{flatten1[i]}".capitalize() - беру значения(название языка) по индексу
    	#callback_data=f'{flatten[i]}' - обратная связь. При нажатии на кнопку, программа получает ключ языка
    	#то есть нажав на Русский, программа получает ru. Индекс названия языка совпадает с индексом ключа
        butto = [
        telebot.types.InlineKeyboardButton(text=f"{flatten1[i]}".capitalize(), callback_data=f'{flatten[i]}'),
        telebot.types.InlineKeyboardButton(text=f"{flatten1[ii]}".capitalize(), callback_data=f'{flatten[ii]}')
            ]
        i += 2 #каждый раз увеличиваю индек на 2.
        ii += 2
        button_demo.append(butto)#помещаю в список наши кнопки(2 кнопки в одном спсике, а значит button_demo - вложенный список) каждый раз
        #далее условие. Если кол-во списокв(в одном 2 кнопки) в списке ровняется 8, то...
        #я создаю список b, в который тем же методом помещаю уже чиисла
        #это пермещение по выбору языков. кнопка 1 - первый список выбора языков, а 2 - вторйо список выбора. Всего их 6.
        if len(button_demo) == 8:
            b = [telebot.types.InlineKeyboardButton(text=f"1", callback_data=f'1'),
                 telebot.types.InlineKeyboardButton(text=f"2", callback_data=f'2'),
                 telebot.types.InlineKeyboardButton(text=f"3", callback_data=f'3'),
                 telebot.types.InlineKeyboardButton(text=f"4", callback_data=f'4'),
                 telebot.types.InlineKeyboardButton(text=f"5", callback_data=f'5'),
                 telebot.types.InlineKeyboardButton(text=f"6", callback_data=f'6')]
            button_demo.append(b)
            break #завершаю цикл через break для безопасности
    #в маркап я помещаю клавиатуру, в которую помещаю наш список из кнопок языка и чисел по выбору страниц(лучше назвать эток ак старнциа, да)
    markup = telebot.types.InlineKeyboardMarkup(button_demo) 
    #бот присылает сообщение, где выходит уже наш маркап, то есть полноценное меню по выбору языка
    bot.send_message(message.chat.id, text='Выберите язык:', reply_markup=markup)
#-------------------------------Шестая страница--------------------------------------------------------
def choose_lang6(message, nn, mm):
    i = nn
    ii = mm
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
    bot.send_message(message.chat.id, text='Выберите язык:', reply_markup=markup)
#-------------------------------Обработчик запроса с кнопок Инлайн(выбор языка)--------------------------------------------------------
#query_handler совершает обработку полученных данных
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    global q #глобальная перменная с ключом языка
    global qq #глобальная перемнная с номером страницы
    #здесь и после - проверка через условие. Если полученное значение будет 1, 2, 3...
    #то мы в перемнную qq помещаем это значеие и удаляем последнее сооб9щение от бота,
    #то есть выбор яызка и делаем редирект(перелистывание) на функциию, которой мы преровняли нумерацию
    #простым языком - если ты нажмёшь на 1, то программа обработает это и перенесёт тебя на функцию choose_lang2(call.message)
    #а если будет 5, то choose_lang5(call.message)
    if call.data == '1':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang(call.message, 0, 1)
        return
    elif call.data == '2':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang(call.message, 16, 17)
        return
    elif call.data == '3':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang(call.message, 32, 33)
        return
    elif call.data == '4':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang(call.message, 48, 49)
        return
    elif call.data == '5':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang(call.message, 64, 65)
        return
    elif call.data == '6':
        qq = call.data
        bot.delete_message(call.message.chat.id, call.message.message_id)
        choose_lang6(call.message, 80, 81)
        return
    #если ты нажал не на кнопки 1, 2, 3.., а на язык, то бот так же удаляет последнее своё сообщение
    #и и передаёт на обработку ключ языка, хранящийся в callback_data
    #и в перменную q передаёт этот ключ
    else:
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.answer_callback_query(callback_query_id=call.id, text='❗❗❗Язык выбран - ' + (call.data).capitalize() + '❗❗❗')
        q = call.data
#-------------------------------Обработчик голосовых сообщений--------------------------------------------------------
# в это функции мы обрабатываем гс
@bot.message_handler(content_types=['voice'])
def repeat_all_message(message):
	#если отправлено гс , то в переменную file_info помещаем то, что отправил пользователь и получаю сам фал для будщего скачивания
	#а в file мы через рекуаэст, с помощью передачи данных get,
	#начинаем процесс скачивания. Создаю файл new_voice.ogg(288 строка) и открываю его на запись, записывая туда file.content
  file_info = bot.get_file(message.voice.file_id)
  file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))
  with open('new_voice.ogg','wb') as f:
    f.write(file.content)
  src_filename = 'new_voice.ogg'#помещаю скачанное голосове в формате ogg в переменную
  dest_filename = 'output.wav' #помещаю будущее название аудиофайла в переменную
  process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename]) #конвертирую файл ogg в wav
  if process.returncode != 0: #если ошибка, то пользователь получает об этом сообщение и переадрессовывается на ф-ию error_message()
      bot.send_message(message.chat.id, text="Голосовое сообщение не распознано.")
      error_message(message)
      return
  r = sr.Recognizer() #создаю класс распознавания
  will_convert = sr.AudioFile('output.wav') #подготавливаю
  with will_convert as source: #идёт перевод гс в текст
      audio = r.record(source)
  try:#пытаюст избежать возможных ошибок. Подготовленный файл мы помещаем в распознавание, указывая язык
      converted_soundfile = r.recognize_google(audio, language='ru-RU')
  except:
      os.remove('output.wav')#если будет ошибка, то удаляем все аудиофайлы
      os.remove('new_voice.ogg')
      error_message(message)#и перенаправляем во ф-ию с сообщением об ошибке
      return
  #бот присылает распознанное сообщение
  bot.send_message(message.chat.id, text="*Оригинал.*\n"
                                         f"\n"
                                         f"{converted_soundfile}.", parse_mode="Markdown")
  os.remove('output.wav')
  os.remove('new_voice.ogg')#удаляем все файлы
  # пытаемся перенестись во ф-ию process_of_translation(),
  #передавая распознанный текст и выбранный до этого языка, но если не был выбран язык, то убдет ошибка,
  #и дял её устарнения оборачиваю всё в try, давая язык как английский
  try:
      process_of_translation(message, f'{converted_soundfile}', q)
  except:
      process_of_translation(message, f'{converted_soundfile}','en')

#-------------------------------Перевод и принятие команд(ответ на все слова)--------------------------------------------------------
def process_of_translation(message, text, q):
    target = q #присваиваю переданный язык
    #идёт работа с api yandex. в словарь боди помещаю текст, яызк на который нужно перевести и айди папки с проектом
    #на яндекс клауд
    body = {
        "targetLanguageCode": target,
        "texts": text,
        "folderId": folder_id,
    }
    #перадю апи ключ
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {0}".format(KeyAPI)
    }
    #тут мы через рекуаэст, методом пост, отпраляем подготовленные данные и поулчем назад
    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                             json=body,
                             headers=headers
                             )
    str_dict = response.text #поулчаю ответ(перевод)
    done_dict = eval(str_dict)#так как ответ приходит в виде строки(там словарь в виде строки), то через eval я делаю его обратно в слвоарь
    qq = LANGUAGES.get(target)#через уже полученный ранее ключ языка, я простоп олучаю значение, чттобы пользователь мог видеть, на какой язфк был совершён перевод
    #в полученном словаре, мне нужно отсеить всё лишнее. Обращаюсь к слвоарю, а затем к его ключу
    #'translations', затем к массиву, в которм ещё один словарь, под индексом 0 и уже к ключу text, через который мы получем текст
    bot.send_message(message.chat.id, text=f"*Перевод на {qq}.*\n"
                                           f"\n"
                                           f"{done_dict['translations'][0]['text'].replace('&#39;', '')}.", parse_mode="Markdown")
    #оборачиваю в трай для устранения ошибок
    #в tts обращаюсь к библиотеки gtts, вставляя переведённый текст и выбирая язык.
    #сохраняю озвучку как Произношение.ogg
    #отправляю пользователю аудиосообщение
    #завершаю процесс и удаляю файл.
    try:
        tts = gTTS(f" {done_dict['translations'][0]['text'].replace('&#39;', '')}", lang=f'{target}')
        tts.save('Произношение.ogg')
        audio = open(r'Произношение.ogg', 'rb')
        bot.send_audio(message.chat.id, audio)
        audio.close()
        os.remove('Произношение.ogg')
    except ValueError:
        bot.send_message(message.chat.id, text='Воспроизведение языка не поддерживается.')#при ошибке сообщаю пользователю, что язык не поддерживается для озвучки

def error_message(message):
    bot.send_message(message.chat.id, text="Голосовое сообщение не распознано.")# для корректности я перенаправляю сюда при слдучае подобной ошибки

@bot.message_handler()
def any_message(message): #сюда попадают все сообщения
    global q #наш выбранный язык
    text = message.text #оборачиваю в удобный вид
    list_of_cut = '/111' #команда, если пользователь сам введёт язык
    if text == 'Старт':
        start(message)
        return
    elif text == 'Список языков':
        list_lan(message)
        return
    elif text == 'Выбор языка':
        choose_lang(message, 0, 1)
        return
    elif text == 'Помощь':
        help(message)
        return
    elif text[0] in list_of_cut[0] and text[1] in list_of_cut[1] and text[2] in list_of_cut[2] and text[3] in list_of_cut[3]:
    	#сюда попадают всё, что начниается с /111 ...
    	#в q будет помещён язык
        q = ''
        new_list = text.split()#сплитую текст, чтобы сделать тут же и спсиок
        new1 = new_list[1].capitalize()#выбираю элемент под индексом 1, там всегда язык
        if new1 in LANGUAGES.values(): #проверка: если наш элемент под индексом 1 есть в значениях словаря LANGUAGES, то идем далее
            for k, v in LANGUAGES.items():
                if v == new1: #если значение = наш элемент, то...
                    q = k #присваиваю
                    bot.send_message(message.chat.id, text='Язык выбран - ' + (q).capitalize() + '')
                else:
                    bot.send_message(message.chat.id, "Такого языка не существует.")
    else: #если ничто из этого пользователь не вввёл, то
        try:#оборачивая в трай, мы перенаправялемся в фу-ию по переводу, тут же объяснял выше
            process_of_translation(message, text, q)
        except:
            process_of_translation(message, text, 'en')

print('WE WORK')
bot.polling()#включение бота
