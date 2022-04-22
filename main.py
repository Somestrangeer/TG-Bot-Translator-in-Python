import telebot

token = 'your token here' 
KeyAPI = 'your API here'
folder_id = 'your folder Id here' 

bot = telebot.TeleBot(token)

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

print('WE WORK')
bot.polling()