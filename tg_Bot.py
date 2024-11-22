import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
import os  # Для работы с переменными окружения

# Токен бота теперь берется из переменных окружения
API_TOKEN = os.getenv("API_TOKEN")

bot = telebot.TeleBot(API_TOKEN)

# Список файлов (фото и видео)
media_files = [
    "image.png",  # Путь к первому фото
    "tony.png",  # Путь ко второму фото
    "IMG_5935.MP4"   # Путь к видео
]

# Создаем клавиатуру с кнопкой
def get_keyboard():
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Показать случайный файл", callback_data="show_random")
    markup.add(button)
    return markup

@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Нажми на кнопку, чтобы увидеть случайное фото или видео.",
        reply_markup=get_keyboard()
    )

@bot.callback_query_handler(func=lambda call: call.data == "show_random")
def send_random_media(call):
    # Выбираем случайный файл из списка
    random_file = random.choice(media_files)

    # Проверяем тип файла (по расширению)
    if random_file.endswith((".png", ".jpg", ".jpeg")):
        # Отправляем фото
        with open(random_file, "rb") as photo:
            bot.send_photo(call.message.chat.id, photo)
    elif random_file.endswith(".mp4"):
        # Отправляем видео
        with open(random_file, "rb") as video:
            bot.send_video(call.message.chat.id, video)

    bot.answer_callback_query(call.id, "Файл отправлен!")  # Уведомление для пользователя

if __name__ == "__main__":
    bot.polling(none_stop=True)
