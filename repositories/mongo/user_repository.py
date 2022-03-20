from bson import ObjectId
from discord.ext.commands import Context
from pymongo.collection import Collection, ReturnDocument
from pymongo.results import InsertOneResult

from models.User import User
from repositories.mongo.repository import repository


@repository
def add_user(db: Collection, user_information: dict) -> ObjectId:
    new_user_id: InsertOneResult = db.insert_one(user_information)
    return new_user_id.inserted_id


@repository
def update_user(db: Collection, user_information: dict) -> dict:
    updated_user: dict = db.find_one_and_update(
        {"_id": user_information["_id"]},
        {"$set": user_information},
        return_document=ReturnDocument.AFTER,
    )
    return updated_user


@repository
def get_user_by_discord_id_and_guild(
    db: Collection, user_id: str, guild_id: str
) -> dict:
    existing_user: dict = db.find_one({"id": user_id, "guild_id": guild_id})
    return existing_user


@repository
def get_user_by_id(db: Collection, user_id: ObjectId) -> dict:
    existing_user: dict = db.find_one({"_id": user_id})
    return existing_user


@repository
def get_or_add_user_from_context(db: Collection, ctx: Context) -> dict:
    existing_user = get_user_by_discord_id_and_guild(ctx.author.id, ctx.guild.id)

    if existing_user is None:
        new_user = add_user(User(ctx.author).convert_to_dict())
        existing_user = get_user_by_id(new_user)

    return existing_user
