import logging
import time

import yaml
import zmq

from module_a import ModuleA
from proveris_requests import ProverisRequests

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
                elif message == 'start_cycle':
                    self.actuation_cycle()
                    result = {'success': 'cycle started'}
                elif message == 'last_cycle':
                    result = {'cycle':
                                {
                                'cycle_number': self.last_cycle_number,
                                'force_data': self.force_data,
                                    }
                        }
                else:
                    result = {'error': f'{self.module_a} method not known'}
            else:
                result = {'error': f'{module} not known'}
                logger.debug(result)
            self.socket.send_json(result)
        self.socket.close()

    def actuation_cycle(self):
        num_steps = 1000
        self.force_data = np.zeros((100, num_steps))
        for i in range(num_steps):
            self.force_data[:, i] = self.module_a.get_values('force_data')
            self.position_data = self.module_a.get_values('position_data')
            self.last_cycle_number = i
            np.save(self.force_data, 'force_data.npy')
            url = 'service_endpoint_ip'
            ProverisRequests.put(url, self.position_data)

    def publish_actuation_cycle(self):
        position_data = np.load('position_data.npy')
        url = 'service_endpoint_ip'
        requests.put(url, position_data)

    def stop(self):
        self.keep_running = False