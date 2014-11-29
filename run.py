import logging
logging.basicConfig(level=logging.DEBUG)

import asyncio

from gsc.wrapper import ServerWrapper

asyncio.get_event_loop().set_debug(True)
wrapper = ServerWrapper()
wrapper.run()
