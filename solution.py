from socket import *


def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"
    endmsg = "\r\n.\r\n"

    mail_server = ('127.0.0.1', 1025)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect(mail_server)

    recv = clientSocket.recv(1024).decode()
    # print('Received: ' + recv)
    # if recv[:3] != '220':
    #     print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    # print(recv1)
    # if recv1[:3] != '250':
    #     print('250 reply not received from server.')

    # Send MAIL FROM command and print server response.
    mail_from = 'MAIL FROM: <source@fakemail.com> \r\n'
    clientSocket.send(mail_from.encode())
    recv2 = clientSocket.recv(1024).decode()
    # print('MAIL FROM: ' + recv2)
    # if recv2[:3] != '250':
    #     print('250 reply not received from server.')

    # Send RCPT TO command and print server response.
    rcpt_to = 'RCPT TO: <destination@fakemail.com> \r\n'
    clientSocket.send(rcpt_to.encode())
    recv3 = clientSocket.recv(1024).decode()
    # print('RCPT TO: ' + recv3)
    # if recv3[:3] != '250':
    #     print('250 reply not received from server.')

    # Send DATA command and print server response.
    data_command = "DATA\r\n"
    recv4 = clientSocket.send(data_command.encode())
    # print('DATA: ' + recv4)
    # if recv4[:3] != '250':
    #     print('250 reply not received from server.')

    # Send message data.
    clientSocket.send(msg.encode())
    clientSocket.send(endmsg.encode())
    recv5 = clientSocket.recv(1024).decode()
    # print('endmsg sent: ' + recv5)
    # if recv5[:3] != '354':
    #     print('354 reply not received from server.')

    # Send QUIT command and get server response.
    clientSocket.send('QUIT\r\n'.encode())
    recv6 = clientSocket.recv(1024).decode()
    # print('QUIT:' + recv6)
    clientSocket.close()


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
