from sqlalchemy import select, or_, and_, extract
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema

async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts for the user.

    :param limit: int: Limit the number of contacts returned
    :param offset: int: Specify the number of rows to skip
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user id from the user object
    :return: A list of contact objects
    :doc-author: Trelent
    """
    stmt = select(Contact).filter_by(user_id=user.id).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactSchema: Validate the request body against the contactschema schema
    :param db: AsyncSession: Pass the database session to the function
    :param user: User: Get the user_id from the session
    :return: The contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.model_dump(exclude_unset=True), user=user)  # (title=body.title, description=body.description)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact

async def update_contact(contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id, user=user)
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

async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    stmt = select(Contact).filter_by(id=contact_id)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(search: str, db: AsyncSession, user: User):
    query = select(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{search}%"),
            Contact.last_name.ilike(f"%{search}%"),
            Contact.email.ilike(f"%{search}%")
        )
    )

    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_contacts_by_birthday_range(start_date: date, end_date: date, db: AsyncSession, user_id: int):
    query = select(Contact).filter(
        and_(
            Contact.user_id == user_id,
            extract('month', Contact.date_of_birthday) == extract('month', start_date),
            extract('day', Contact.date_of_birthday).between(extract('day', start_date), extract('day', end_date)),
        )
    )

    contacts = await db.execute(query)
    return contacts.scalars().all()