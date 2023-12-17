from datetime import date, timedelta

from fastapi import APIRouter, HTTPException, Depends, status, Path, Query
from flask import session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import contacts as repositories_contacts
from src.schemas.contact import ContactSchema, ContactUpdateSchema, ContactResponse


from src.repository.contacts import search_contacts, get_contacts_by_birthday_range

router = APIRouter(prefix='/contacts', tags=['contacts'])
@router.get("/", response_model=list[ContactResponse])
async def get_contacts(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0),
                    db: AsyncSession = Depends(get_db)):
    contacts = await repositories_contacts.get_contacts(limit, offset, db)
    return contacts

@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(body: ContactSchema, db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.create_contact(body, db)
    return contact

@router.put("/{contact_id}")
async def update_contact(body: ContactUpdateSchema, contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="NOT FOUND")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_contacts(contact_id: int = Path(ge=1), db: AsyncSession = Depends(get_db)):
    contact = await repositories_contacts.delete_contact(contact_id, db)
    return contact


# @router.get("/search/", response_model=list[ContactResponse])
# async def search_contacts_api(
#         search: str = Query(None, min_length=1, max_length=100),
#         db: AsyncSession = Depends(get_db)
# ):
#     if not search:
#         return []
#
#     contacts = await search_contacts(search, db)
#     return contacts

@router.get("/search", response_model=list[ContactResponse])
async def search_contacts_api(
    query: str = Query(None, min_length=1, max_length=300),
    db: AsyncSession = Depends(get_db)
):
    contacts = await search_contacts(query, db)
    return contacts


@router.get("/upcoming-birthdays", response_model=list[ContactResponse])
async def get_upcoming_birthdays(db: AsyncSession = Depends(get_db)):
    today = date.today()
    next_week = today + timedelta(days=7)

    contacts = await repositories_contacts.get_contacts_by_birthday_range(today, next_week, db)
    return contacts