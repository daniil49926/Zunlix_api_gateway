from pydantic import BaseModel


class Message(BaseModel):
    message: str


class Message404(Message):
    ...


class Message418(Message):
    ...


class Message500(Message):
    ...


class Message403(Message):
    additional_information: str
