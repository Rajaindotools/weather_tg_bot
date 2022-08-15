import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Hello! Write the city and get the weather : ")

@dp.message_handler()
async def get_weather(message: types.Message):
        try:
            r = requests.get(
                f'https://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
            )
            data = r.json()

            city = data['name']
            cur_weather_temp = data['main']['temp']
            cur_weather_feels = data['main']['feels_like']
            cur_weather_humidity = data['main']['humidity']
            cur_weather_pressure = data['main']['pressure']
            cur_weather_sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
            cur_weather_sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
            cur_weather_wind_speed = data['wind']['speed']

            await message.reply(
                f'on the current date and time the weather in the city {city} {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}\n'
                f'current weather in the city : {city} \nTemperature: {cur_weather_temp} °\nFeels like: {cur_weather_feels} °\n'
                f'Humidity : {cur_weather_humidity} % \nPressure: {cur_weather_pressure} мм.рт.ст \nSunrise: {cur_weather_sunrise} h.min.sec\n'
                f'Sunset : {cur_weather_sunset} h.min.sec\nSpeed wind: {cur_weather_wind_speed} m/s'
                )

        except:
            await message.reply('check city name')

if __name__ == '__main__':
    executor.start_polling(dp)
