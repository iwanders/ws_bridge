
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

if hasattr(asyncio, 'ensure_future'):
    ensure_future = asyncio.ensure_future
else:  # Deprecated since Python 3.4.4
    ensure_future = getattr(asyncio, "async")

class WsServerToTCPClient:
    """
        Websocket server to tcp client.
    """
    def __init__(self, ws_ip="localhost", ws_port=8001, tcp_ip="localhost",
                 tcp_port=8000, chunk_size=1024):
        self.ws_ip = ws_ip
        self.ws_port = ws_port
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.chunk_size = chunk_size


    def server(self):
        return websockets.serve(self.handler, self.ws_ip, self.ws_port)

    @asyncio.coroutine
    def handler(self, websocket, path):
        reader, writer = yield from asyncio.open_connection(self.tcp_ip,
                                                            self.tcp_port)

        consumer_task = ensure_future(self.consumer_handler(websocket, writer))
        producer_task = ensure_future(self.producer_handler(websocket, reader))

        done, pending = yield from asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    @asyncio.coroutine
    def consumer_handler(self, websocket, writer):
        try:
            while True:
                try:
                    message = yield from websocket.recv()
                except websockets.exceptions.ConnectionClosed as e:
                    break
                writer.write(message)
                yield from writer.drain()
        finally:
            ensure_future(websocket.close())
            writer.close()

    @asyncio.coroutine
    def producer_handler(self, websocket, reader):
        try:
            while True:
                message = yield from reader.read(self.chunk_size)
                yield from websocket.send(message)
        finally:
            yield from websocket.close()
            reader.close()
