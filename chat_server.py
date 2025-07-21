"""
Write a socket-server chat-server that accepts clients that connect to it over TCP. You may not remember raw sockets and need to look it up: that's fine! 

Write test cases as well.
"""
import asyncio

# defining a global set to track connected clients. this will store each
# clients writer stream
clients = set()

#create a coroutine to handle new clients.

async def handle_client(reader, writer):
    addr = writer. get_extra_info('peername')
    print(f"[+] New connection fro {addr}")
    clients.add(writer)

    try:
        while True:
            data = await reader.readline()
            if not data:
                break
            message = data.decode().strip()
            print(f"[{addr}] {message}")

            #Broadcast to all other clients
            for client in clients:
                if client is not writer:
                    client.write(f"[{addr}] {message}\n".encode())
                    await client.drain()
    except Exception as e:
         print(f"[!]Error: {e}")
    
    finally:
        print(f"[-] Connection closed: {addr}")
        clients.remove(writer)
        writer.close()
        await writer.wait_closed()


#add server startup logic

async def main():
    server = await asyncio.start_server(handle_client, '0.0.0.0', 8880)
    addr = server.sockets[0].getsockname()
    print(f" Server started on {addr}")

    async with server:
        await server.serve_forever()

if __name__== "__main__":
    asyncio.run(main())
    