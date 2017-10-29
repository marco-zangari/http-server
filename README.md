# HTTP-SERVER
Server and client built with Python sockets

**Author**: Megan Flood, Marco Zangari

**Version**: 4.1.1

## Overview
To make a simple blocking http server and client to receive http requests and send http responses. Also to make a simple concurrent http server using gevent.

## Getting Started
To get started, use:
```
pip install http-server
```
Start the blocking server with:
```
python server.py
```
Start the concurrent server with:
```
python concurrent_server.py
```
In a separate terminal send HTTP requests with:
```
python client.py <add your request>
```

## Architecture
Written in Python, built using gevent, tested with pytest and tox.

## Change Log
**10-29-2017 9:50pm** - Refactored resolution of URI to improve security

**10-29-2017 7:46pm** - Concurrent server module added, built using gevent

**10-29-2017 6:00pm** - Server responds with files requested through HTTP GET requests

**10-27-2017 4:06pm** - Server now requires properly formatted HTTP requests

**10-25-2017 3:33pm** - Rebuilt server to send either an http OK 200 response or an http 500 Internal Server Error response

**10-24-2017 2:44pm** - Built server and client with functionality to echo messages.

## Resources
Python [OS Module Docs](https://docs.python.org/3/library/os.html)

Jeremy Allen: Checking that a string can be parsed as an http response, [StackOverflow](https://stackoverflow.com/questions/24728088/python-parse-http-response-string/24729316#24729316)