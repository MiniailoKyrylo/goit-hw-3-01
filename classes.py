from validation import validation
from abc import ABC

"""Base class for contact fields"""
class AbstractField(ABC):

    """
    Attributes:
    - value (str): Stores the value of the contact field
    """

    # Class constructor
    def __init__(self, value: str) -> None:
        self.value = validation(self, value)
    
    # Returns the string representation of the field value
    def __str__(self) -> str:
        return self.value
    
    # Checks the equivalence of Field objects
    def __eq__(self, obj: object) -> bool:
        
        if not isinstance(obj, type(self)):
            return False
                    
        return self.value == obj.value

"""Class for contact name"""
class Name(AbstractField):
    pass

"""Class for contact birthday"""
class Birthday(AbstractField):
    pass

"""Class for contact phone number"""
class Phone(AbstractField):
    pass

"""Class for contact email address"""
class Email(AbstractField):
    pass

"""Class for contact physical address"""
class Address(AbstractField):
    pass

"""Class for contact group"""
class Group(AbstractField):
    pass

"""Class for representing a contact"""
class Record():
    """
    Attributes:
    - name (Name): Contact name.
    """
    # Class constructor
    def __init__(self, name: str) -> None:
        
        # Creating instances of corresponding contact fields
        self.name = Name(name)
        self.birthday = None
        self.phone = None
        self.email = None
        self.address = None
        self.group = None

    # Adds a value of the specified type to the contact
    def add_value(self, obj_type: type, value: str) -> None:
        value = obj_type(value)
        obj_type_name = obj_type.__name__
        obj_attr_name = obj_type.__name__.lower()

        # Adding name, birthday, physical address
        if obj_type in [Name, Birthday, Address]:
            if getattr(self, obj_attr_name):
                raise ValueError(f'Record - The "{obj_type_name}" value already exists, it can only be changed.')
            setattr(self, obj_attr_name, value)

        # Adding phone number, email address, group
        if obj_type in [Phone, Email, Group]:
            if not getattr(self, obj_attr_name):
                setattr(self, obj_attr_name, [value])
            else:
                if value in getattr(self, obj_attr_name):
                    raise ValueError(f'Record - The value "{obj_type_name} - {value}" already exists.')
                getattr(self, obj_attr_name).append(value)

        return self

    # Deletes a value of the specified type from the contact
    def delete_value(self, obj_type: type, value: str = None) -> None:
        
        if value:
            value = obj_type(value)
        
        obj_type_name = obj_type.__name__
        obj_attr_name = obj_type.__name__.lower()

        # Deleting name - not possible.
        if obj_type == Name:
            raise ValueError(f'Record - Unable to delete the "{obj_type_name}" value.')

        # Deleting birthday and physical address.
        if obj_type in [Birthday, Address]:
            setattr(self, obj_attr_name, value)

        # Deleting phone number, email address, group.
        if obj_type in [Phone, Email, Group]:
            if not getattr(self, obj_attr_name) or not value in getattr(self, obj_attr_name):
                raise ValueError(f'Record - The specified value "{obj_type_name} - {value}" for deletion was not found.')
            getattr(self, obj_attr_name).remove(value)

        return self

    # Changes a value of the specified type in the contact
    def change_value(self, obj_type: type, new_value: str = None, old_value: str = None) -> None:
        if old_value:
            old_value = obj_type(old_value)
        if new_value:
            new_value = obj_type(new_value)

        obj_type_name = obj_type.__name__
        obj_attr_name = obj_type.__name__.lower()
        
        # Deleting birthday and physical address.
        if obj_type in [Name, Birthday, Address]:
            setattr(self, obj_attr_name, new_value)

        # Deleting phone number, email address, group.
        if obj_type in [Phone, Email, Group]:
            if not getattr(self, obj_attr_name) or not old_value in getattr(self, obj_attr_name):
                raise ValueError(f'Record - The specified value "{obj_type_name} - {old_value}" for replacement was not found.')
            getattr(self, obj_attr_name).remove(old_value)
            getattr(self, obj_attr_name).append(new_value)

        return self
    
    # Returns the string representation of the contact.
    def __str__(self) -> None:
        result = ''
        for name_attr, value_attr in vars(self).items():
            if isinstance(value_attr, list):
                if value_attr:
                    result += f'{name_attr.upper()}: '
                    for index, item in enumerate(value_attr):
                        result += f'{item}{", " if index != len(value_attr) - 1 else "\n"}'
            else:
                if value_attr:
                    result += f'{name_attr.upper()}: '
                    result += f'{value_attr}\n'
     
        return result
    
    # Checks the equivalence of two contacts.
    def __eq__(self, other) -> bool:
        
        if not isinstance(other, type(self)):
            return False
        
        return self.name == other.name