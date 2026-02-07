import logging
import sys

#run code like this in files to create a logger
#logger = logging.getLogger(__name__)
#logger.setLevel(logging.INFO)
#logger.addHandler(stdoutHandler)
#logger.addHandler(errHandler)

# logging config
stdoutHandler = logging.StreamHandler(stream=sys.stdout)
stdoutHandler.setLevel(logging.DEBUG)

errHandler = logging.FileHandler("error.log")
errHandler.setLevel(logging.ERROR)

fmt = logging.Formatter(
    "{asctime} - {levelname}:{name}:{message}", style="{", datefmt="%Y-%m-%d %H:%M")

stdoutHandler.setFormatter(fmt)
errHandler.setFormatter(fmt)