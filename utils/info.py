import os

from core.logger import logger
from integrations.storage import Storage


async def info(project_name: str):
    """
        Get project backups info
    :param project_name: Name of the project
    """
    storage = Storage()
    backups = await storage.project_dumps(project_name)
    backups = [os.path.split(path)[-1] for path in backups]

    logger.info('Project backups:\n%s', '\n'.join(backups))