from logging import getLogger

from controller import main

logger = getLogger(__name__)

if __name__ == "__main__":
    logger.info("start app")
    main()
    logger.info("stop app")
