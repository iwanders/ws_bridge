
# The MIT License (MIT)
#
# Copyright (c) 2018 Ivor Wanders
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import asyncio
import websockets

try:
    from asyncio import ensure_future
except ImportError:
    from asyncio import async as ensure_future

class TCPServerToWsClient:
    """
        Tcp server, websocket client
    """
    def __init__(self, ws_ip="localhost", ws_port=8001, tcp_ip="localhost",
                 tcp_port=8000, path="", chunk_size=1024):
        self.ws_ip = ws_ip
        self.ws_port = ws_port
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.chunk_size = chunk_size
        self.path = path

    def server(self):
        return asyncio.start_server(self.handler, self.tcp_ip, self.tcp_port)

    @asyncio.coroutine
    def handler(self, reader, writer):
        websocket = yield from websockets.connect('ws://{:s}:{:d}/{:s}'.format(
                                                  self.ws_ip, self.ws_port,
                                                  self.path))

        consumer_task = ensure_future(self.consumer_handler(reader, websocket))
        producer_task = ensure_future(self.producer_handler(writer, websocket))

        done, pending = yield from asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    @asyncio.coroutine
    def consumer_handler(self, reader, websocket):
        try:
            while True:
                message = yield from reader.read(self.chunk_size)
                if reader.at_eof():
                    break
                yield from websocket.send(message)
        finally:
            ensure_future(websocket.close())
            reader.feed_eof()

    @asyncio.coroutine
    def producer_handler(self, writer, websocket):
        try:
            while True:
                message = yield from websocket.recv()
                writer.write(message)
                yield from writer.drain()
        finally:
            ensure_future(websocket.close())
            writer.close()
