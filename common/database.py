import uuid

from pymongo import MongoClient
from pymongo.collection import Collection

from config import Config


class Mongo(object):
    default_db: str
    db: MongoClient

    def __init__(self, host: str = None, port: int = None, default_db: str = None, **kwargs):
        self.db = MongoClient(host, port, **kwargs)
        self.default_db = default_db

    def get_db(self, col: str, db: str = None) -> Collection:
        if db is None:
            db = self.default_db
        return self.db.get_database(db).get_collection(col)


MONGODB = Mongo(Config.MONGODB_HOST, Config.MONGODB_PORT, Config.MONGODB_DEFAULT_DB)


def get_uuid() -> str:
    return str(uuid.uuid4())
