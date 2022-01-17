import logging
import threading
from experiment import Experiment

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

exp = Experiment(file='config.yml')

thread = threading.Thread(target=exp.wait_for_messages)
thread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    logging.info('Stopping Experiment')
    exp.stop()
except Exception as e:
    logging.exception(e)

logging.info('Bye Bye')

