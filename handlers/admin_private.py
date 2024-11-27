from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Question
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
async def delete_product(message: types.Message, counter):
    print(counter)
    await message.answer("Выберите вопрос(ы) для удаления")


#Код ниже для машины состояний (FSM)

class AddQuestion(StatesGroup):
    name = State()
    description = State()
    keywords = State()
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
    await state.set_state(AddQuestion.name)


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

    if current_state == AddQuestion.name:
        await message.answer('Предыдущего шага нет, используйте команду "отмена"')
        return

    previous = None
    for step in AddQuestion.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddQuestion.texts[previous.state]}")
            return
        previous = step




@admin_router.message(AddQuestion.name, F.text)
async def add_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("<b>Введите описание вопроса</b>")
    await state.set_state(AddQuestion.description)

@admin_router.message(AddQuestion.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст названия товара")



@admin_router.message(AddQuestion.description, F.text)
async def add_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer("Введите ключевые слова")
    await state.set_state(AddQuestion.keywords)

@admin_router.message(AddQuestion.description)
async def add_description(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст описания товара")



@admin_router.message(AddQuestion.keywords, F.text)
async def add_keywords(message: types.Message, state: FSMContext):
    await state.update_data(keywords=message.text)
    await message.answer("Загрузите изображение либо введите 'Пропустить'")
    await state.set_state(AddQuestion.image)

@admin_router.message(AddQuestion.keywords)
async def add_keywords(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите ключевые слова для вопроса через запятую")


@admin_router.message(AddQuestion.image, F.text == "пропустить")
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await message.answer("Вопрос добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))

    obj = Question(
        name=data["name"],
        description=data["description"],
        keywords=data["keywords"],
    )
    session.add(obj)
    await session.commit()

    await state.clear()


@admin_router.message(AddQuestion.image, F.photo)
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    print("Сообщение получено:", message.text)
    await state.update_data(image=message.photo[-1].file_id)
    await message.answer("Вопрос добавлен", reply_markup=ADMIN_KB)
    data = await state.get_data()
    await message.answer(str(data))

    obj = Question(
        name = data["name"],
        description = data["description"],
        keywords = data["keywords"],
        image = data["image"]
    )
    session.add(obj)
    await session.commit()
    await state.clear()
    return

@admin_router.message(AddQuestion.image)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели недопустимые данные, отправьте фотографию для вопроса, либо нажмите кнопку "пропустить"')



