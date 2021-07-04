from pydantic import BaseModel
from random import randrange, choice


DEVICE_TYPES = ('emeter', 'zigbee', 'lora', 'gsm')


class Device(BaseModel):
    dev_type: str
    dev_id: str


def random_mac(length=6):
    return ''.join(format(randrange(256), 'x') for _ in range(length))


def device(count=None):
    if count is None or count < 1:
        count = 1
    for _ in range(count):
        yield Device(dev_type=choice(DEVICE_TYPES), dev_id=random_mac())
