from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.orm import Session

# Yahan 'app.' hata diya hai kyunki files seedhe root mein hain
from database import get_db, init_db
from leads import router as leads_router  # Agar leads.py root mein hai toh


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="LeadFlow Agent", lifespan=lifespan)
app.include_router(leads_router)


@app.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok", "db": "connected"}
