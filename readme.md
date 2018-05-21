# ws_bridge

This module provides a way transfer a tcp connection through a websocket.

Original use case is to expose access to [music player daemon][mpd]'s
remote control port over a HTTP proxy.

## Example
A simple example to explain potential use, using just one machine and `nc` to
create a dummy 'server' and 'client'.

```bash
# Start a dummy tcp server:
# This listens for tcp connections on 127.0.0.1:8000.
nc -l 127.0.0.1 8000

# Next, we run the websocket server to tcp client.
# This listens to websocket connections at 127.0.0.1:8001
# When a connection is opened it connects to 127.0.0.1:8000 over tcp.
python3 -m ws_bridge ws_server_to_tcp_client

# Next, we run the tcp server to websocket client.
# This listens to tcp connections on 127.0.0.1:8002.
# When a connection is opened it opens a websocket connection to 127.0.0.1:8001
python3 -m ws_bridge tcp_server_to_ws_client --tcp-port 8002

# Next, we can create a dummy client.
# This creates a tcp connection to 127.0.0.1:8002
nc 127.0.0.1 8002

# Now we have the following connections.
# client (tcp://127.0.0.1:8002) -> tcp_server_to_ws_client
# tcp_server_to_ws_client (ws://127.0.0.1:8001/) -> ws_server_to_tcp_client
# ws_server_to_tcp_client (tcp://127.0.0.1:8000) -> server
```

The bytes sent through the dummy client are converted into websocket traffic
by the `tcp_server_to_ws_client`, this opens a websocket to the 
`ws_server_to_tcp_client` part of the bridge, which converts it back to tcp
and connects to the dummy server. Bytes send from the dummy server are 
passed all the way back to the dummy client, over the same websocket.

All hostnames, ports and the websocket path can be modified through commandline
arguments.

## Requirements
This module makes use of the [websockets][websockets] library and makes use of
[asyncio][asyncio]. Tested on Python 3.4.3, 3.5.

## License

MIT License, see [LICENSE](LICENSE).

[mpd]: https://www.musicpd.org/
[websockets]: http://websockets.readthedocs.io/en/stable/
[asyncio]: https://docs.python.org/3/library/asyncio.html
