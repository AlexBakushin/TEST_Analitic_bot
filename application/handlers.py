from aiogram import Router
from aiogram.types import Message
from ai import make_openrouter_request
from database import validate_sql, execute_sql_and_get_number

router = Router()


@router.message()
async def echo(message: Message):
    full_response = await make_openrouter_request(message)
    try:
        sql = full_response["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        sql = "ERROR"
    print(sql)
    if validate_sql(sql):
        resp = await execute_sql_and_get_number(sql)
    else:
        resp = "ERROR"
    await message.answer(str(resp))
