# C TCP Chat Application

A multi-client TCP chat server and client built in C using POSIX sockets and pthreads.

## Project Structure

```
├── c-socketUtils/      # Shared socket utility library
│   ├── socketutil.h    # Header with struct/function declarations
│   └── socketutil.c    # Socket helper implementations
├── c-server-socket/    # TCP chat server
│   ├── main.c          # Server entry point
│   └── Makefile
├── c-client-socket/    # TCP chat client
│   ├── main.c          # Client entry point
│   └── Makefile
```

## Features

- Multi-client support (up to 10 simultaneous connections)
- Real-time message broadcasting to all connected clients
- Client name display with messages
- Threaded architecture for non-blocking I/O

## Prerequisites

- GCC compiler
- Linux/WSL (POSIX sockets)
- pthreads library

## How to Build

**Build the server:**
```bash
cd c-server-socket
make
```

**Build the client:**
```bash
cd c-client-socket
make
```

## How to Run

**1. Start the server:**
```bash
cd c-server-socket
./server.exe
```

**2. Start one or more clients (in separate terminals):**
```bash
cd c-client-socket
./client.exe
```

**3. Enter your name and start chatting!**

Type `exit` to disconnect a client and shut down the server.
