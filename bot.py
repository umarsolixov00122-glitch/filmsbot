import json
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

TOKEN = "8638573679:AAGyt_lhb1mY59RRjGjYMo6gO5oKEMPoEME"
ADMIN_ID = 8578660273  # sizning Telegram ID

bot = Bot(token=TOKEN)
dp = Dispatcher()

# baza yuklash
try:
    with open("movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)
except FileNotFoundError:
    movies = {}

def save_movies():
    with open("movies.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, indent=4, ensure_ascii=False)

# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("🎬 Kino botga xush kelibsiz!\nKino nomi yoki kodini yuboring.")

# barcha xabarlarni bir joyda qayta ishlash
@dp.message()
async def handle_message(message: types.Message):
    if message.text:  # matnli xabarlar
        text = message.text.lower()

        # kodi orqali qidirish
        if text in movies:
            movie = movies[text]
            await message.answer_video(movie["file_id"], caption=f"{movie['name']}")
            return

        # nom orqali qidirish
        results = []
        for code, movie in movies.items():
            if text in movie["name"].lower():
                results.append(f"{code} - {movie['name']}")

        if results:
            await message.answer("🔎 Topildi:\n" + "\n".join(results[:10]))
        else:
            await message.answer("❌ Kino topilmadi")

    # admin video yuborsa avtomatik qo‘shish
    elif message.video and message.from_user.id == ADMIN_ID:
        file_id = message.video.file_id
        new_code = str(len(movies) + 1)
        name = message.caption if message.caption else f"Kino {new_code}"

        movies[new_code] = {
            "name": name,
            "file_id": file_id
        }
        save_movies()
        await message.answer(f"✅ Kino qo‘shildi!\n🎬 Kod: {new_code}")

# botni ishga tushirish, tarmoq uzilishlariga chidamli
async def main():
    print("✅ Bot ishga tushdi...")
    while True:
        try:
            await dp.start_polling(bot, skip_updates=True, timeout=30)
        except Exception as e:
            print(f"❌ Xato yuz berdi: {e}. 5 soniyadan keyin qayta urinish...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())