import json
from pydantic_settings import BaseSettings


with open(file="config/services.json", mode="r", encoding="utf-8") as config_file:
    config = json.load(config_file)


class __Settings(BaseSettings):
    USER_SERVICE: dict = config["user_service"]


settings = __Settings()
