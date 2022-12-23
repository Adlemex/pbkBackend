from pydantic import BaseModel


class Block(BaseModel):
    title: str = ""
    steps: list[str] = []


class Resp(BaseModel):
    result: str = ""
    blocks: list[Block] = []
