from pydantic import BaseModel

class TwitterConnectionSchema(BaseModel):
    bearer_token: str
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str
