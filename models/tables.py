import os

from sqlalchemy import create_engine, Table, Column, Integer, ForeignKey, String, Text, DateTime, and_
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base

DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

engine = create_engine('postgresql+psycopg2://{}:{}@localhost/{}'.format(DB_USER, DB_PASS, DB_NAME))

Base = declarative_base()
session = Session(engine)

class Candidates(Base):
	__tablename__ = 'candidates'
	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(256), nullable=False)
	email_id = Column(String(256), nullable=False)
	github_id = Column(String(256), nullable=True)
	phone_no = Column(String(50), nullable=True)

class Languages(Base):
	__tablename__ = 'languages'
	id = Column(Integer, primary_key=True, nullable=False)
	name = Column(String(256), nullable=False)
	candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
	candidate = relationship("Candidates", foreign_keys=[candidate_id])