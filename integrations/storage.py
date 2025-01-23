import asyncio
import logging
import os

import asyncssh

from integrations.base import AbstractFile, AbstractStorage
from settings import settings


class Storage(AbstractStorage):
    _host = settings.storage.HOST
    _key = settings.storage.KEY
    _key_passphrase = settings.storage.KEY_PASSPHRASE
    _port = settings.storage.PORT
    _user = settings.storage.USER

    async def all_dumps(self) -> list[str]:
        """
            Get paths to all dump files
        :return: List with paths
        """
        # Create SSH session
        async with asyncssh.connect(
                host=self._host,
                port=self._port,
                username=self._user,
                client_keys=[self._key],
                passphrase=self._key_passphrase,
                known_hosts=None
        ) as conn:
            result = []
            server_folders = await conn.run(f'ls /root/storage', check=True)

            # Skan every folder of server
            for server_folder in server_folders.stdout.strip().split('\n'):
                project_folders = await conn.run(f'ls /root/storage/{server_folder}', check=True)

                # Skan every folder of project
                for project_folder in project_folders.stdout.strip().split('\n'):
                    files = await conn.run(
                        f'ls /root/storage/{server_folder}/{project_folder}',
                        check=True
                    )

                    # Add file paths to result
                    result += [
                        f'/root/storage/{server_folder}/{project_folder}/{file}'
                        for file in files.stdout.strip().split('\n')
                    ]

            return result
