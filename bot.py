import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = "8706781197:AAFOdCjrVShjQ5d6U5YyA6DSZ7y8XQpIe48"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# alphabets
hiragana = [
    ("あ","a"),("い","i"),("う","u"),("え","e"),("お","o"),
    ("か","ka"),("き","ki"),("く","ku"),("け","ke"),("こ","ko")
]

katakana = [
    ("ア","a"),("イ","i"),("ウ","u"),("エ","e"),("オ","o"),
    ("カ","ka"),("キ","ki"),("ク","ku"),("ケ","ke"),("コ","ko")
]

# user state
users = {}

# keyboard
menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Hiragana"), KeyboardButton(text="Katakana")],
        [KeyboardButton(text="Stop")]
    ],
    resize_keyboard=True
)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Choose an alphabet:", reply_markup=menu)

# category select
@dp.message(lambda m: m.text in ["Hiragana","Katakana"])
async def choose(message: types.Message):
    alphabet = hiragana if message.text=="Hiragana" else katakana
    users[message.from_user.id] = {
        "set": alphabet,
        "index": 0,
        "tries": 0
    }
    letter = alphabet[0][0]
    await message.answer(f"What letter is this?\n{letter}")

# stop
@dp.message(lambda m: m.text=="Stop")
async def stop(message: types.Message):
    users.pop(message.from_user.id, None)
    await message.answer("Test stopped ❌")

# answers
@dp.message()
async def check(message: types.Message):
    user = message.from_user.id

    if user not in users:
        return

    data = users[user]
    letter, correct = data["set"][data["index"]]
    answer = message.text.lower()

    if answer == correct:
        data["index"] += 1
        data["tries"] = 0

        if data["index"] >= len(data["set"]):
            await message.answer("Congratulations! You finished 🎉")
            users.pop(user)
            return

        next_letter = data["set"][data["index"]][0]
        await message.answer(f"✅ Correct!\nNext letter:\n{next_letter}")

    else:
        data["tries"] += 1

        if data["tries"] >= 3:
            await message.answer(f"❌ Answer: {correct}")
            data["index"] += 1
            data["tries"] = 0

            if data["index"] >= len(data["set"]):
                await message.answer("Test finished 🎉")
                users.pop(user)
                return

            next_letter = data["set"][data["index"]][0]
            await message.answer(f"Next letter:\n{next_letter}")
        else:
            await message.answer("❌ Wrong, try again")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())