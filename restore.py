import argparse
import asyncio

import os
import sys
from typing import Literal

from core.logger import logger
from integrations.docker import Docker
from integrations.ipconfig import get_my_ip
from integrations.storage import StorageFile


async def main() -> None:
    """
        Start backup of dbs
    :return:
    """
    # Catch script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-p',
        '--project',
        type=str,
        help='Project name for restore',
        required=True
    )
    parser.add_argument(
        '-d',
        '--dump',
        type=str,
        help='Dump name on storage-server',
        required=True
    )
    args = parser.parse_args()

    # Get ip address of your server
    my_ip = await get_my_ip()

    # Download dump file to local
    dump_path = f'data/buffer/{args.dump}'
    file = StorageFile(
        storage_path=f'/root/storage/{my_ip}/{args.project}/{args.dump}',
        local_path=dump_path
    )
    success = await file.download()

    if not success:
        logger.error("Failed to download dump file from storage")
        sys.exit(1)

    # Get Containers with dbs
    docker = Docker()
    await docker.restore_db(
        project_name=args.project,
        dump_path=dump_path
    )

    os.remove(dump_path)


if __name__ == "__main__":
    asyncio.run(main())
