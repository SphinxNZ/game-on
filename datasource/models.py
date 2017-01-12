import asyncio
from django.db import models

from compete.models import CompetitionRound

DATA_SOURCE_CHOICES = (('Server', 'Server'),
                  ('Client', 'Client'), )

                  
class DataSource(models.Model):
    start_date = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True,blank=True)
    data_source_type = models.CharField(max_length=100,choices=DATA_SOURCE_CHOICES)

    round = models.ForeignKey(CompetitionRound, null=True,blank=True)
    source_url = models.URLField(null=True,blank=True)
    
    def action_start(self):
        #loop = asyncio.get_event_loop()
        self.loop = asyncio.get_event_loop_policy().new_event_loop()
        message = 'GET / \n\n'
        coro = self.loop.create_connection(lambda: ClientDataSourceProtocol(message, self.loop),
                                      '127.0.0.1', 80)
                                      
        print('Start')
        self.loop.run_until_complete(coro)
        print("Finish?")
        self.loop.run_forever()
        print("Finish?")
        self.loop.close()
        print("Finish?")

        
class ClientDataSourceProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        #transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


        


#TCP client
class TcpClient(asyncio.Protocol):
    message = 'Testing'

    def connection_made(self, transport):
        self.transport = transport
        self.transport.write(self.message.encode())
        print('data sent: {}'.format(self.message))
        server_udp[1].tcp_client_connected()


    def data_received(self, data):
        self.data = format(data.decode())
        print('data received: {}'.format(data.decode()))
        if self.data == 'Testing':
            server_udp[1].send_data_to_udp(self.data)

    def send_data_to_tcp(self, data):
        self.transport.write(data.encode())

    def connection_lost(self, exc):
        msg = 'Connection lost with the server...'
        info = self.transport.get_extra_info('peername')
        server_udp[1].tcp_client_disconnected(msg, info)


#UDP Server
class UdpServer(asyncio.DatagramProtocol):

    CLIENT_TCP_TIMEOUT = 5.0

    def __init__(self):
        self.client_tcp_timeout = None

    def connection_made(self, transport):
        print('start', transport)
        self.transport = transport

    def datagram_received(self, data, addr):
        self.data = data.strip()
        self.data = self.data.decode()
        print('Data received:', self.data, addr)
        if self.data == 'send to tcp.':
            client_tcp[1].send_data_to_tcp(self.data)

    def connection_lost(self, exc):
        print('stop', exc)

    def send_data_to_udp(self, data):
        print('Receiving on UDPServer Class: ', (data))

    def connect_client_tcp(self):
        global client_tcp
        coro = loop.create_connection(TcpClient, 'localhost', 8000)
        task = asyncio.async(do_connect())
        def cb(result):
            client_tcp = result
        task.add_done_callback(cb)

    def tcp_client_disconnected(self, data, info):
        print(data)
        self.client_tcp_info = info
        self.client_tcp_timeout = loop.call_later(self.CLIENT_TCP_TIMEOUT, self.connect_client_tcp)

    def tcp_client_connected(self):
        if self.client_tcp_timeout:
            self.client_tcp_timeout.cancel()
            print('call_later cancel.')

@asyncio.coroutine
def do_connect():
    global client_tcp
    while True:
        try:
            client_tcp = yield from loop.create_connection(TcpClient, 'localhost', 8000)
        except OSError:
            print("Server not up retrying in 5 seconds...")
            yield from asyncio.sleep(1)
        else:
            break

def crap():            
    loop = asyncio.get_event_loop()

    #UDP Server
    coro = loop.create_datagram_endpoint(UdpServer, local_addr=('localhost', 9000))
    server_udp = loop.run_until_complete(coro)

    #TCP client
    loop.run_until_complete(do_connect())

    loop.run_forever()        