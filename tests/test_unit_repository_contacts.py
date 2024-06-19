import unittest
from unittest.mock import MagicMock, AsyncMock

from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date, timedelta

from src.database.models import Contact, User
from src.schemas.schemas import ContactCreate, ContactUpdate
from src.repository.contacts import (
    get_contacts, create_contact, get_contact, update_contact, delete_contact,
    search_contacts, get_upcoming_birthdays
)

class TestContactRepository(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, email='test_user@example.com', hashed_password="qwerty", is_verified=True)
        self.session = AsyncMock(spec=AsyncSession)
        self.contact = Contact(
            id=1, first_name="John", last_name="Doe", email="john@example.com",
            phone_number="1234567890", birthday=date(1990, 1, 1),
            additional_info="Some info", owner_id=self.user.id
        )

    async def test_get_contacts(self):
        contacts = [self.contact]
        mocked_result = MagicMock()
        mocked_result.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_result

        result = await get_contacts(self.session, skip=0, limit=10, owner_id=self.user.id)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        contact_create = ContactCreate(
            first_name="Jane", last_name="Doe", email="jane@example.com",
            phone_number="0987654321", birthday=date(1991, 2, 2), additional_info="Other info"
        )
        self.session.commit.return_value = None
        self.session.refresh.return_value = self.contact

        result = await create_contact(self.session, contact_create, owner_id=self.user.id)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, contact_create.first_name)
        self.assertEqual(result.last_name, contact_create.last_name)

    async def test_get_contact(self):
        mocked_result = MagicMock()
        mocked_result.scalars.return_value.first.return_value = self.contact
        self.session.execute.return_value = mocked_result

        result = await get_contact(self.session, contact_id=1)
        self.assertEqual(result, self.contact)

    async def test_update_contact(self):
        contact_update = ContactUpdate(
            first_name="Johnny", last_name="Doe", email="johnny@example.com",
            phone_number="1234567890", birthday=date(1990, 1, 1), additional_info="Updated info"
        )
        self.session.commit.return_value = None
        self.session.refresh.return_value = self.contact

        mocked_result = MagicMock()
        mocked_result.scalars.return_value.first.return_value = self.contact
        self.session.execute.return_value = mocked_result

        result = await update_contact(self.session, contact_id=1, contact=contact_update, owner_id=self.user.id)
        self.assertIsInstance(result, Contact)
        self.assertEqual(result.first_name, contact_update.first_name)
        self.assertEqual(result.last_name, contact_update.last_name)

    async def test_delete_contact(self):
        self.session.commit.return_value = None

        self.session.execute.return_value.scalars.return_value.first.return_value = self.contact

        mocked_result = MagicMock()
        mocked_result.scalars.return_value.first.return_value = self.contact
        self.session.execute.return_value = mocked_result

        result = await delete_contact(self.session, contact_id=1, owner_id=self.user.id)
        self.session.delete.assert_called_once_with(self.contact)
        self.assertEqual(result, self.contact)

    async def test_search_contacts(self):
        contacts = [self.contact]
        mocked_result = MagicMock()
        mocked_result.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_result

        result = await search_contacts(self.session, query="John", owner_id=self.user.id)
        self.assertEqual(result, contacts)

    async def test_get_upcoming_birthdays(self):
        contacts = [self.contact]
        mocked_result = MagicMock()
        mocked_result.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_result

        result = await get_upcoming_birthdays(self.session, owner_id=self.user.id)
        self.assertEqual(result, contacts)

if __name__ == "__main__":
    unittest.main()
