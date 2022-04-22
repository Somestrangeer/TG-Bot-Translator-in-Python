import requests
import subprocess
import os

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
