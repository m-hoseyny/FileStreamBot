

import datetime
import motor.motor_asyncio


class Database:
    def __init__(self, uri, database_name):
        # self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        # self.db = self._client[database_name]
        # self.col = self.db.users
        pass

    def new_user(self, id):
        return
        return dict(
            id=id,
            join_date=datetime.date.today().isoformat()
        )

    async def add_user(self, id):
        return
        user = self.new_user(id)
        await self.col.insert_one(user)

    async def is_user_exist(self, id):
        return
        user = await self.col.find_one({'id': int(id)})
        return True if user else False

    async def total_users_count(self):
        return
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        return
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        return
        await self.col.delete_many({'id': int(user_id)})
