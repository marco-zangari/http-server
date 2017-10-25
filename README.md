# HTTP-SERVER
Server and client built with Python sockets

**Author**: Megan Flood, Marco Zangari
**Version**: 2.0.0

## Overview
To make a simple http server and client to receive http requests and send http responses.

## Getting Started
To get started, use:
```
pip install http-server
```
Start the server with:
```
python server.py
```
In a separate terminal send messages with:
```
python client.py <add your message>
```

## Architecture
Written in python, tested with pytest and tox.

## Change Log
**10-25-2017 3:33pm** - Rebuilt server to send either an http OK 200 response or an http 500 Internal Server Error response

**10-24-2017 2:44pm** - Built server and client with functionality to echo messages.