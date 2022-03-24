from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

DBModel = declarative_base(metadata=MetaData(schema='project'))
