import logging
import env

from logs.log import setup_logging
from service import service_mediasi


def main():
    logging.info(
        "======================================================================================"
    )
    logging.info("START")
    logging.info(f"version : {env.version}")
    logging.info(
        "======================================================================================"
    )

    service_mediasi()

    logging.info("END")
    logging.info(
        "======================================================================================"
    )


if __name__ == "__main__":
    setup_logging()
    main()
