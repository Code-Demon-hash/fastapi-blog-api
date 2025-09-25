from sqlalchemy import MetaData
from app.engine import engine


metadata_obj = MetaData()


metadata_obj.create_all(engine)