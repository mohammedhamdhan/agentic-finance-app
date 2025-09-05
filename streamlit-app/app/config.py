import os
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv()

@dataclass
class Settings:
    DATA_DIR: str = os.getenv("DATA_DIR", "./data")
    FAISS_DIR: str = os.getenv("FAISS_DIR", "./data/faiss_index")
    ETF_PDF_DIR: str = os.getenv("ETF_PDF_DIR", "./data/etf_pdfs")
    FMP_API_KEY: str = os.getenv("FMP_API_KEY", "")
    ALPHAVANTAGE_API_KEY: str = os.getenv("ALPHAVANTAGE_API_KEY","")
settings = Settings()
