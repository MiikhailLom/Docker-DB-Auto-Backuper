import asyncio

import os
import sys
from typing import Literal

from core.logger import logger
from integrations.docker import Docker
from integrations.ipconfig import get_my_ip
from integrations.file import StorageFile
from utils.storage import delete_old_dumps


async def dbs_dump(containers: list[str], db: Literal["postgres", "mongo"]):
    """
        Dump databases
    :param containers: List of contaners
    :param db: Type of db ('postgres' or 'mongo')
    """
    docker = Docker()

    # Dump every db container
    for container_id in containers:
        await docker.dump_db(
            container_id,
            db=db
        )


async def upload_dump(file_path: str):
    """
        Upload dumps to storage-server
    :param file_path: Path to local file
    """
    # Get ip address of your server
    my_ip = await get_my_ip()

    # Split file path
    file_data = os.path.split(file_path)[-1].split('&')
    project_name = file_data[0]
    file_name = file_data[-1]

    # Create file object and upload
    file = StorageFile(
        local_path=file_path,
        storage_path=f'/root/storage/{my_ip}/{project_name}/{file_name}'
    )
    success = await file.upload()

    # If successful delete local dump
    if success:
        logger.info(
            f"Success uploaded to storage. File: %s. Project: %s.",
            file_name,
            project_name
        )
        os.remove(file_path)


async def backup() -> None:
    """
        Start backup of dbs
    :return:
    """
    # Delete old backups
    await delete_old_dumps()

    # Get Containers with dbs
    docker = Docker()
    containers = await docker.db_containers()

    logger.info('Postgres Containers length: %d', len(containers.postgres))
    logger.info('Mongo Containers length: %d', len(containers.mongo))

    dbs_dump_task = []

    # Dump postgres dbs
    for container_id in containers.postgres:
        dbs_dump_task.append(
            asyncio.create_task(
                docker.dump_db(
                    container_id=container_id,
                    db='postgres'
                )
            )
        )
    # Dump mongo dbs
    for container_id in containers.mongo:
        dbs_dump_task.append(
            asyncio.create_task(
                docker.dump_db(
                    container_id=container_id,
                    db='mongo'
                )
            )
        )

    # Wait for all tasks to complete
    await asyncio.gather(*dbs_dump_task)

    # Get list of local dumps
    directory = 'data/buffer'
    file_paths = [os.path.join(directory, file) for file in os.listdir(directory)]

    # Send dumps to storage-server
    upload_tasks = []
    for file_path in file_paths:
        upload_tasks.append(
            asyncio.create_task(upload_dump(file_path))
        )

    # Wait for all tasks to complete
    await asyncio.gather(*upload_tasks)

    logger.info("All backups done")
    sys.exit(0)
