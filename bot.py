import os
import django
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from asgiref.sync import sync_to_async

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")
django.setup()

from main.models import User, UserTelegram

BOT_TOKEN = "8218372259:AAFXKY2LjAwHxEID4bhYZJMXcMA7peg9ehw"

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: types.Message):
    args = message.text.split()

    # ✅ Agar kod yuborilmagan bo‘lsa
    if len(args) == 1:
        await message.answer(
            "Iltimos, sayt orqali berilgan kodni yuboring. Masalan:\n/start ABC123"
        )
        return

    # ✅ Avval code ni olamiz
    code = args[1].strip()

    try:
        # ✅ Userni async tarzda olish
        user = await sync_to_async(User.objects.get)(telegram_code=code)

        # ✅ chat_id ni saqlash
        await sync_to_async(UserTelegram.objects.update_or_create)(
            user=user,
            defaults={"chat_id": message.chat.id},
        )

        await message.answer("✅ Telegram hisobingiz muvaffaqiyatli bog‘landi!")

    except User.DoesNotExist:
        await message.answer("❗ Kod noto‘g‘ri.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
