from pydantic import BaseModel


class DbContainersResult(BaseModel):
    mongo: list[str]
    postgres: list[str]


class Dump(BaseModel):
    path: str
    project_name: str
