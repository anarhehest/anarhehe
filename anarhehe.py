import os
import random
import time
from dotenv import load_dotenv
from telethon.errors import FloodError
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights

load_dotenv()

_l = {
    'dict': { 'bool': lambda c,v: c(**{k: v for k in c().to_dict().keys() if k != '_'})},
    'os': { 'file': lambda: os.path.basename(__file__).strip('\\').split('.')[0],}, 
    'time': { 'range': lambda a=.12,b=.358,p=0: (a*10**p, b*10**p),}
}

_l['time'].update({'sleep': lambda p=0: time.sleep(random.uniform(*_l['time']['range'](p=p))),})

_l.update({ 'fstr': {
    'link': lambda: f'https://t.me/{_l["os"]["file"]()}',
    'rank': lambda: f'{_l["os"]["file"]()}st',
}})

cfg = { 'client': {
    'session': _l['os']['file'](),
    'api_id': os.getenv('API_ID'),
    'api_hash': os.getenv('API_HASH'),
}, 'request': {
    'admin_rights': _l['dict']['bool'](ChatAdminRights, True),
    'rank': _l['fstr']['rank'](),
}}

with TelegramClient(**cfg['client']) as c:
    cfg['request'].update({'channel': c.get_entity(_l['fstr']['link']())})
    try:
        for u in c.get_participants(cfg['request']['channel']):
            cfg['request'].update({'user_id': u.id})
            c(EditAdminRequest(**cfg['request']))
            _l['time']['sleep'](p=1)
    except FloodError:
        _l['time']['sleep'](p=3)