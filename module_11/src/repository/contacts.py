from sqlalchemy import select, or_, extract
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from src.entity.models import Contact
from src.schemas.contact import ContactSchema, ContactUpdateSchema

async def get_contacts(limit: int, offset: int, db: AsyncSession):
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession):
    contact = Contact(**body.model_dump(exclude_unset=True))  # (title=body.title, description=body.description)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.date_of_birthday = body.date_of_birthday
        contact.additional_information = body.additional_information
        await db.commit()
        await db.refresh(contact)
    return contact

async def delete_contact(contact_id: int, db: AsyncSession):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(search: str, db: AsyncSession):
    query = select(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{search}%"),
            Contact.last_name.ilike(f"%{search}%"),
            Contact.email.ilike(f"%{search}%")
        )
    )

    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_contacts_by_birthday_range(start_date: date, end_date: date, db: AsyncSession):
    query = select(Contact).where(
        extract('month', Contact.date_of_birthday) == extract('month', start_date),
        extract('day', Contact.date_of_birthday).between(extract('day', start_date), extract('day', end_date)),
    )

    contacts = await db.execute(query)
    return contacts.scalars().all()