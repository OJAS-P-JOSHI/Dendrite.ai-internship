from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///database/todos.db')
Session = sessionmaker(bind=engine)
session = Session()

class ToDoModel(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    image = Column(String)

Base.metadata.create_all(engine)
