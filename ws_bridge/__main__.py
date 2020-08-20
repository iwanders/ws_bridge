#!/usr/bin/env python3

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

import sys
import asyncio
import argparse
from .ws_to_tcp import WsServerToTCPClient
from .tcp_to_ws import TCPServerToWsClient

def run_ws_to_tcp(args):
    z = WsServerToTCPClient(ws_ip=args.ws_host, ws_port=args.ws_port,
                            tcp_ip=args.tcp_address, tcp_port=args.tcp_port,
                            chunk_size=args.chunk_size, text_mode=args.text_mode)

    asyncio.get_event_loop().run_until_complete(z.server())
    asyncio.get_event_loop().run_forever()
        
def run_tcp_to_ws(args):
    z = TCPServerToWsClient(ws_ip=args.ws_address, ws_port=args.ws_port,
                            tcp_ip=args.tcp_host, tcp_port=args.tcp_port,
                            path=args.ws_path, chunk_size=args.chunk_size,
                            text_mode=args.text_mode)

    asyncio.get_event_loop().run_until_complete(z.server())
    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":

    # argument parsing
    parser = argparse.ArgumentParser(prog="ws_bridge",
        description="ws_bridge: tcp server to websocket client,  "
                    "websocket server to tcp client."
        )
    parser.add_argument("-d", "--debug", action="store_true",
                        help="Enable debug mode in asyncio's event loop.")

    subparsers = parser.add_subparsers(dest="command")


    ws_to_tcp = subparsers.add_parser("ws_server_to_tcp_client",
                                        help="Websocket server to tcp client")
    ws_to_tcp.set_defaults(func=run_ws_to_tcp)
    ws_to_tcp.add_argument("--ws-host", default="0.0.0.0",
                           help="The websocket server hostname / ip to bind"
                                " (default: %(default)s).")
    ws_to_tcp.add_argument("--ws-port", default=8001, type=int,
                           help="The websocket server port."
                                "(default: %(default)s)")

    ws_to_tcp.add_argument("--tcp-address", default="127.0.0.1",
                           help="The address to connect the tcp client to."
                                "(default: %(default)s)")
    ws_to_tcp.add_argument("--tcp-port", default=8000, type=int,
                           help="The port to connect to."
                                "(default: %(default)s)")

    ws_to_tcp.add_argument("--chunk-size", default=4096, type=int,
                           help="The chunk size to chunk the stream by."
                                "(default: %(default)s)")
    ws_to_tcp.add_argument("--text-mode", action="store_true", default=False,
                           help="Output text messages to the websocket. "
                                " Default is binary messages.")
    

    tcp_to_ws = subparsers.add_parser("tcp_server_to_ws_client",
                                      help="TCP server to websocket client.")
    tcp_to_ws.set_defaults(func=run_tcp_to_ws)
    tcp_to_ws.add_argument("--tcp-host", default="0.0.0.0",
                           help="The tcp server hostname / ip to bind."
                                "(default: %(default)s)")
    tcp_to_ws.add_argument("--tcp-port", default=8000, type=int,
                           help="The port to bind to."
                                "(default: %(default)s)")

    tcp_to_ws.add_argument("--ws-address", default="127.0.0.1",
                           help="The websocket address to connect to"
                                " (default: %(default)s).")
    tcp_to_ws.add_argument("--ws-port", default=8001, type=int,
                           help="The websocket server port."
                                "(default: %(default)s)")
    tcp_to_ws.add_argument("--ws-path", default="/",
                           help="The path to use open the websocket.")
    tcp_to_ws.add_argument("--chunk-size", default=4096, type=int,
                           help="The chunk size to chunk the stream by."
                                "(default: %(default)s)")
    tcp_to_ws.add_argument("--text-mode", action="store_true", default=False,
                           help="Output text messages to the websocket. "
                                " Default is binary messages.")

    args = parser.parse_args()
    if (args.debug):
        asyncio.get_event_loop().set_debug(True)

    # no command, print help
    if (args.command is None):
        parser.print_help()
        parser.exit()
        sys.exit(1)

    args.func(args)
    sys.exit()
