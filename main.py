import argparse
import asyncio
import os
import sys

from core.logger import logger
from integrations.storage import Storage
from utils.backup import backup
from utils.info import info
from utils.restore import restore


async def main() -> None:
    """
        Start backup of dbs
    :return:
    """
    # Catch script arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-a',
        '--action',
        type=str,
        help='restore, backup, info',
        required=True
    )
    parser.add_argument(
        '-p',
        '--project',
        type=str,
        help='Project folder name for restore'
    )
    parser.add_argument(
        '-d',
        '--dump',
        type=str,
        help='File dump name on storage-server'
    )
    args = parser.parse_args()

    # Start backup or restore based on provided action
    if args.action == 'restore':
        if not args.project or not args.dump:
            logger.error('Select dump and project with --dump and --project')
            sys.exit(1)

        await restore(
            project=args.project,
            dump=args.dump
        )

    elif args.action == 'backup':
        await backup()

    elif args.action == 'info':
        if not args.project:
            logger.error('Select project with --project')
            sys.exit(1)

        await info(args.project)

    # If another argument
    else:
        logger.error('Use --help')
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
