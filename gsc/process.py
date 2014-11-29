import asyncio
import codecs
import logging

logger = logging.getLogger('process')

class StdStream:
    def __init__(self, encoding, errors='replace'):
        self.buffer_ = ''
        self.decoder = codecs.getincrementaldecoder(encoding)(errors)

    def feed_data(self, data):
        self.buffer_ += self.decoder.decode(data)

    def get_lines(self):
        *lines, self.buffer_ = self.buffer_.split('\n')
        return lines

class ProcessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, wrapper):
        self.wrapper = wrapper
        self.stdout = StdStream('utf8')
        self.stderr = StdStream('utf8')

    @classmethod
    def factory(cls, wrapper):
        def factory():
            return cls(wrapper)
        return factory

    def connection_made(self, transport):
        self.process = transport

    def ev_write(self, data):
        self.process.write(data['data'].encode(encoding))

    def ev_kill(self, data):
        self.process.send_signal(data['signal'])

    def pipe_data_received(self, fd, data):
        if fd == 1:
            typ = 'stdout'
            stream = self.stdout
        else:
            typ = 'stderr'
            stream = self.stderr
        stream.feed_data(data)
        for line in stream.get_lines():
            self.wrapper.process_output(self, typ, line)

    def process_exited(self):
        self.wrapper.process_exited(self, self.process.get_returncode())
