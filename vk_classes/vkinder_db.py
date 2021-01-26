from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///vkinder', echo=True)
Base = declarative_base()


class Client(Base):
	__tablename__ = 'Client'
	id = Column(Integer, primary_key=True)
	vk_id = Column(Integer)
	first_name = Column(String)
	last_name = Column(String)
	sex = Column(Integer)
	city = Column(Integer)
	url = Column(String)
	found_photos = relationship('Photos')
	results = relationship('SearchData')


class Photos(Base):
	__tablename__ = 'Photos'
	id = Column(Integer, primary_key=True)
	likes = Column(Integer)
	url = Column(String)
	variant_id = Column(Integer)
	client_id = Column(Integer, ForeignKey('Client.id'))


class SearchData(Base):
	__tablename__ = 'SearchData'
	id = Column(Integer, primary_key=True)
	vk_id = Column(Integer)
	name = Column(String)
	url = Column(String)
	client_id = Column(Integer, ForeignKey('Client.id'))


Base.metadata.create_all(engine)
