import logging
from datetime import datetime
import sys

timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')

log_path = 'logs/{}.log'.format(timestamp)

logging.basicConfig(filename=log_path, level=logging.INFO)
log = logging.getLogger('')
stdout = logging.StreamHandler(sys.stdout)
log.addHandler(stdout) # also log to stdout