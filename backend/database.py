from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Base, PDFDocument


Base = declarative_base()
engine = create_engine("sqlite:///pdfs.db")
Session = sessionmaker(bind=engine)
session = Session()

def init_db():
    Base.metadata.create_all(engine)

class PDFDocument(Base):
    __tablename__ = "pdf_documents"
    id = Column(Integer, primary_key=True)
    filename = Column(String)
    content = Column(Text)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

def add_pdf_metadata(filename, content):
    pdf = PDFDocument(filename=filename, content=content)
    session.add(pdf)
    session.commit()
    return pdf.id

def get_pdf_by_id(doc_id):
    pdf = session.query(PDFDocument).filter_by(id=doc_id).first()
    return {"filename": pdf.filename, "text": pdf.content} if pdf else None
