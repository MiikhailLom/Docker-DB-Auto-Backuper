import os
from datetime import datetime, timedelta

from core.logger import logger
from integrations.file import StorageFile
from integrations.storage import Storage


async def delete_old_dumps(age: int = 30):
    """
        Delete dumps from storage server older then age
    :param age: Days age
    """
    storage = Storage()
    file_paths = await storage.all_dumps()

    logger.info('On storage server %d dumps.', len(file_paths))

    for file_path in file_paths:
        # Math created at date
        date = os.path.split(file_path)[-1].replace('.dump', '')
        file_created_at = datetime.strptime(date, '%d-%m-%Y_%H-%M')

        # Skip if file younger then age
        if not datetime.now() - file_created_at >= timedelta(days=age):
           continue

        # Delete from storage server
        logger.info('Deleting from storage. File %s', file_path)
        storage_file = StorageFile(storage_path=file_path)
        await storage_file.delete()
