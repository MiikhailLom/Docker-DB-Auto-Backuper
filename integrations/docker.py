import os
from datetime import datetime

import aiodocker
import aiofiles
from aiodocker.containers import DockerContainer

from core.logger import logger
from settings import settings


class Docker:
    _docker_host = settings.docker.HOST

    async def db_containers(self) -> list[str]:
        """
            Search db containers by images
        :return: DbContainersResult
        """
        async with aiodocker.Docker(url=self._docker_host) as docker:
            # Get all containers
            containers = await docker.containers.list()

            result = []

            # Searching of containers with db image
            for container in containers:
                container = await container.show()
                image = container['Config']['Image']

                if 'mongo' in image:
                    logger.info('Append Mongo container: %s', container['Id'])
                    result.append(container['Id'])

                elif 'postgres' in image:
                    logger.info('Append Postgres container: %s', container['Id'])
                    result.append(container['Id'])

            return result

    async def dump_db(self, container_id: str) -> str:
        """
            Create dump file from postgres db
        :param container_id: Id of the container with db
        :return: Path to dump
        """
        async with aiodocker.Docker(url=self._docker_host) as docker:
            # Get db container
            container = await docker.containers.get(container_id)
            # Get working dir name
            container_info = await container.show()
            project_path = container_info['Config']['Labels'].get('com.docker.compose.project.working_dir')
            if not project_path:
                project_path = container_info['Config']['WorkingDir']
            project_name = os.path.split(project_path)[-1]

            # Create local dump path
            now = datetime.now()
            dump_name = f'{project_name}&{now.strftime("%d-%m-%Y_%H-%M")}.dump'
            dump_path = f'data/buffer/{dump_name}'

            # Set commands for backup
            if 'postgres' in container_info['Config']['Image']:
                command = "pg_dumpall -U postgres"
            elif 'mongo' in container_info['Config']['Image']:
                command = "mongodump --archive"

            # Insert commands into container
            exec_instance = await container.exec(['sh', '-c', command])
            exec_stream = exec_instance.start(detach=False)

            # Get stream of out data and insert in local file
            async with aiofiles.open(dump_path, 'wb') as f:
                while True:
                    chunk = await exec_stream.read_out()
                    if not chunk:
                        break
                    await f.write(chunk.data)

            logger.info('Local dump created: %s', dump_name)
            return dump_path

    async def restore_db(self, container_id: str, dump_path: str) -> bool:
        """
            Create dump file from postgres db
        :param container_id: Id of the container with db
        :param dump_path: Local dump file
        :return: Path to dump
        """
        async with aiodocker.Docker(url=self._docker_host) as docker:
            # Get db container
            container = await docker.containers.get(container_id)
            container_info = await container.show()

            # Set commands for backup
            if 'postgres' in container_info['Config']['Image']:
                command = "psql -U postgres"
            elif 'mongo' in container_info['Config']['Image']:
                command = "mongorestore --archive"
            else:
                logger.error('Not found database')
                return False

            # Insert commands into container
            exec_instance = await container.exec(['sh', '-c', command], stdin=True)
            exec_stream = exec_instance.start(detach=False)

            # Starts stream of dump into db
            async with aiofiles.open(dump_path, 'rb') as f:
                while True:
                    chunk = await f.read(1024)
                    if not chunk:
                        break
                    await exec_stream.write_in(chunk)

                await exec_stream.close()

            logger.info(
                'Success restore. Container: %s. Dump: %s',
                container_id,
                os.path.split(dump_path)[-1]
            )
            return True

    async def container_by_project_name(self, project_name: str) -> DockerContainer:
        """
            Get DB container by proj name
        :param project_name: Name of the project
        :return: Path to dump
        """
        async with aiodocker.Docker(url=self._docker_host) as docker:
            # Get db containers
            containers = await docker.containers.list()
            for container in containers:
                container_info = await container.show()

                # Get container work directory
                project_path = container_info['Config']['Labels'].get('com.docker.compose.project.working_dir')
                if not project_path:
                    project_path = container_info['Config']['WorkingDir']

                # Skip if not searching project
                if not project_name in project_path:
                    continue

                # If searching project then check if db container
                image = container_info['Config']['Image']
                db = ''
                if 'postgres' in image:
                    db = 'postgres'
                elif 'mongo' in image:
                    db = 'mongo'

                if db:
                    break

            return container
