from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 'app.' hata kar direct config se import kiya
from config import get_settings

engine = create_engine(get_settings().DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # 'app.' hata kar direct models import kiya (agar models.py hai toh)
    import models  # tables register hone ke liye
    Base.metadata.create_all(bind=engine)
