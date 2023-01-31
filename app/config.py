from pydantic import BaseSettings

from app import database
class Settings(BaseSettings): #this will automatically 
                            #import values from environmnet varuiables which
                            # have the same name
    database_hostname: str = ""
    database_port: str = ""
    database_password: str = ""
    database_name: str = ""
    database_username: str = ""
    secret_key: str = ""
    algorithm: str = ""
    access_token_expire_minutes: int = 0 #default values are not necessary, Setting imports it from .env 
                                        #or the enviorenment varaibles
    class Config:
        env_file = ".env"

settings = Settings()