from aiogram import Router, types, F, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from datetime import datetime, timedelta, timezone

from bot.data_base.database import add_user, set_timezone, get_timezone
from bot.keyboards.user_keyboards import main_keyboard, get_timezone_kb

import asyncio
router = Router()

@router.message(CommandStart())
async def command_start(message: Message):
    await add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    await message.answer('Привет!\nЯ бот, который поможет тебе не забыть что то очень важное. '
                         'Для начала советую ознакомится с командами бота',
                         reply_markup=main_keyboard())

@router.message(Command('set_timezone'))
async def command_set_timezone(message: Message):
    await message.answer('Выберите свой часовой пояс:', reply_markup=get_timezone_kb())


@router.callback_query()
async def process_timezone_callback(call: types.CallbackQuery):
    utc_user = call.data
    utc_offset_int = int(utc_user)
    await set_timezone(call.from_user.id, utc_offset_int)
    await call.answer('Часовой пояс успешно выбран')

@router.message(F.text == 'Профиль')
async def profile(message: Message):
    await message.answer(f'Ваш профиль: \n\n'
                         f'Имя: {message.from_user.full_name}\n'
                         f'Ваш часовой пояс: UTC+{await get_timezone(message.from_user.id)}')


def parse_reminder_command(message_text: str) -> tuple[datetime, str] | None:
    try:
        parts = message_text.split(maxsplit=3)

        if len(parts) >= 4:
            date_str = parts[1]
            time_str = parts[2]
            reminder_text = parts[3]

            dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m.%Y %H:%M")

            if dt <= datetime.now():
                return None

            return dt, reminder_text
    except (ValueError, IndexError):
        return None
    return None


async def schedule_message(bot: Bot, chat_id: int, text: str, user_time: datetime, utc_offset: int):
    try:
        localized_time = user_time.replace(tzinfo=timezone(timedelta(hours=utc_offset)))
        utc_time = localized_time.astimezone(timezone.utc)

        now_utc = datetime.now(timezone.utc)
        delay = (utc_time - now_utc).total_seconds()

        if delay <= 0:
            raise ValueError("Указанное время уже прошло")

        await asyncio.sleep(delay)
        await bot.send_message(chat_id, f"⏰ Напоминание: {text}")
    except Exception:
        await bot.send_message(chat_id, 'Ошибка при установке напоминания')


@router.message(Command('remind'))
async def handle_reminder(message: types.Message):
    try:
        result = parse_reminder_command(message.text)
        if not result:
            return await message.answer("Неверный формат❌\nИспользуйте: /remind ДД.ММ.ГГГГ ЧЧ:MM текст напоминания")

        dt, reminder_text = result

        utc_offset = await get_timezone(message.from_user.id)


        asyncio.create_task(
            schedule_message(message.bot, message.chat.id, reminder_text, dt, utc_offset)
        )

        await message.answer(
            f"Напоминание установлено на {dt.strftime('%d.%m.%Y %H:%M')}✅\n"
            f"Текст: {reminder_text}"
        )
    except Exception:
        await message.answer("Произошла ошибка")

@router.message(F.text == 'Команды')
async def commands(message: Message):
    await message.answer('Команды бота:\n\n'
                         'Сменить часовой пояс: /set_timezone\n'
                         'Добавить напоминание /remind\n\n'
                         'Формат напоминания /remind <i>ДД.НН.ГГГГ ЧЧ:ММ</i> ТЕКСТ', parse_mode="HTML")

@router.message(F.text == 'О боте')
async def about_the_bot(message: Message):
    await message.answer('Этот бот является просто небольшим проектом, созданным @not1nqwe')