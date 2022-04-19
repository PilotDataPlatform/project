from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

DBModel = declarative_base(metadata=MetaData(schema='project'))
