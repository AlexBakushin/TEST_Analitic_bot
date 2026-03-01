import json
import os
from datetime import datetime, timezone
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DB_PATH = "analytics.db"
POSTGRES_URI = os.getenv("POSTGRES_URI", "postgresql://admin:postgres@localhost:5432/analytics_db")


async def init_db():
    """Инициальзация БД"""
    conn = await asyncpg.connect(POSTGRES_URI)
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id TEXT PRIMARY KEY,
            creator_id TEXT,
            video_created_at TIMESTAMP,
            views_count INTEGER,
            likes_count INTEGER,
            comments_count INTEGER,
            reports_count INTEGER,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        );
    """)

    await conn.execute("""
        CREATE TABLE IF NOT EXISTS video_snapshots (
            id TEXT PRIMARY KEY,
            video_id TEXT REFERENCES videos(id),
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
        );
    """)
    await conn.close()


def parse_datetime(dt_str):
    """Форматирование дат"""
    if dt_str is None:
        return None
    dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).replace(tzinfo=None)


async def load_json_to_db(json_file):
    """Импорт json в БД"""
    conn = await asyncpg.connect(POSTGRES_URI)

    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)

    for video in data["videos"]:
        vid = video["id"]
        await conn.execute("""
            INSERT INTO videos(
                id, creator_id, video_created_at, views_count, likes_count, 
                comments_count, reports_count, created_at, updated_at
            )
            VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9)
            ON CONFLICT (id) DO NOTHING;
        """,
           vid,
           video["creator_id"],
           parse_datetime(video["video_created_at"]),
           video["views_count"],
           video["likes_count"],
           video["comments_count"],
           video["reports_count"],
           parse_datetime(video["created_at"]),
           parse_datetime(video["updated_at"])
           )

        for snap in video["snapshots"]:
            await conn.execute("""
                INSERT INTO video_snapshots(
                    id, video_id, views_count, likes_count, comments_count, reports_count,
                    delta_views_count, delta_likes_count, delta_comments_count, delta_reports_count,
                    created_at, updated_at
                )
                VALUES($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12)
                ON CONFLICT (id) DO NOTHING;
            """,
               snap["id"],
               vid,
               snap["views_count"],
               snap["likes_count"],
               snap["comments_count"],
               snap["reports_count"],
               snap["delta_views_count"],
               snap["delta_likes_count"],
               snap["delta_comments_count"],
               snap["delta_reports_count"],
               parse_datetime(snap["created_at"]),
               parse_datetime(snap["updated_at"])
               )
    await conn.close()


def validate_sql(sql: str) -> bool:
    """Валидация sql ответа от ИИ"""
    sql_lower = sql.strip().lower()
    if not sql_lower.startswith("select"):
        return False
    forbidden = ["delete", "insert", "update", "drop", "alter"]
    return not any(f in sql_lower for f in forbidden)


async def execute_sql_and_get_number(sql: str):
    """Применение sql от ИИ в БД"""
    conn = await asyncpg.connect(POSTGRES_URI)
    try:
        row = await conn.fetchrow(sql)
        if row is None:
            return 0
        return row[0]
    finally:
        await conn.close()
