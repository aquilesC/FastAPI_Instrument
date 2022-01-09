
import time
from random import random

import zmq


class Instrument:
    """ Fake instrument to show the pattern on how to communicate with a fastAPI server through sockets
    """
    def __init__(self, name):
        self.name = name
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")
        print('Instrument ready to accept messages')

    def wait_for_messages(self):
        """ This method will run an infinite loop waiting for messages. It can be directly passed to
        its own thread, for example.
        """
        while True:
            #  Wait for next request from client
            message = self.socket.recv_string()
            print(f"Received request: {message}")

            if message == 'measure_temp':
                # This is where we would measure the temperature
                temp = str(self.measure_temp())
                self.socket.send_string(temp)
            elif message == 'idn':
                name = self.idn()
                self.socket.send_string(name)
            else:
                self.socket.send_string('Unknown command')

    def measure_temp(self):
        time.sleep(1)  # to simulate some process
        return random()

    def idn(self):
        return self.name