import argparse
import asyncio
import sys

from core.logger import logger
from utils.backup import backup
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
        help='restore or backup',
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

    # If another argument
    else:
        logger.error('Select action (backup, restore) with --action')
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
