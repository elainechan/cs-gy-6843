from socket import *
import sys

def webServer(port=13331):
    REQUEST_URL = 'http://127.0.0.1:13331/helloworld.html'
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('127.0.0.1', port))
    serverSocket.listen(5)

    while True:
        # print('Ready to serve...')
        connectionSocket, addr = serverSocket.accept()
        try:
            try:
                message = connectionSocket.recv(1024).decode()
                filename = message.split()[1]
                f = open(filename[1:])
                outputdata = f.read()

                #Send one HTTP header line into socket.
                OK_CONTENT = b'''HTTP/1.1 200 OK\r\nContent-Type: text/html\n\n'''
                OK = b'''HTTP/1.1 200 OK\r\n\r\n'''
                connectionSocket.sendall(OK_CONTENT)
                connectionSocket.sendall(OK)

                #Send the content of the requested file to the client
                for i in range(0, len(outputdata)):
                    connectionSocket.send(outputdata[i].encode())
                connectionSocket.send('\r\n'.encode())
                connectionSocket.close()
            except IOError:
                # Send response message for file not found (404)
                NOT_FOUND_CONTENT = b'''HTTP/1.1 404 Not Found\r\nContent-Type: text/html\n\n'''
                NOT_FOUND = b'''HTTP/1.1 404 Not Found\r\n'''
                connectionSocket.sendall(NOT_FOUND_CONTENT)
                connectionSocket.sendall(NOT_FOUND)

                # Close client socket
                connectionSocket.close()
        except (ConnectionResetError, BrokenPipeError):
            connectionSocket.close()
        except (KeyboardInterrupt):
            try:
                if connectionSocket:
                    connectionSocket.shutdown()
                    connectionSocket.close()
                if serverSocket:
                    serverSocket.shutdown()
                    serverSocket.close()
                sys.exit()
            except: pass
            break
    serverSocket.close()
    sys.exit()

if __name__ == '__main__':
    webServer(13331)