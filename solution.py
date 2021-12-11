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
                    tracelist1.append("* * * Request timed out.")
                    #Fill in start
                    #You should add the list above to your all traces list
                    #Fill in end
                recvPacket, addr = mySocket.recvfrom(1024)
                
                timeReceived = time.time()
                rtt = str(int(round((timeReceived - startedSelect) * 1000, 0))) + "ms"
                timeLeft = timeLeft - howLongInSelect
                if timeLeft <= 0:
                    tracelist1.append("* * * Request timed out.")
                    #Fill in start
                    #You should add the list above to your all traces list
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
                    #Fill in end
                # except herror:   #if the host does not provide a hostname
                    #Fill in start
                except herror:
                    host = 'hostname not returnable'
                    #Fill in end
                # [‘1’, ‘12ms’, ‘10.10.111.10’, ‘hop1.com’]
                if types == 11:
                    # bytes = struct.calcsize("d")
                    # timeSent = struct.unpack("d", recvPacket[28:28 +
                    # bytes])[0]
                    # #Fill in start
                    # rtt = str(int(round((timeReceived - t) * 1000, 0))) + "ms"
                    # res = [str(ttl), rtt, addr[0], host]
                    #You should add your responses to your lists here
                    tracelist1.append(str(ttl))
                    tracelist1.append(rtt)
                    tracelist1.append(addr[0])
                    tracelist1.append(host)
                    tracelist2.append(tracelist1)
                    # print(res)
                    # tracelist2.append(tracelist1)
                    # Fill in end
                elif types == 3:
                    # bytes = struct.calcsize("d")
                    # timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    # #Fill in start
                    # #You should add your responses to your lists here 
                    # rtt = str(int(round((timeReceived - t) * 1000, 0))) + "ms"
                    # res = [str(ttl), rtt, addr[0], host]
                    tracelist1.append(str(ttl))
                    tracelist1.append(rtt)
                    tracelist1.append(addr[0])
                    tracelist1.append(host)
                    tracelist2.append(tracelist1)
                    # print(res)
                    # tracelist2.append(res)
                    #Fill in end
                elif types == 0:
                    break
                
                    # bytes = struct.calcsize("d")
                    # timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
                    # #Fill in start
                    # #You should add your responses to your lists here and return your list if your destination IP is met
                    # rtt = str(int(round((timeReceived - timeSent) * 1000, 0))) + "ms"
                    # res = [str(ttl), rtt, addr[0], host]
                    
                    tracelist1.append(addr[0])
                    tracelist1.append(host)
                    tracelist2.append(tracelist1)
                    
                    # tracelist2.append(res)
                    #Fill in end
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

# print(get_route('www.google.com'))
# get_route('www.google.com')
if __name__ == "__main__":
    get_route('www.google.com')
    # print(get_route('www.google.com'))

'''
All values must be strings

You're also not resolving the hostname of the replying IP; see how it's 
www.google.com on every hop?  Additionally, you should put a return statement 
in your elif types == 0, since that's the block where you're getting an ICMP 
type 0 (an echo reply) which should only come from the destination you're 
actually tracing to; you want the loop to end at that point.  As is, you're 
reaching www.google.com at hop 10, and then continuing to send pings to 
www.google.com for hops 11-29.

In your most recent submission on Gradescope, your get_route definition starts 
off with initializing both tracelist1 and tracelist2 as empty lists.  You only 
want to initialize tracelist2 as an empty list here.  tracelist1 should be a 
list containing:
The hop number, which is equivalent to the TTL you set on that iteration of the 
loop
The round trip time (time between you sending the packet and receiving it).  
Right now, it looks like you have this set to calculated as 
timeReceived - timeSent, where 
timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0] . 
This looks like it's assuming the ICMP payload was set to be whatever the 
current time was went the ping was sent, which build_packet doesn't do.  
To simplify this, I'd instead calculated RTT as timeReceived - startedSelect . 
startedSelect is set on line 98 as the current time when you send the packet 
(or almost immediately after--close enough for this assignment); timeReceived 
is set on line 109 and is the time when you received the reply packet as 
measured by time.time() immediately after 
recvPacket, addr = mySocket.recvfrom(1024).
The source IP address of the reply packet.
The reverse resolution of that source IP, as given by the 
gethostbyaddr(addr[0]) function.  You may want to modify this slightly--as-is 
this actually returns a list of values including the address you looked up and 
the reverse resolution, but you only want the reverse resolution.  Output below:
>>> from socket import *
>>> gethostbyaddr("8.8.8.8")('dns.google', [], ['8.8.8.8'])
>>> gethostbyaddr("8.8.8.8")[0]
'dns.google'
Note that by just pulling out the [0] index of gethostbyaddr, I only get the 
hostname, not any of the other items.
If there is no reverse resolution, you can just set 
srcHostname = "hostname not returnable", which you've done on line 134.
If you do not get a response from a particular hop, you want to set the content 
of tracelist1 to reflect that:
Hop number
"* Request timed out."
On each iteration of the for loop you want to re-initialize tracelist1 as an 
empty list.  Otherwise you're just going to continually append to it and 
continually append its content to tracelist2.
Last thing - you've defined tracelist1 as an empty list; within your append 
statements you're kind of duplicating that effort.
tracelist1 = []
...
tracelist1.append([str(ttl), rtt, str(addr[0]), srcHostname])
tracelist2.append([tracelist1])
I think what this would do is append a list containing those four values to 
tracelist1 , so tracelist1 is a list of a list; tracelist2.append([tracelist1]) 
then appends a list containing tracelist1, which itself is a list of a list, so 
tracelist2 becomes a list, of a list, of a list, of a list. (edited) 
'''