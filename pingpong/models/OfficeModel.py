from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from pingpong.utils.database import Base

class OfficeModel(Base):

	__tablename__ = "offices"

	id = Column(Integer, primary_key = True)
	city = Column(String)
	state = Column(String)
	skypeChatId = Column(String)
	key = Column(String)
	enabled = Column(Integer)
	createdAt = Column(DateTime)
	modifiedAt = Column(DateTime)

	def __init__(self, city, state, skypeChatId, key, enabled, createdAt, modifiedAt):
		self.city = city
		self.state = state
		self.skypeChatId = skypeChatId
		self.key = key
		self.enabled = enabled
		self.createdAt = createdAt
		self.modifiedAt = modifiedAt

	def hasSkypeChatId(self):
		return self.skypeChatId != None and len(self.skypeChatId.strip()) > 0

	def isEnabled(self):
		return self.enabled == 1
