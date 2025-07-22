from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from database_connection import Base

class Company(Base):
    __tablename__ = 'companies'
    
    id = Column(Integer, primary_key=True, index=True)
    legal_name = Column(String(255), nullable=False)           # razão social
    trade_name = Column(String(255))                           # nome fantasia
    state_registration = Column(String(20))                    # inscrição estadual
    cnpj = Column(String(14), nullable=False, unique=True)
    cellphone = Column(String(20))
    email = Column(String(255), nullable=False, unique=True)
    address_street = Column(String(255))
    address_number = Column(String(20))
    address_info = Column(String(100))
    address_neighborhood = Column(String(100))
    address_city = Column(String(100))
    address_state = Column(String(20))
    postal_code = Column(String(20))
    active = Column(Boolean, default=True)
    signature_date = Column(DateTime)
    plan = Column(Integer, default=1)
    trial_start_date = Column(DateTime)
    trial_end_date = Column(DateTime)
    trial_used = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now()) 
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    fiscal_invoices = relationship("FiscalInvoice", back_populates="company")
    users = relationship("User", back_populates="company")

