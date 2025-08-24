from logging import getLogger

from controller import main

logger = getLogger(__name__)

if __name__ == "__main__":
    try:
        logger.info("start app")
        main()
    except (KeyboardInterrupt, EOFError):
        print("END")
        logger.info("stop app")
