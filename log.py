from loguru import logger as log
import sys
log.remove()
log.add(sys.stderr, level="INFO")