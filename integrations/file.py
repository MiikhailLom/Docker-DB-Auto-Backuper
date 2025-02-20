import asyncio
import logging
import os

import asyncssh

from integrations.base import AbstractFile
from settings import settings


class StorageFile(AbstractFile):
    _host = settings.storage.HOST
    _key = settings.storage.KEY
    _key_passphrase = settings.storage.KEY_PASSPHRASE
    _port = settings.storage.PORT
    _user = settings.storage.USER

    def __init__(
            self,
            storage_path: str,
            local_path: str = ''
    ):
        """
        :param local_path: Local file path. No need for deleting
        :param storage_path: Server file path
        """
        self.storage_path = storage_path
        self.local_path = local_path

    async def upload(self) -> bool:
        """
            Upload file on server by SFTP
        :return: bool
        """
        # Try to put file until it works out
        attempts = 0
        while attempts <= 5:
            try:
                # Create SSH session
                async with asyncssh.connect(
                        host=self._host,
                        port=self._port,
                        username=self._user,
                        client_keys=[self._key],
                        passphrase=self._key_passphrase,
                        known_hosts=None
                ) as conn:
                    # Create folder for file if not exist
                    await conn.run(f'mkdir -p {os.path.dirname(self.storage_path)}')

                    # Start SFTP session
                    async with conn.start_sftp_client() as sftp:
                        await sftp.put(
                            localpaths=self.local_path,
                            remotepath=self.storage_path
                        )
                        return True

            except Exception as e:
                logging.error('SFTP upload exception: %s', e)
                attempts += 1
                await asyncio.sleep(5)

        logging.error('SFTP CANT UPLOAD FILE: %s', self.local_path)

    async def download(self) -> bool:
        """
            Download file from server by SFTP
        :return: bool
        """
        # Try to put file until it works out
        attempts = 0
        while attempts <= 5:
            try:
                # Create SSH session
                async with asyncssh.connect(
                        host=self._host,
                        port=self._port,
                        username=self._user,
                        client_keys=[self._key],
                        known_hosts=None,
                        passphrase=self._key_passphrase
                ) as conn:
                    # Start SFTP session
                    async with conn.start_sftp_client() as sftp:
                        # Try to put file until it works out
                        attempts = 0
                        while attempts <= 5:
                            await sftp.get(
                                localpath=self.local_path,
                                remotepaths=self.storage_path
                            )
                            return True

            except Exception as e:
                logging.error('SFTP upload exception: %s', e)
                attempts += 1
                await asyncio.sleep(5)

        logging.error('SFTP CANT UPLOAD FILE: %s', self.local_path)

    async def delete(self) -> bool:
        """
            Delete file from server by SFTP
        :return: bool
        """
        # Try to put file until it works out
        attempts = 0
        while attempts <= 5:
            try:
                # Create SSH session
                async with asyncssh.connect(
                        host=self._host,
                        port=self._port,
                        username=self._user,
                        client_keys=[self._key],
                        known_hosts=None,
                        passphrase=self._key_passphrase
                ) as conn:
                    # Start SFTP session
                    async with conn.start_sftp_client() as sftp:
                        # Try to put file until it works out
                        attempts = 0
                        while attempts <= 5:
                            await sftp.remove(path=self.storage_path)
                            return True

            except Exception as e:
                logging.error('SFTP delete exception: %s', e)
                attempts += 1
                await asyncio.sleep(5)

        logging.error('SFTP CANT UPLOAD FILE: %s', self.local_path)
