import asyncio
import sys

from ElinaRobot import log
from motor import motor_asyncio
from ElinaRobot import MONGO_DB_URI 
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from ElinaRobot.conf import get_int_key, get_str_key


MONGO_PORT = get_int_key("27017")
MONGO_DB_URI = get_str_key("MONGO_DB_URI")
MONGO_DB = "ElinaRobot"


client = MongoClient()
client = MongoClient(MONGO_DB_URI, MONGO_PORT)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URI, MONGO_PORT)
db = motor[MONGO_DB]
db = client["ElinaRobot"]
try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(log.critical("» 𝙲𝙰𝙽'𝚃 𝙲𝙾𝙽𝙽𝙴𝙲𝚃 𝚃𝙾 𝙼𝙾𝙽𝙶𝙾𝙳𝙱 𝙴𝚇𝙸𝚃𝙸𝙽𝙶 •••"))
