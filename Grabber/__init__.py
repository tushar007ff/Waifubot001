import logging  

from pyrogram import Client 

from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

OWNER_ID = 1826484283
sudo_users = ["6769261147", "1826484283"]
GROUP_ID = -1002126546106
TOKEN = "6764429942:AAFo6cjU3BcbBvQDvqdvcxv4LvAfrgPBGlw"
mongo_url = "mongodb+srv://itachi123:itachi123@cluster0.q08jjzp.mongodb.net/?retryWrites=true&w=majority"
PHOTO_URL = ["https://telegra.ph/file/72ea883532b722f405059.jpg", "https://telegra.ph/file/72ea883532b722f405059.jpg"]
SUPPORT_CHAT = "warzone_123"
UPDATE_CHAT = "warzone_123"
BOT_USERNAME = "Mei_pro_robot"
CHARA_CHANNEL_ID =-1002126546106
api_id = 28509005
api_hash = "dc43ab3927d0c4da0067ee3100ea2f08"


application = Application.builder().token(TOKEN).build()
Grabberu = Client("Grabber", api_id, api_hash, bot_token=TOKEN)
client = AsyncIOMotorClient(mongo_url)
db = client['Character_catcher']
collection = db['anime_characters']
user_totals_collection = db['user_totals']
user_collection = db["user_collection"]
group_user_totals_collection = db['group_user_total']
top_global_groups_collection = db['top_global_groups']



