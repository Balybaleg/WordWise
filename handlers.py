import logging
import openai

from bot import dp
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.utils.callback_data import CallbackData

from generate import generate_mood, generate_synopsis

class Waiting(StatesGroup):
    wait_text_mood = State() 
    wait_text_synopsis = State() 

@dp.message_handler(commands=['start'])  # Обработчик команды /start
async def send_welcome(message: Message):
    await message.reply("Привет! Я бот WordWise! \nМои функции для обощение текста и определение его настроения\nДля получения списка команд введите /help")

@dp.message_handler(commands=['help'])   # Обработчик команды /help
async def send_welcome(message: Message):
    await message.answer('/mood - узнать настроение текста \n/synopsis - обобщить текст\n\U00002757В бот нельзя отправлять фотографии и тексты, превышающие 3000 символов')


@dp.message_handler(commands=['cancel'], state='*') # Обработчик команды /cancel
async def cancel(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('Отменено.')


@dp.message_handler(commands=['mood','synopsis'], state='*') # Общий обработчик команд synopsis и mood
async def text_worker(message: Message, state: FSMContext):

    command = message.get_command()

    if (command == '/mood'):                                # В зависимости от команды меняем состояние бота, на соответствующее команде.
        await message.reply("Введите текст: ")
        await state.set_state(Waiting.wait_text_mood)

    elif (command == '/synopsis'):
        await message.reply("Введите текст: ")
        await state.set_state(Waiting.wait_text_synopsis)



@dp.message_handler(state = Waiting.wait_text_mood)            # Обработчик сообщения в состоянии wait_text_mood, для получения текста для определения настроения текста от пользователя
async def mood(message: Message):

    state = dp.current_state(user=message.from_user.id)
    wait_msg = await message.reply("Подождите, текст обрабатывается\nЭто сообщение будет изменено")
    prompt = message.text

    try:
        response = await generate_mood(prompt)

    except openai.error.InvalidRequestError as e:           # Отлов ошибки неправильного запроса, в данном случае превышение количество символов.
        logging.exception(e)
        error_message = str(e)

        if "maximum context length" in error_message:
            response = f"\U000026A0 Ошибка: превышено максимальное количество символов. Попробуйте сократить текст до 3000 символов."
        else:
            response = f"\U000026A0 Произошла ошибка. Попробуйте еще раз позже."

    await wait_msg.edit_text(response)
    await state.finish()



@dp.message_handler(state = Waiting.wait_text_synopsis)            # Обработчик сообщения в состоянии wait_text_synopsis, для получения текста для обобщения от пользователя
async def synopsis(message: Message):
    state = dp.current_state(user=message.from_user.id)
    wait_msg = await message.reply("Подождите, текст обрабатывается\nЭто сообщение будет изменено")
    prompt = message.text

    try:
        response = await generate_synopsis(prompt)

    except openai.error.InvalidRequestError as e:           # Отлов ошибки неправильного запроса, в данном случае превышение количество символов.
        logging.exception(e)
        error_message = str(e)

        if "maximum context length" in error_message:
            response = f"\U000026A0 Ошибка: превышено максимальное количество символов. Попробуйте сократить текст до 3000 символов."
        else:
            response = f"\U000026A0 Произошла ошибка. Попробуйте еще раз позже."

    await wait_msg.edit_text(response)
    await state.finish()



@dp.message_handler()           #Обработчик любых сообщений от пользователя.
async def echo(message: Message):
    await message.answer("Извините, я не понимаю!\nИспользуйте команду /help")
