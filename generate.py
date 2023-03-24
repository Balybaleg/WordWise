import openai

import settings

OPENAI_API_TOKEN = settings.OPENAI_API_TOKEN

openai.api_key = OPENAI_API_TOKEN

async def generate_synopsis(prompt: str):
    response = openai.Completion.create(            # Создание запроса к нейросети
    model="text-davinci-003",                       # Модель обработчика текста
    prompt= prompt + "\n Обобщи данный текст.",     # Сам текст на который нужно ответить
    temperature=0.7,
    max_tokens=1000,                                # Максимальное количество символов в ответе
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0
    )

    return response["choices"][0]["text"] + "\n \n<b>\U00002757 Обобщение текста может упускать некоторые изложенные факты и допускать логические ошибки.</b>"

async def generate_mood(prompt: str):
    response = openai.Completion.create(
    model="text-davinci-003",
    prompt= "Какое настроение у текста:" + prompt,
    temperature=0.5,
    max_tokens=1000,
    top_p=1.0,
    frequency_penalty=0.5,
    presence_penalty=0.0
    )
    return response["choices"][0]["text"]