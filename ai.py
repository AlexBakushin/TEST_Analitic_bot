import aiohttp
import os
from dotenv import load_dotenv


load_dotenv()
AI_TOKEN = os.getenv("AI_TOKEN")


async def make_openrouter_request(user_text):
    """Функция с запросом к ИИ и промптом"""
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
      "Authorization": f"Bearer {AI_TOKEN}",
      "Content-Type": "application/json",
    }
    context = f"""
        Ты — SQL-генератор:  
        Дана PostgreSQL схема:
        
        videos(
            id TEXT PRIMARY KEY,
            creator_id TEXT,
            video_created_at TIMESTAMP,
            views_count INTEGER,
            likes_count INTEGER,
            comments_count INTEGER,
            reports_count INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        video_snapshots(
            id TEXT PRIMARY KEY,
            video_id TEXT,
            views_count INTEGER,
            likes_count INTEGER,
            comments_count INTEGER,
            reports_count INTEGER,
            delta_views_count INTEGER,
            delta_likes_count INTEGER,
            delta_comments_count INTEGER,
            delta_reports_count INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        База данных именно PostgreSQL.
        Пользователь задаёт вопрос на русском.  
        Сгенерируй **безопасный SQL SELECT**, который возвращает **ровно одно числовое значение** по этим таблицам.  
        Ни в коем случае не модифицируй базу (только SELECT).  
        Если запрос не может быть правильно преобразован — верни «ERROR: Cannot convert».
        Ответ отдавай без ```sql``` и без пояснений — только чистый SQL.
        
        === ВОПРОС ===
        {user_text}
    """

    data = {
      "model": "stepfun/step-3.5-flash:free",
      "messages": [
        {
          "role": "user",
          "content": context
        }
      ],
      "reasoning": {"enabled": True}
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            return await response.json()
