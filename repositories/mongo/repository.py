import asyncio

from configparser import ConfigParser
import pymongo
from bson import ObjectId
from pymongo.collection import Collection
from pymongo.cursor import Cursor
from pymongo.results import InsertOneResult

config = ConfigParser()

config.read("secrets/secrets.cfg")

db_user = config["Default"]["DB_USER_2"]
db_password = config["Default"]["DB_PASSWORD_2"]
db_uri = config["Default"]["DB_URI"]


def repository(func: ()):
    def _wrapper(*args, **kwargs):
        with pymongo.MongoClient(db_uri.format(db_user, db_password)) as client:
            db: pymongo = client.DiscordBots.swrpgbot
            response = func(db, *args, **kwargs)
        return response
    return _wrapper


@repository
def test(db: Collection):
    user = {
        "name": "Alex Buchanan",
        "discord_id": "123412341423",
        "discord_server": "SWPRGDiceRollerBot",
    }

    post_response: InsertOneResult = db.insert_one(user)
    post_id: ObjectId = post_response.inserted_id

    result: Cursor = db.find({"_id": post_id})
    for res in result:
        print(res)
        db.delete_one({"_id": res["_id"]})


if __name__ == "__main__":
    test()
