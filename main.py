import logging
import env
import time

from logs.log import setup_logging
from service import service_mediasi

from apscheduler.schedulers.background import BackgroundScheduler


def main():
    logging.info(
        "======================================================================================"
    )
    logging.info("START")
    logging.info(f"Database Source Name : {env.dbSrc}")
    logging.info(f"Database mediasi Name : {env.dbDst}")
    logging.info(
        "======================================================================================"
    )

    service_mediasi()

    logging.info("END")
    logging.info(
        "======================================================================================"
    )


def schedule_jobs():
    scheduler = BackgroundScheduler()

    # Schedule main function every 5 minutes
    scheduler.add_job(main, "interval", minutes=5)

    # Start the scheduler
    scheduler.start()

    # Keep the main thread alive
    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Shutdown the scheduler on exit
        scheduler.shutdown()


if __name__ == "__main__":
    setup_logging()
    main()
    schedule_jobs()
