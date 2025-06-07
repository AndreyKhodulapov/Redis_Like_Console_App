from logging import getLogger, basicConfig, FileHandler, StreamHandler, ERROR, \
    DEBUG

from controller import main

logger = getLogger()
FORMAT = '%(asctime)s : %(name)s : %(levelname)s: %(message)s'
file_handler = FileHandler("data.log")
file_handler.setLevel(DEBUG)
console = StreamHandler()
console.setLevel(ERROR)
basicConfig(level=DEBUG, format=FORMAT, handlers=[file_handler, console])

if __name__ == "__main__":
    logger.info("start app")
    main()
    logger.info("stop app")
