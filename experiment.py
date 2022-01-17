import logging
import time

import yaml
import zmq

from module_a import ModuleA

logger = logging.getLogger(__name__)


class Experiment:
    def __init__(self, file='config.yml'):
        self.config = None
        self.load_config(file)
        self.module_a = ModuleA(ip=self.config['module_a']['ip'], port=self.config['module_a']['port'])
        logger.info(f'Initialized {self.module_a}')
        self.keep_running = True

    def load_config(self, file):
        logger.info(f'Loading config {file}')
        self.config = yaml.load(open(file, 'r'), Loader=yaml.FullLoader)
        logger.debug(self.config)

    def wait_for_messages(self):
        """ This method will run an infinite loop waiting for messages. It can be directly passed to
        its own thread, for example.
        """
        logger.info(f'Binding ZMQ on tcp://*:{self.config["experiment_socket"]["port"]}')
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind(f"tcp://*:{self.config['experiment_socket']['port']}")

        while self.keep_running:
            #  Wait for next request from client
            event = self.socket.poll(0)
            if not event:
                time.sleep(.005)
                continue
            message = self.socket.recv_json()
            logger.debug(f"Received request: {message}")

            module = list(message.keys())[0]
            message = message[module]
            if module == 'module_a':
                if message == 'attributes':
                    result = self.module_a.get_attributes()
                elif message == 'parameters':
                    result = self.module_a.get_parameters()
                else:
                    result = {'error': f'{self.module_a} method not known'}
            else:
                result = {'error': f'{module} not known'}
                logger.debug(result)
            self.socket.send_json(result)
        self.socket.close()

    def stop(self):
        self.keep_running = False