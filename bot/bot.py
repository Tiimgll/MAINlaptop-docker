import telebot
from telebot import types
from ultralytics import YOLO
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env
load_dotenv()

# Загрузить модель
#model = YOLO("yolo11n.pt")  # pretrained YOLO11n model
model = YOLO("best.pt")  # Используем твою обученную модель

API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)  # Ключ

def detect_objects(image_path):
  # Запуск инференса на изображении
  results = model([image_path]) # Вернет список объектов результатов

  # Обработка результатов
  result = results[0] # берем первый (и в данном случае единственный) результат
  result.show() # отображение на экране (для отладки, если нужно)

  # Путь для сохранения аннотированного изображения
  annotated_image_path = "annotated_image.jpg"
  result.save(filename=annotated_image_path)

  return annotated_image_path

@bot.message_handler(commands=['start'])
def start(message):
  botton_0 = types.ReplyKeyboardMarkup(resize_keyboard=True)
  botton_1 = types.KeyboardButton('Загрузить фото')
  botton_2 = types.KeyboardButton('Информация')
  botton_3 = types.KeyboardButton('Тех. поддержка')
  botton_0.add(botton_1, botton_2, botton_3)
  bot.send_message(message.chat.id, 'Я телеграмм бот для определения брака ноутбуков', reply_markup=botton_0)

@bot.message_handler(content_types=['text'])
def get_text_message(message):
  if message.text == 'бот':
    bot.send_message(message.chat.id, 'нажми /start')
  elif message.text == 'Загрузить фото':
    bot.send_message(message.chat.id, 'Пожалуйста, отправьте фото ноутбука для анализа.')
  elif message.text == 'Информация':
    bot.send_message(message.chat.id, 'Привет, я бот который найдет поломку в твоем ноутбуке. Чтобы я нашел ошибку загрузи картинку/видео и при помощи нейросетей я выдам тебе результат с возможными поломками.')
  elif message.text == 'Тех. поддержка':
    bot.send_message(message.chat.id, '[Администратор](https://t.me/hantik_X)', parse_mode='Markdown')

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
  file_info = bot.get_file(message.photo[-1].file_id)
  downloaded_file = bot.download_file(file_info.file_path)

  photo_path = "received_photo.jpg"
  with open(photo_path, 'wb') as new_file:
    new_file.write(downloaded_file)

  annotated_image_path = detect_objects(photo_path)

  with open(annotated_image_path, 'rb') as img_file:
    bot.send_photo(message.chat.id, img_file)

if __name__ == "__main__":
  bot.polling(none_stop=True)
