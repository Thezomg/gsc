import asyncio
from .process import ProcessProtocol

import logging

logger = logging.getLogger('wrapper')

class ServerWrapper(object):
    """
    Server wrapper class manages all of the servers
    """

    def __init__(self):
        self.servers = []

    @asyncio.coroutine
    def start_server_process(self, command):
        loop = asyncio.get_event_loop()
        factory = ProcessProtocol.factory(self)
        transport, process = yield from loop.subprocess_exec(factory, *command)
        logger.debug("Started server process")
        self.servers.append(process)

        return transport.get_pid()

    def process_output(self, process, typ, data):
        logger.debug("{}: {}".format(typ, data))

    def process_exited(self, process, return_code):
        if process in self.servers:
            self.servers.remove(process)

        logging.debug("Process {} closed with code {}".format(process, return_code))

    def run(self):
        asyncio.async(self.start_server_process(["python", "-u", "test.py"]))
        asyncio.get_event_loop().run_forever()
