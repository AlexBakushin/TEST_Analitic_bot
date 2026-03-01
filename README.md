***TEST_Analitic_bot***
===

Это Telegram-бота, который умеет по запросу на естественном языке считать нужные метрики по базе данных.

---
**Ход работы:**
-
1. Введите запрос к БД -- писать можно как угодно на человесвок языке
---
После отправки запроса и раздумывания ИИ вы получите ответ ввиде целого чиста
````
Сам бот работает очень просто, ИИ получает промт в котором описаны все правила ответ - чистый SQL без всего лишнего и 
описание схемы таблиц БД, ИИ сам анализирет и в ответ отдает готовый sql кодЮ который после простой валидации
отправляется в БД
В ответ просто отправляется первое что пришло от БД на запрос
````

---
**Развертывание бота:**

Бот развертывается в докер контейнере
Для правильного запуска вам необходимо прописать свои данные в `.env `файл
Пример прописан в  `.env_exemple`
После можно разворачивать докер контейнер

1. Запустите Docker Desctop
2. В дериктрии с 'docker-compose.yml' запустите команду `docker compose build` для сборки образа
3. После сборки введите команду `docker compose up` для запуска образа
4. После запуска бот инициализирует БД и импортирует загруженный json файл, после этого бот готов к работе


Промт для ИИ

```
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
```
Модель ИИ - `stepfun/step-3.5-flash:free`
