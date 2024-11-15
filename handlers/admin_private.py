from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.reply import get_keyboard
from aiogram.enums import ParseMode
admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]),IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить вопрос",
    "Изменить вопрос",
    "Удалить вопрос",
    "Я так, просто посмотреть зашёл",
    placeholder= "Выберите действие",
    sizes=(2,1,1),
)

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Я так, просто посмотреть зашёл")
async def starring_at_product(message: types.Message):
    await message.answer("ОК, вот список вопросов")



@admin_router.message(F.text == "Изменить вопрос")
async def change_product(message: types.Message):
    await message.answer("ОК, вот список вопросов")


@admin_router.message(F.text == "Удалить вопрос")
async def delete_product(message: types.Message):
    await message.answer("Выберите вопрос(ы) для удаления")


#Код ниже для машины состояний (FSM)

class AddProduct(StatesGroup):
    name = State()
    description = State()
    price = State()
    image = State()

    texts = {
        'AddProduct:name':'Введите название заново',
        'AddProduct:description': 'Введите описание заново',
        'AddProduct:price': 'Введите стоимость заново',
        'AddProduct:image': '******',
    }



@admin_router.message(StateFilter(None),F.text == "Добавить вопрос")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название вопроса", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(AddProduct.name)


@admin_router.message(StateFilter('*'), Command("отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'), Command("назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddProduct.name:
        await message.answer('Предыдущего шага нет, используйте команду "отмена"')
        return

    previous = None
    for step in AddProduct.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddProduct.texts[previous.state]}")
            return
        previous = step




@admin_router.message(AddProduct.name,F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("<b>Введите описание вопроса</b>")
    await state.set_state(AddProduct.description)

@admin_router.message(AddProduct.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст названия товара")



@admin_router.message(AddProduct.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите ключевые слова")
    await state.set_state(AddProduct.price)

@admin_router.message(AddProduct.description)
async def add_description(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст описания товара")



@admin_router.message(AddProduct.price, F.text)
async def add_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await message.answer("Загрузите изображение либо введите 'Пропустить'")
    await state.set_state(AddProduct.image)

@admin_router.message(AddProduct.price)
async def add_price(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите ключевые слова для вопроса через запятую")


@admin_router.message(AddProduct.image, F.text == "пропустить")
async def add_image(message: types.Message, state: FSMContext):
    await message.answer("Вопрос добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()


@admin_router.message(AddProduct.image, F.photo)
async def add_image(message: types.Message, state: FSMContext):
    print("Сообщение получено:", message.text)
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Вопрос добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))
    await state.clear()
    return

@admin_router.message(AddProduct.image)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели недопустимые данные, отправьте фотографию для вопроса, либо нажмите кнопку "пропустить"')



