from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.dispatcher import filters
from db_init import init_db
from db_init import show_table_med, show_table_writ, truncate_tables, clear_medic, \
    get_cat, add_to_medic, add_to_use, dell_medic, ch_medic, drop_db, get_med_cat, \
    get_ins, get_med_ins, check_medic
from aiogram import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from enum import Enum
from aiogram import types
from aiogram.dispatcher import FSMContext

API_TOKEN = 'your token'
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Просмотр")],
        [types.KeyboardButton(text="Поиск лекарства")],
        [types.KeyboardButton(text="Редактировать")],
        [types.KeyboardButton(text="Очистить")]
        # [types.KeyboardButton(text="В начало")]
    ]
    first_mess = f"{message.from_user.first_name}, привет!\n" \
                 f"Я - бот-помощник для наведения порядка в вашей домашей аптечки\n" \
                 f"Отправь мне действие, а я тебе обязательно помогу"
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    await message.reply(first_mess, reply_markup=keyboard)

@dp.message_handler(filters.Text(contains='Назад', ignore_case=True))
async def text_back(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Просмотр")],
        [types.KeyboardButton(text="Поиск лекарства")],
        [types.KeyboardButton(text="Редактировать")],
        [types.KeyboardButton(text="Очистить")]
        # [types.KeyboardButton(text="В начало")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    await message.reply("Привет!\n"
                        "Я - бот-помощник для наведения порядка в вашей домашей аптечки\n"
                        "Отправь мне действие, а я тебе обязательно помогу",
                        reply_markup=keyboard)

# @dp.message_handler(filters.Text(contains='В начало', ignore_case=True))
# async def text_view(message: types.Message):
#     kb = [
#         [types.KeyboardButton(text="Удалить всю историю действий")],
#         [types.KeyboardButton(text="Назад")]
#     ]
#     keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
#     await message.reply("Выбери, что хочешь посмотреть", reply_markup=keyboard)
#
# @dp.message_handler(filters.Text(contains='Удалить всю историю действий', ignore_case=True))
# async def text_view(message: types.Message):
#     drop_db()
#     await message.reply("Чтобы начать сначала, напиши команду /start")

