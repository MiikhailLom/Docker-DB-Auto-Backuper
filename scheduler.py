import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from core.logger import logger
from settings import settings
from utils.backup import backup


async def main() -> None:
    """
        Create scheduler
    :return:
    """
    logger.info('=== Running scheduler ===')

    # Start scheduler with backup task
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        backup,
        trigger='interval',
        days=settings.scheduler.DAYS
    )
    scheduler.start()

    # Run forever
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
