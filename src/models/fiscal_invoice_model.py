
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Numeric, Text, JSON
from sqlalchemy.orm import relationship
from database_connection import Base

class FiscalInvoice(Base):
    __tablename__ = 'fiscal_invoices'
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    access_key = Column(String(44), nullable=False, unique=True)
    number = Column(String(15), nullable=False)
    series = Column(String(3), nullable=False)
    model = Column(String(2), nullable=False)
    
    issuer_cnpj = Column(String(14), nullable=False)
    issuer_name = Column(String(255), nullable=False)

    recipient_cnpj = Column(String(20))
    recipient_name = Column(String(255))

    issued_at = Column(DateTime, nullable=False)
    received_at = Column(DateTime)


    total_amount = Column(Numeric(15, 2), nullable=False)
    situation = Column(String(50))
    total_amount = Column(Numeric(15, 2), nullable=False)
    status = Column(String(50))

    xml_content = Column(Text, nullable=False)
    data_json = Column(JSON)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

    company = relationship("Company", back_populates="fiscal_invoices")
    user = relationship("User", back_populates="fiscal_invoices")