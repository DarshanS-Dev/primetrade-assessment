from fastapi import Depends, APIRouter, HTTPException
from app.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy import select
from app import models, schemas, auth

router = APIRouter(prefix="/watchlist", tags=["watchlist"])

@router.get("/", response_model=list[schemas.WatchlistOut])
async def get_watchlist(user: models.User = Depends(auth.get_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.WatchlistItem).where(models.WatchlistItem.user_id == user.id))
    items = result.scalars().all()
    return items 

@router.get("/admin", response_model=list[schemas.WatchlistOut])
async def get_admin_watchlist(user: models.User = Depends(auth.get_user), db: AsyncSession = Depends(get_db)):
    if not user.is_admin:
        raise HTTPException(403, "User is not admin")
    
    result = await db.execute(select(models.WatchlistItem))
    items = result.scalars().all()
    return items 

@router.post("/", response_model=schemas.WatchlistOut)
async def add_item(payload: schemas.WatchlistCreate, user: models.User = Depends(auth.get_user), db: AsyncSession = Depends(get_db)):
    item = models.WatchlistItem(symbol=payload.symbol, user_id=user.id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.put("/", response_model=schemas.WatchlistOut)
async def update_item(payload: schemas.WatchlistUpdate, user: models.User = Depends(auth.get_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.WatchlistItem).where(models.WatchlistItem.id == payload.item_id, models.WatchlistItem.user_id == user.id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Item not found")
    item.symbol = payload.symbol
    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/")
async def delete_item(payload: schemas.WatchlistDelete, user: models.User = Depends(auth.get_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.WatchlistItem).where(models.WatchlistItem.id == payload.item_id, models.WatchlistItem.user_id == user.id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(404, "Item not found")
    await db.delete(item)
    await db.commit()
    return {"message": "Deleted"}