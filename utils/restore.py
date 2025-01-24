import os
import sys

from core.logger import logger
from integrations.docker import Docker
from integrations.ipconfig import get_my_ip
from integrations.file import StorageFile


async def restore(project: str, dump: str) -> None:
    """
        Start backup of dbs
    :param project: The name of the project
    :param dump: The name of the dump file to restore
    :return:
    """
    logger.info('=== Running restore ===')

    # Get ip address of your server
    my_ip = await get_my_ip()

    # Download dump file to local
    dump_path = f'data/buffer/{dump}'
    file = StorageFile(
        storage_path=f'/root/storage/{my_ip}/{project}/{dump}',
        local_path=dump_path
    )
    success = await file.download()

    if not success:
        logger.error("Failed to download dump file from storage")
        sys.exit(1)

    # Get Containers with dbs
    docker = Docker()
    container = await docker.container_by_project_name(project)

    # Backup before restore
    await docker.dump_db(container.id)

    # Restore
    await docker.restore_db(
        container_id=container.id,
        dump_path=dump_path
    )

    os.remove(dump_path)
    sys.exit(0)
