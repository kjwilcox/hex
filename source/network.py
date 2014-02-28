import socket

class NetworkWriter:
    def __init__(self, outbound, target):
        """ Initalize the NetworkWriter object with the lists to operate on. """
        
        self.outbound = outbound
        self.target = target

    def write(self):
        """ Sends the oldest object in the queue to the target address. """

        if len(self.outbound) <= 0:
            return False
        
        sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # we do want a blocking socket for writing

        try: # sending stuff
            sender.connect(self.target)
            sender.send(self.outbound[0])
            r_val = self.outbound.pop(0)
            
        except socket.error:
            r_val = False

        sender.close()

        return r_val

class NetworkReader:
    def __init__(self, inbound, address):
        """ Opens and binds a socket for listening on the given port. """
        
        self.inbound = inbound
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(address)
        self.listener.setblocking(0)
        # we don't want to block, as we make a ton of read checks

    def read(self):
        """ Does a non-blocking check of the network, and adds read data to the queue. """

        r_val = False
        
        try:
            client, address = self.listener.accept()
            data = client.recv(128) # magic number for now
            if data:
                self.inbound.append(data)
                r_val = True
            client.close()
            
        except socket.error:
            pass # socket dodged a block

        return r_val     
