from aiogram import F, Router, types
from aiogram.filters import Command, StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import Question
from database.orm_query import orm_add_question, orm_add_question_pic, orm_get_questions, orm_get_question, \
    orm_delete_question, orm_update_question
from filters.chat_types import ChatTypeFilter, IsAdmin
from kbds.inline import get_callback_btns
from kbds.reply import get_keyboard
from aiogram.enums import ParseMode
admin_router = Router()
admin_router.message.filter(ChatTypeFilter(["private"]),IsAdmin())


ADMIN_KB = get_keyboard(
    "Добавить вопрос",
    "Список вопросов",
    placeholder= "Выберите действие",
    sizes=(2,),
)

GO_BACK_KB = get_keyboard(
    "Назад",
    "Отмена",
    sizes=(2,),
)

SKIP_KB = get_keyboard(
    "Назад",
    "Отмена",
    "Пропустить",
    sizes=(3,),
)

DELETE_PHOTO_KB= get_keyboard(
    "Назад",
    "Отмена",
    "Удалить фото",
    sizes=(3,),
)

class AddQuestion(StatesGroup):
    name = State()
    description = State()
    keywords = State()
    image = State()
    question_for_change = None
    texts = {
        'AddQuestion:name':'Введите название заново',
        'AddQuestion:description': 'Введите описание заново',
        'AddQuestion:keywords': 'Введите ключевые слова заново',
        'AddQuestion:image': '******',
    }

@admin_router.message(Command("admin"))
async def add_product(message: types.Message):
    await message.answer("Что хотите сделать?", reply_markup=ADMIN_KB)


@admin_router.message(F.text == "Список вопросов")
async def starring_at_product(message: types.Message, session: AsyncSession):
    for question in await orm_get_questions(session):
        if question.image:
            await message.answer_photo(
                question.image,
                caption=f"<strong>{question.name}\
                        </strong>\n{question.description}\nКлючевые слова: {question.keywords}",
                reply_markup=get_callback_btns(btns={
                    'Удалить': f'delete_{question.id}',
                    'Изменить': f'change_{question.id}',
                })
            )
        else:
            await message.answer(
                text=f"<strong>{question.name}\
                        </strong>\n{question.description}\nКлючевые слова: {question.keywords}",
                reply_markup=get_callback_btns(btns={
                    'Удалить': f'delete_{question.id}',
                    'Изменить': f'change_{question.id}',
                })
            )
    await message.answer("ОК, вот список вопросов")


@admin_router.callback_query(F.data.startswith('delete_'))
async def delete_question(callback: types.CallbackQuery, session: AsyncSession):
    question_id = callback.data.split("_")[-1]
    await orm_delete_question(session, int(question_id))
    await callback.answer("Вопрос удалён")
    await callback.message.answer("Вопрос удалён!")

#Код ниже для машины состояний (FSM)

