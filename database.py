import aiosqlite

class Database:
    def __init__(self, db_name="tasks.db"):
        self.db_name = db_name

    async def init(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                "CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, task_text TEXT)"
            )
            await db.commit()

    async def add_task(self, user_id, text):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("INSERT INTO tasks (user_id, task_text) VALUES (?, ?)", (user_id, text))
            await db.commit()

    async def get_tasks(self, user_id):
        async with aiosqlite.connect(self.db_name) as db:
            async with db.execute("SELECT id, task_text FROM tasks WHERE user_id = ?", (user_id,)) as cursor:
                return await cursor.fetchall()

    async def delete_task(self, task_id):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            await db.commit()
