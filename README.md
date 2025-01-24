# Docker dbs Backuper

## What the app can do:
* This application makes auto backups of all containerized databases (postgres, mongo) from the server where it is running and saves them to a remote storage server.

* You can also restore databases from backups on the storage server with this project!

* The application deletes backups older than 30 days.
If you want change it, then change number 30 on the line 9 in utils/storage.py

### The structure of the backups stored on the storage server:
```
.
└── root
    └── storage
        ├── 111.11.111.11
        │   ├── project-name-000
        │   │   ├── 01.01.25_02:00.dump
        │   │   └── 02.01.25_02:00.dump
        │   └── project-name-001
        │       ├── 01.01.25_02:00.dump
        │       └── 02.01.25_02:00.dump
        └── 222.22.222.22
            ├── project-name-000
            │   ├── 01.01.25_02:00.dump
            │   └── 02.01.25_02:00.dump
            └── project-name-001
                ├── 01.01.25_02:00.dump
                └── 02.01.25_02:00.dump
```

## Setting project.

### Step 1: Get your storage VPS server

You can buy it in any place of internet :)

### Step 2: Create Key to access the server

Make a key using this [tutorial](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)

### Step 3: Clone this repository

**On server what you need to backup:**

1. If you haven't Docker and Docker Compose:
   ```
   curl -fsSL https://raw.githubusercontent.com/taphix/deploydocker/main/setup.sh | bash
   ```

2. Clone this repository:
   ```
   git clone https://github.com/taphix/deploydocker
   ```

### Step 4: Create Virtual environment

Create .env file

```
STORAGE_HOST=Ip of storage server
STORAGE_KEY=Path to private key. I use "data/key"
STORAGE_KEY_PASSPHRASE=Pthrase for key if you used it
STORAGE_PORT=Ssh port on storage server. By defoult 22
STORAGE_USER=Server user. By Defualt root

DOCKER_HOST=Url for Docker API. Use "tcp://localhost:2375" (Don't forget setting it in Docker App). For Wondwos and "unix:///var/run/docker.sock" for Linux.

SCHEDULER_DAYS=How many times a day should backups be made
```

### Step 5: Create Key to access the server

Start the project!

_From the project folder_
```
docker compose up -d
```

After that you have container "backuper".  Run it when you need some backups:
```
docker compose run --rm --remove-orphans backuper python main.py -a backup
```


### Step 5: Create Key to access the server

Start the project!

_From the project folder_
```
docker compose up -d
```

## How to use.

For backup all Mongo, Postgres Containers on server:
```
docker compose run --rm backuper python main.py -a backup
```

For restore project db:
```
docker compose run --rm backuper python main.py -a restore -d name_pg_dump_in_storage -p name_of_project_workdir
```

For To find out the names of the project dams:
```
docker compose run --rm backuper python main.py -a info -p name_of_project_workdir
```

If you have any problems:
```
docker compose run --rm backuper python main.py -h
```
