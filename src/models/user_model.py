from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from database_connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'))

    email = Column(String(255), unique=True, index=True)
    hashed_password = Column(String(255))
    name = Column(String(255))
    role = Column(String(255))
    active = Column(Boolean, default=True)
    last_login = Column(DateTime)
    created_at = Column(DateTime, server_default=func.now()) 
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    fiscal_invoices = relationship("FiscalInvoice", back_populates="user")
    company = relationship("Company", back_populates="users")