from loguru import logger as log
log.remove()
log.add(sys.stderr, level="INFO")