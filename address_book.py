import datetime
from collections import UserList
from serialize_pickle import Serializer
from classes import Record

class AddressBook(UserList):
    """A class to represent an address book."""

    def __init__(self) -> None:
        """Initialize the AddressBook."""
        self.path = r'address_book.pkl'
        super().__init__(Serializer._deserialize_dict(self.path))

    def save_contact_changes(self) -> None: 
        """Save the changes made to the address book."""
        Serializer._serialize_dict(self, self.path)

    def __str__(self) -> str:
        """String representation of the address book."""
        if not self.data:
            raise ValueError('AddressBook - The address book does not exist or does not contain any contacts.')
        result = '\n'.join(str(contact) for contact in self)
        result = result.rstrip('\n')
        return result

    def add_contact(self, contact: Record) -> None:
        """Add a contact to the address book."""
        if contact in self:
            raise ValueError(f'AddressBook - The contact "{contact.name}" already exists in the address book.')
        self.append(contact)
        self.save_contact_changes()

    def find_contact(self, find_contact: Record) -> Record:
        """Find a contact in the address book by name."""
        if not find_contact in self:
            raise ValueError(f'AddressBook - No matches found in the address book for "{find_contact.name}".')
        return self[self.index(find_contact)]

    def delete_contact(self, delete_contact: Record) -> None:
        """Delete a contact from the address book by name."""
        self.remove(self.find_contact(delete_contact))
        self.save_contact_changes()

    def change_contact(self, flag, contact, obj_type: type, new_value: str = None, old_value: str = None):
        """Change a contact's details."""
        contact = self.find_contact(contact)
        if flag == 'add':
            contact.add_value(obj_type, new_value)
        if flag == 'delete':
            contact.delete_value(obj_type, new_value)
        if flag == 'change':
            contact.change_value(obj_type, new_value, old_value)
        self.save_contact_changes()

    def get_upcoming_birthdays(self) -> list:
        """Get a list of contacts whose birthdays are in the current week."""
        if not self.data:
            raise ValueError('AddressBook - The address book does not contain any contacts.')
        birthday_week_list = list()
        local_date = datetime.datetime.today().date()
        local_weekdate_start = local_date - datetime.timedelta(days=local_date.weekday() + 2)
        local_weekdate_finish = local_date + datetime.timedelta(days=4 - local_date.weekday())
        for contact in self.contacts:
            contact.birthday = datetime.datetime.strptime(contact.birthday.value, '%d-%m-%Y').date()
            if (local_date.month - contact.birthday.month) == 0:
                if (local_weekdate_start.day <= contact.birthday.day <= local_weekdate_finish.day):
                    birthday_week_list.append(contact)
        return birthday_week_list