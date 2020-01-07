import os
from dotenv import load_dotenv
from app.utils.cache import Cache
from app import ApplicationFactory

load_dotenv()

with open('./AppleMusicAuthKey.p8', 'r') as f:
    os.environ['APPLE_KEY'] = f.read()

TITLE = 'Sharify'
DESCRIPTION = ''
DEBUG = os.environ.get('APP_DEBUG') or False

Cache.instance().init()
app = ApplicationFactory(TITLE, DESCRIPTION).create(debug=DEBUG)
