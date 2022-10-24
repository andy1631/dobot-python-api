from logging import getLogger
from time import sleep


from .api import *

_log = getLogger(__name__)


class Dobot:
   def __init__(self, port: Optional[str] = None):
       connect(port)
