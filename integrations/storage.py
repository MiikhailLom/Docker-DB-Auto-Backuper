import asyncio
import logging
import os

import asyncssh

from integrations.base import AbstractFile, AbstractStorage
from integrations.ipconfig import get_my_ip
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
            stdout = server_folders.stdout.strip()

            if not stdout:
                return []

            # Skan every folder of server
            for server_folder in stdout.split('\n'):
                project_folders = await conn.run(f'ls /root/storage/{server_folder}', check=True)
                stdout = project_folders.stdout.strip()

                if not stdout:
                    continue

                # Skan every folder of project
                for project_folder in stdout.split('\n'):
                    files = await conn.run(
                        f'ls /root/storage/{server_folder}/{project_folder}',
                        check=True
                    )
                    stdout = files.stdout.strip()

                    if not stdout:
                        continue

                    # Add file paths to result
                    result += [
                        f'/root/storage/{server_folder}/{project_folder}/{file}'
                        for file in stdout.split('\n')
                    ]

            return result


    async def project_dumps(self, project_name: str) -> list[str]:
        """
            Get paths to all dump files
        :param project_name: Name of the project
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
            try:
                # Get ip address of your server
                my_ip = await get_my_ip()
                path = f'/root/storage/{my_ip}/{project_name}'

                # Run command
                folder = await conn.run(f'ls {path}', check=True)
                stdout = folder.stdout.strip()

                if not stdout:
                    return []

                # Add file paths to result
                return [
                    f'{path}/{file}'
                    for file in stdout.split('\n')
                ]

            except Exception as e:
                logging.error(f'Error getting project dumps: %s', e)
                return []