@dp.message_handler(filters.Text(contains='Просмотр', ignore_case=True))
async def text_view(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Список лекарств в аптечке")],
        [types.KeyboardButton(text="Записи приема лекарств")],
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    await message.reply("Выбери, что хочешь посмотреть", reply_markup=keyboard)

@dp.message_handler(filters.Text(contains='Записи приема лекарств', ignore_case=True))
async def show_medicines(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    try:
        result = show_table_writ()
        if len(result) > 0:
            headers = ["ID", "Количество", "Название лекарства"]
            table_data = [headers] + [[row[0], row[1], row[2]] for row in result]
            if len(headers) > 0:
                max_lengths = [max(len(str(row[i])) for row in table_data) for i in range(len(headers))]
                table_text = ""
                for row in table_data:
                    if len(row) == len(headers):
                        table_text += "  ".join(str(row[i]).ljust(max_lengths[i] + 2) for i in range(len(headers))) + "\n"
                    else:
                        await message.answer(text="Неверное количество столбцов в таблице.", reply_markup=keyboard)
                        return
                await message.answer(text=f"Таблица записи приема лекарств:\n\n{table_text}", reply_markup=keyboard)
            else:
                await message.answer(text="Отсутствуют заголовки таблицы.", reply_markup=keyboard)
        else:
            await message.answer(text="Таблица записи приема лекарств пуста.", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=keyboard)

@dp.message_handler(filters.Text(contains='Список лекарств в аптечке', ignore_case=True))
async def show_list(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    try:
        result = show_table_med()
        if len(result) > 0:
            headers = ["ID", "Название лекарства","Дозировка","Категория","Количество таблеток","Инструкция"]
            table_data = [headers] + [[row[0], row[1], row[2],row[3], row[4], row[5]] for row in result]
            table_text = ""
            max_lengths = [max(len(str(row[i])) for row in table_data) for i in range(len(headers))]
            for row in table_data:
                table_text += "  ".join(str(row[i]).ljust(max_lengths[i] + 5) for i in range(len(headers))) + "\n"
            await message.answer(text=f"Таблица лекарств:\n\n{table_text}", reply_markup=keyboard)
        else:
            await message.answer(text="Таблица лекарств пуста.", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}", reply_markup=keyboard)

@dp.message_handler(filters.Text(contains='Редактировать', ignore_case=True))
async def text_edit(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Добавить новое лекарство")],
        [types.KeyboardButton(text="Изменить лекарство")],
        [types.KeyboardButton(text="Удалить лишнее лекарство")],
        [types.KeyboardButton(text="Добавить запись приема лекарства")],
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    await message.reply("Выбери действие", reply_markup=keyboard)

class AddMedicineList(StatesGroup):
    NAME = State()
    DOSAGE = State()
    CATEGORY = State()
    QUANTITY = State()
    INSTRUCTION = State()
    ENTER_DATA = State()
@dp.message_handler(filters.Text(contains='Добавить запись приема лекарства', ignore_case=True))
async def add_medicine_usage_callback(query: types.CallbackQuery):
    await query.reply(text="Введите название лекарства и количество принятых таблеток в следующем формате:\n"
                           "Название, Количество\n"
                           "Например: Аспирин, 1")
    await AddMedicineList.ENTER_DATA.set()
@dp.message_handler(state=AddMedicineList.ENTER_DATA)
async def process_enter_data(message: types.Message, state: FSMContext):
    data = message.text.split(",")
    if len(data) == 2:
        name_med = data[0].strip()
        quantity_med = int(data[1].strip())
        try:
            add_to_use(name_med,  quantity_med)
            await message.answer("Прием лекарства успешно записан")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("Неверный формат данных. Введите данные в формате: Название, Дозировка, Количество")
    await state.finish()

class AddMedicineStates(StatesGroup):
    NAME = State()
    DOSAGE = State()
    CATEGORY = State()
    QUANTITY = State()
    INSTRUCTION = State()
    ENTER_DATA = State()
@dp.message_handler(filters.Text(contains='Добавить новое лекарство', ignore_case=True))
async def add_new_medicine_callback(query: types.CallbackQuery):
    await query.reply(text="Введите данные о новом лекарстве в следующем формате:\n"
                               "Название, Дозировка, Категория, Количество, Инструкция\n"
                               "Например: Аспирин, 0.1, Обезболивающее, 30, Принимать по одной таблетке в день")
    await AddMedicineStates.ENTER_DATA.set()
@dp.message_handler(state=AddMedicineStates.ENTER_DATA)
async def process_enter_data(message: types.Message, state: FSMContext):
    data = message.text.split(",")
    if len(data) == 5:
        name_med = data[0].strip()
        dosage_med = float(data[1].strip())
        category_name = data[2].strip()
        quantity_med = int(data[3].strip())
        instruction_name = data[4].strip()
        try:
            fl = add_to_medic(name_med, dosage_med, category_name, quantity_med, instruction_name)
            if fl:
                await message.answer("Новое лекарство успешно добавлено")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("Неверный формат данных. Введите данные в формате: Название, Дозировка, Категория, Количество, Инструкция")
    await state.finish()

class EditMedicineStates(StatesGroup):
    ENTER_NAME = State()
    ENTER_DATA = State()
@dp.message_handler(filters.Text(contains='Изменить лекарство', ignore_case=True))
async def edit_medicine_callback(query: types.CallbackQuery):
    await query.reply(text="Введите новые данные о лекарстве в следующем формате:\n"
                                 "Название, Дозировка, Категория, Количество, Инструкция\n"
                                 "Например: Аспирин, 0.1, Обезболивающее, 30, Принимать по одной таблетке в день")
    await EditMedicineStates.ENTER_DATA.set()
@dp.message_handler(state=EditMedicineStates.ENTER_DATA)
async def process_enter_data(message: types.Message, state: FSMContext):
    data = message.text.split(",")
    if len(data) == 5:
        name_med = data[0].strip()
        dosage_med = float(data[1].strip())
        category_name = data[2].strip()
        quantity_med = int(data[3].strip())
        instruction_name = data[4].strip()
        try:
            fl1 = dell_medic(name_med)
            fl = add_to_medic(name_med, dosage_med, category_name, quantity_med, instruction_name)
            if fl1 and fl:
                await message.answer("Данные лекарства успешно изменены")
            else:
                await message.answer("Не удалось изменить данные лекарства")
        except Exception as e:
            await message.answer(f"Произошла ошибка: {e}")
    else:
        await message.answer("Неверный формат данных. Введите данные в формате: Название, Дозировка, Категория, Количество, Инструкция")
    await state.finish()
class DeleteMedicineStates(StatesGroup):
    ENTER_NAME = State()
@dp.message_handler(filters.Text(contains='Удалить лишнее лекарство', ignore_case=True))
async def delete_medicine_callback(query: types.CallbackQuery):
    await query.reply(text="Введите название лекарства, которое вы хотите удалить:")
    await DeleteMedicineStates.ENTER_NAME.set()
@dp.message_handler(state=DeleteMedicineStates.ENTER_NAME)
async def process_enter_name(message: types.Message, state: FSMContext):
    name = str(message.text)
    try:
        fl = dell_medic(name)
        if fl:
            await message.answer("Лекарство успешно удалено")
        else:
            await message.answer("Не удалось удалить лекарство")
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    await state.finish()

@dp.message_handler(filters.Text(equals =['Поиск лекарства'], ignore_case=True))
async def text_critmed(message: types.Message):
    kb = [
        [types.KeyboardButton(text="По категориям")],
        [types.KeyboardButton(text="По способу приема")],
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    await message.answer("Выбери критерий", reply_markup=keyboard)


class CategoryMedicineStates(StatesGroup):
    ENTER_CATEGORY = State()
@dp.message_handler(filters.Text(equals=['По категориям'], ignore_case=True))
async def text_critmed(message: types.Message):
    try:
        categories = get_cat()
        categories_message = "Выберите номер категории из списка:\n"
        for category_number, category_name in categories.items():
            categories_message += f"{category_number}. {category_name}\n"
        await message.answer(categories_message)
        await CategoryMedicineStates.ENTER_CATEGORY.set()

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
@dp.message_handler(state=CategoryMedicineStates.ENTER_CATEGORY)
async def process_category_number(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    if message.text.isdigit():
        cat_id = int(message.text)
        res = get_med_cat(cat_id)
        if len(res) > 0:
            # table_text = "Таблица лекарств:\n"
            # for row in res:
            #     table_text += f"Название лекарства: {row[0]}, Количество таблеток: {row[1]}\n"
            # await message.answer(table_text, reply_markup=keyboard)
            await message.answer(str(res), reply_markup=keyboard)
        else:
            await message.answer(text="Таблица лекарств пуста.", reply_markup=keyboard)
            await state.finish()
    elif message.text.lower() == "назад":
        await message.answer("Вы вернулись назад.")
        await state.finish()
    else:
        await message.answer("Некорректный номер категории. Попробуйте еще раз.")

class InstMedicineStates(StatesGroup):
    ENTER_CATEGORY = State()
@dp.message_handler(filters.Text(equals=['По способу приема'], ignore_case=True))
async def text_critmed(message: types.Message):
    try:
        categories = get_ins()
        categories_message = "Выберите номер инструкции из списка:\n"
        for category_number, category_name in categories.items():
            categories_message += f"{category_number}. {category_name}\n"
        await message.answer(categories_message)
        await InstMedicineStates.ENTER_CATEGORY.set()
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
@dp.message_handler(state=InstMedicineStates.ENTER_CATEGORY)
async def process_category_number(message: types.Message, state: FSMContext):
    kb = [
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    if message.text.isdigit():
        ins_id = int(message.text)
        res = get_med_ins(ins_id)
        if len(res) > 0:
            # table_text = "Таблица лекарств:\n"
            # for row in res:
            #     table_text += f"Название лекарства: {row[0]}, Количество таблеток: {row[1]}\n"
            # await message.answer(table_text, reply_markup=keyboard)
            await message.answer(str(res), reply_markup=keyboard)
        else:
            await message.answer(text="Таблица инструкций пуста.", reply_markup=keyboard)
            await state.finish()
    elif message.text.lower() == "назад":
        await message.answer("Вы вернулись назад.")
        await state.finish()
    else:
        await message.answer("Некорректный номер инструкции. Попробуйте еще раз.")

@dp.message_handler(filters.Text(contains='Очистить', ignore_case=True))
async def text_clear(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Удалить лекарства, которых нет в наличии")],
        [types.KeyboardButton(text="Всю историю")],
        [types.KeyboardButton(text="Назад")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
    await message.reply("Выбери, что удаляем", reply_markup=keyboard)

@dp.message_handler(filters.Text(contains='Удалить лекарства, которых нет в наличии', ignore_case=True))
async def show_list(message: types.Message):
    try:
        kb = [
            [types.KeyboardButton(text="Назад")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
        clear_medic()
        await message.reply("В аптечке нет пустых коробок из-под лекарств", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

@dp.message_handler(filters.Text(contains='Всю историю', ignore_case=True))
async def show_list(message: types.Message):
    try:
        kb = [
            [types.KeyboardButton(text="Назад")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, row_width=1)
        truncate_tables()
        await message.reply("Все таблицы пусты", reply_markup=keyboard)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")

if __name__ == '__main__':
    init_db()
    executor.start_polling(dp, skip_updates=True)
