import unittest
from unittest.mock import MagicMock, AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, datetime

from sqlalchemy.orm import Session
from src.repository.contacts import get_contacts,create_contact, update_contact,delete_contact,search_contacts
from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema



class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.user = User(id=1, username='test_user', password="qwerty", confirmed=True)
        self.session = AsyncMock(spec=AsyncSession)


    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [Contact(id=1, first_name='test_1', last_name='test_description_1', email='aaa@gmail.com', phone_number='023942834938', date_of_birthday='11.11.2012', additional_information='bla-bla', user=self.user),
                 Contact(id=2, first_name='test_1', last_name='test_description_2', email='aagffga@gmail.com', phone_number='023956565658', date_of_birthday='01.08.2002', additional_information='bla-bla', user=self.user)]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):

        date_of_birthday = date(2012, 11, 11)

        body = ContactSchema(
            first_name='test_1',
            last_name='test_description_1',
            email='aaa@gmail.com',
            phone_number='023942834938',
            date_of_birthday=date_of_birthday,
            additional_information='bla-bla',
            user=self.user
        )
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)


    async def test_update_contact(self):
        date_of_birthday = date(2012, 11, 11)

        body = ContactSchema(
            first_name='test_1',
            last_name='test_description_1',
            email='aaa@gmail.com',
            phone_number='023942834938',
            date_of_birthday=date_of_birthday,
            additional_information='bla-bla',
            user=self.user)

        mocked_todo = MagicMock()
        mocked_todo.scalar_one_or_none.return_value = Contact(id=1, first_name='test_1', last_name='test_description_1', email='aaa@gmail.com', phone_number='023942834938', date_of_birthday='11.11.2012', additional_information='bla-bla', user=self.user)
        self.session.execute.return_value = mocked_todo
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(id=1, first_name='test_1', last_name='test_description_1', email='aaa@gmail.com', phone_number='023942834938', date_of_birthday='11.11.2012', additional_information='bla-bla', user=self.user)
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()

        self.assertIsInstance(result, Contact)

    async def test_search_contacts(self):
        search_query = "test"
        expected_contacts = [
            Contact(first_name='test1', last_name='test_last_name1', email='test1@example.com', user=self.user),
            Contact(first_name='test2', last_name='test_last_name2', email='test2@example.com', user=self.user)
        ]
        mocked_contact = MagicMock()
        mocked_contact.filter.return_value.filter.return_value.filter.return_value.all.return_value = expected_contacts
        self.session.execute.return_value = mocked_contact


        result = await search_contacts(search_query, self.session, self.user)




if __name__ == '__main__':
    unittest.main()
