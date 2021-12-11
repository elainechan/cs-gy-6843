from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT = 2.0
TRIES = 1
# The packet that we shall send to each router along the path is the ICMP echo
# request packet, which is exactly what we had used in the ICMP ping exercise.
# We shall use the same packet that we built in the Ping exercise

def checksum(string):
# In this function we make the checksum of our packet
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0

    while count < countTo:
        thisVal = (string[count + 1]) * 256 + (string[count])
        csum += thisVal
        csum &= 0xffffffff
        count += 2

    if countTo < len(string):
        csum += (string[len(string) - 1])
        csum &= 0xffffffff

    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def build_packet():
    #Fill in start
    # In the sendOnePing() method of the ICMP Ping exercise ,firstly the header of our
    # packet to be sent was made, secondly the checksum was appended to the header and
    # then finally the complete packet was sent to the destination.

    # Make the header in a similar way to the ping exercise.
    # Append checksum to the header.
    my_checksum = 0
    packet_id = os.getpid() & 0xFFFF
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, packet_id, 1)
    data = struct.pack("d", time.time())
    my_checksum = checksum(header + data)
    
    if sys.platform == "darwin":
        my_checksum = htons(my_checksum) & 0xffff
    else:
        my_checksum = htons(my_checksum)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, my_checksum, packet_id, 1)
    packet = header + data
    # Don’t send the packet yet , just return the final packet in this function.
    #Fill in end
    return packet

    # So the function ending should look like this

def get_route(hostname):
    timeLeft = TIMEOUT 
    tracelist2 = [] #This is your list to contain all traces

    for ttl in range(1,MAX_HOPS):
        for tries in range(TRIES):
            tracelist1 = [] #This is your list to use when iterating through each trace
            
            destAddr = gethostbyname(hostname)

            #Fill in start
            # Make a raw socket named mySocket
            mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
            mySocket.settimeout(TIMEOUT)
            mySocket.bind(("", 0))
            #Fill in end

            mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
            mySocket.settimeout(TIMEOUT)
            try:
                d = build_packet()
                mySocket.sendto(d, (hostname, 0))
                t = time.time()
                startedSelect = time.time()
                whatReady = select.select([mySocket], [], [], timeLeft)
                howLongInSelect = (time.time() - startedSelect)
                if whatReady[0] == []: # Timeout
                    #Fill in start
                    #You should add the list above to your all traces list
                    tracelist1.append("* * * Request timed out.")
                    tracelist2.append(tracelist1)
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                
                timeReceived = time.time()
                rtt = str(int(round((timeReceived - startedSelect) * 1000, 0))) + "ms"
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    #Fill in start
                    #You should add the list above to your all traces list
                    tracelist1.append("* * * Request timed out.")
                    tracelist2.append(tracelist1)
                    #Fill in end
            except timeout:
                continue

            else:
                #Fill in start
                #Fetch the icmp type from the IP packet
                icmp_header = recvPacket[20:28]
                types, code, checksum, packet_id, seq = struct.unpack("bbHHh", icmp_header)
                #Fill in end
                # try: #try to fetch the hostname
                    #Fill in start
                try:
                    host = gethostbyaddr(addr[0])[0]
                    print(host)
                    #Fill in end
                # except herror:   #if the host does not provide a hostname
                    #Fill in start
                except herror:
                    # pass
                    host = 'hostname not returnable'
                    #Fill in end
                # [‘1’, ‘12ms’, ‘10.10.111.10’, ‘hop1.com’]
                if types == 11:
                    tracelist1.append(str(ttl))
                    tracelist1.append(rtt)
                    tracelist1.append(addr[0])
                    tracelist1.append(host)
                    tracelist2.append(tracelist1)
                elif types == 3:
                    tracelist1.append(str(ttl))
                    tracelist1.append(rtt)
                    tracelist1.append(addr[0])
                    tracelist1.append(host)
                    tracelist2.append(tracelist1)
                elif types == 0:
                    return tracelist2
                else:
                    #Fill in start
                    error = "error"
                    #If there is an exception/error to your if statements, you should append that to your list here
                    tracelist1.append(str(ttl))
                    tracelist1.append(rtt)
                    tracelist1.append(addr[0])
                    tracelist1.append(error)
                    tracelist2.append(tracelist1)
                    # tracelist1.append(response)
                    #Fill in end
                break
            finally:
                mySocket.close()
    return tracelist2

if __name__ == "__main__":
    get_route('www.google.com')
    # print(get_route('www.google.com'))