@admin_router.callback_query(StateFilter(None), F.data.startswith("change_"))
async def change_question_callback(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    question_id = callback.data.split("_")[-1]

    question_for_change = await orm_get_question(session, int(question_id))

    AddQuestion.question_for_change = question_for_change
    await callback.answer()
    await callback.message.answer(
        "Введите название товара", reply_markup=GO_BACK_KB
    )
    await state.set_state(AddQuestion.name)







@admin_router.message(StateFilter(None),F.text == "Добавить вопрос")
async def add_product(message: types.Message, state: FSMContext):
    await message.answer(
        "Введите название вопроса", reply_markup=GO_BACK_KB
    )
    await state.set_state(AddQuestion.name)


@admin_router.message(StateFilter('*'), Command("Отмена"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "отмена")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    if AddQuestion.question_for_change:
        AddQuestion.question_for_change = None
    await state.clear()
    await message.answer("Действия отменены", reply_markup=ADMIN_KB)


@admin_router.message(StateFilter('*'), Command("Назад"))
@admin_router.message(StateFilter('*'), F.text.casefold() == "назад")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()

    if current_state == AddQuestion.name:
        await message.answer('Предыдущего шага нет, используйте команду "отмена"',  reply_markup=GO_BACK_KB)
        return

    previous = None
    for step in AddQuestion.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к прошлому шагу \n {AddQuestion.texts[previous.state]}")
            return
        previous = step




@admin_router.message(AddQuestion.name, or_f(F.text, F.text == "."))
async def add_name(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(name=AddQuestion.question_for_change.name)
    else:
        if len(message.text)>= 100:
            await message.answer(
                "Название вопроса не должно превышать 100 символов. \n Введите заново"
            )
            return

        await state.update_data(name=message.text)
    await message.answer("<b>Введите описание вопроса</b>", reply_markup=GO_BACK_KB)
    await state.set_state(AddQuestion.description)

@admin_router.message(AddQuestion.name)
async def add_name(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст названия товара", reply_markup=GO_BACK_KB)



@admin_router.message(AddQuestion.description, or_f(F.text, F.text == "."))
async def add_description(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(description=AddQuestion.question_for_change.description)
    else:
        await state.update_data(description=message.text)
    await message.answer("Введите ключевые слова", reply_markup=GO_BACK_KB)
    await state.set_state(AddQuestion.keywords)

@admin_router.message(AddQuestion.description)
async def add_description(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите текст описания товара", reply_markup=GO_BACK_KB)



@admin_router.message(AddQuestion.keywords, or_f(F.text, F.text == "."))
async def add_keywords(message: types.Message, state: FSMContext):
    if message.text == '.':
        await state.update_data(keywords=AddQuestion.question_for_change.keywords)
    else:
        await state.update_data(keywords=message.text)
    if AddQuestion.question_for_change:
        await message.answer("Загрузите изображение либо нажмите 'Удалить фото'", reply_markup=DELETE_PHOTO_KB)
    else:
        await message.answer("Загрузите изображение либо нажмите 'Пропустить'", reply_markup=SKIP_KB)
    await state.set_state(AddQuestion.image)

@admin_router.message(AddQuestion.keywords)
async def add_keywords(message: types.Message, state: FSMContext):
    await message.answer("Вы ввели недопустимые данные, введите ключевые слова для вопроса через запятую", reply_markup=GO_BACK_KB)


@admin_router.message(AddQuestion.image, or_f(F.text == "Пропустить", F.text == "Удалить фото"))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):
    await state.update_data(image=None)
    data = await state.get_data()
    try:
        if AddQuestion.question_for_change:
            await orm_update_question(session, AddQuestion.question_for_change.id, data)
        else:
            await orm_add_question(session, data)
        await message.answer("Вопрос добавлен", reply_markup=ADMIN_KB)
        await message.answer(str(data))
        await state.clear()
    except Exception as e:
        await message.answer(
            f"Ошибка добавления запроса \n{str(e)}\n",
            reply_markup=ADMIN_KB
        )
        await state.clear()


@admin_router.message(AddQuestion.image,  or_f(F.photo, F.text == "."))
async def add_image(message: types.Message, state: FSMContext, session: AsyncSession):

    if message.text and message.text == '.':
        await state.update_data(image=AddQuestion.question_for_change.image)
    else:
        await state.update_data(image=message.photo[-1].file_id)
    data = await state.get_data()
    try:
        if AddQuestion.question_for_change:
            await orm_update_question(session, AddQuestion.question_for_change.id, data)
        else:
            await orm_add_question_pic(session, data)
        await message.answer("Вопрос добавлен", reply_markup=ADMIN_KB)
        await message.answer(str(data))
        await state.clear()

    except Exception as e:
        await message.answer(
            f"Ошибка добавления запроса \n{str(e)}\n",
            reply_markup=ADMIN_KB
        )
        await state.clear()

    AddQuestion.question_for_change = None



@admin_router.message(AddQuestion.image)
async def add_image(message: types.Message, state: FSMContext):
    await message.answer('Вы ввели недопустимые данные, отправьте фотографию для вопроса, либо нажмите кнопку "пропустить"')



