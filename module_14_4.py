from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import CallbackQuery
from crud_functions import *


BOT_TOKEN = '6377273949:AAHSHDC044KDjch3EQhPuoRQlJT7Swql5xQ'

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

btn = KeyboardButton(text='Рассчитать')
btn2 = KeyboardButton(text='Информация')
btn3 = KeyboardButton(text='Купить')
kb = ReplyKeyboardMarkup(keyboard=[[btn, btn2],
                                   [btn3]], resize_keyboard=True, one_time_keyboard=True)

in_btn = InlineKeyboardButton(
    text='Рассчитать норму калорий',
    callback_data='calories'
)
in_btn2 = InlineKeyboardButton(
    text='Формулы расчёта',
    callback_data='formulas'
)
in_kb = InlineKeyboardMarkup(inline_keyboard=[[in_btn, in_btn2]])

in_prod_1 = InlineKeyboardButton(
    text='Product1',
    callback_data='product_buying'
)
in_prod_2 = InlineKeyboardButton(
    text='Product2',
    callback_data='product_buying'
)
in_prod_3 = InlineKeyboardButton(
    text='Product3',
    callback_data='product_buying'
)
in_prod_4 = InlineKeyboardButton(
    text='Product4',
    callback_data='product_buying'
)
in_kb_prod = InlineKeyboardMarkup(inline_keyboard=[[in_prod_1, in_prod_2, in_prod_3, in_prod_4]])

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message(Command(commands=['start']))
async def start_message(message: Message):
    await message.answer(
        'Привет! Я бот помогающий твоему здоровью.',
        reply_markup=kb)

@dp.message(F.text=='Рассчитать')
async def main_menu(message: Message):
    await message.answer('Выберите опцию:', reply_markup=in_kb)

@dp.message(F.text=='Купить')
async def get_buying_list(message: Message):
    prod = get_all_products()
    for i in range(4):
        await message.answer(f'Название: {prod[i][1]} | Описание: {prod[i][2]} | Цена: {prod[i][3]}')
        photo = FSInputFile(f'prod_{i + 1}.png')
        await message.answer_photo(photo)
    await message.answer('Выберите продукт для покупки:', reply_markup=in_kb_prod)

@dp.callback_query(F.data=='product_buying')
async def send_confirm_message(callback: CallbackQuery):
    await callback.message.answer(
        'Вы успешно приобрели продукт!', reply_markup=callback.message.reply_markup)
    await callback.answer()

@dp.callback_query(F.data=='formulas')
async def get_formulas(callback: CallbackQuery):
    await callback.message.answer(
        '10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) + 5', reply_markup=callback.message.reply_markup)
    await callback.answer()

@dp.callback_query(F.data=='calories')
async def set_age(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите свой возраст:', reply_markup=callback.message.reply_markup)
    await callback.answer()
    await state.set_state(UserState.age)

@dp.message(StateFilter(UserState.age))
async def set_growth(message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await state.set_state(UserState.growth)

@dp.message(StateFilter(UserState.growth))
async def set_weight(message, state: FSMContext):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await state.set_state(UserState.weight)

@dp.message(StateFilter(UserState.weight))
async def send_calories(message, state: FSMContext):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    result = int(data['weight']) * 10 + int(data['growth']) * 6.25 - int(data['age']) * 5 + 5
    await message.answer(f'Норма калорий для вас составляет: {result}')

if __name__ == '__main__':
    dp.run_polling(bot)
