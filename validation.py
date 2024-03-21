import re
import datetime

# Validation patterns.
pattern_name = {'min': 2, 'max': 20}
pattern_phone = r'^(?:\+?380|0|80)\d{9}$'
pattern_email = r'^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$'
date_pattern = r'%d.%m.%Y'
pattern_groups = ['Family', 'Parents', 'Friends', 'Work', 'School']
pattern_address = {'min': 5, 'max': 20}

def validation(obj: object, value: str) -> str:
    """
    Main validation function.

    Checks the given `value` with respect to the object type `obj`.

    Parameters:
        obj (object): The object for validation.
        value (str): The value to be validated.

    Returns:
        str: The formatted value after validation.

    Raises:
        ValueError: If the `value` does not pass validation.
    """
    if not value: # Check if a value is provided for validation.
        raise ValueError(f'Validation - Value {value} cannot be empty.')

    obj_type = obj.__class__.__name__
 
    if obj_type == 'Name': # Validate name.
        value = validation_name(value)
    elif obj_type == 'Birthday': # Validate birthday date format and check against today's date.
        value = validation_birthday(value)  
    elif obj_type == 'Phone': # Validate phone number format for Ukrainian operators.
        value = validation_phone(value)
    elif obj_type == 'Email': # Validate email address format.
        value = validation_email(value) 
    elif obj_type == 'Group': # Validate group name against the list.
        value = validation_group(value)
    elif obj_type == 'Address': # Validate physical address.
        value = validation_address(value)

    return value

def validation_name(value: str) -> str:
    """
    Validate the name value.

    Checks if the length of the name is within the specified range.

    Parameters:
        value (str): The name value to be validated.

    Returns:
        str: The validated name value.

    Raises:
        ValueError: If the length of the name is not within the specified range.
    """
    value = value.strip()

    if len(value) < pattern_name['min'] or len(value) > pattern_name['max']:
        raise ValueError(f'Validation - Name "{value}" should contain between {pattern_name["min"]} and {pattern_name["max"]} characters.')
    
    return value

def validation_birthday(value: str) -> str:
    """
    Validate the birthday date.

    Checks the format of the birthday date and ensures it's not in the future.

    Parameters:
        value (str): The birthday date string to be validated.

    Returns:
        str: The validated birthday date string.

    Raises:
        ValueError: If the birthday date format is incorrect or if it's in the future.
    """
    try:
        value = datetime.datetime.strptime(value, date_pattern).date()
    except ValueError:
        raise ValueError(f'Validation - Incorrect birthday date format - "{value}". Please enter in "DD.MM.YYYY" format.')
    else:   
        if  value > datetime.datetime.today().date():
            raise ValueError(f'Validation - Birthday date "{value}" cannot be in the future.')
        
    return value.strftime(date_pattern)

def validation_phone(value: str) -> str:
    """
    Validate the phone number.

    Checks if the phone number matches the Ukrainian operators format.

    Parameters:
        value (str): The phone number string to be validated.

    Returns:
        str: The validated phone number string.

    Raises:
        ValueError: If the phone number format is incorrect.
    """
    match = re.fullmatch(pattern_phone, value)

    if not match: 
        raise ValueError(f'Validation - Incorrect phone number format - "{value}".')
    
    return f'+38{match.group()[-10:]}'

def validation_email(value: str) -> str:
    """
    Validate the email address.

    Checks if the email address matches the standard format.

    Parameters:
        value (str): The email address string to be validated.

    Returns:
        str: The validated email address string.

    Raises:
        ValueError: If the email address format is incorrect.
    """
    match = re.fullmatch(pattern_email, value) 

    if not match: 
        raise ValueError(f'Validation - Incorrect email address format - "{value}".')
    
    return f'{match.group().casefold()}'

def validation_group(value:str) -> str:
    """
    Validate the group name.

    Checks if the group name exists in the predefined list.

    Parameters:
        value (str): The group name string to be validated.

    Returns:
        str: The validated group name string.

    Raises:
        ValueError: If the group name does not exist in the predefined list.
    """
    value = value.capitalize()

    if value not in pattern_groups:
        raise ValueError(f'Validation - Group "{value}" does not exist.')
    
    return value

def validation_address(value:str) -> str:
    """
    Validate the physical address.

    Checks if the length of the address string is within the specified range.

    Parameters:
        value (str): The address string to be validated.

    Returns:
        str: The validated address string.

    Raises:
        ValueError: If the length of the address string is not within the specified range.
    """
    value = value.strip()

    if len(value) < pattern_address['min'] or len(value) > pattern_address['max']: 
        raise ValueError(f'Validation - Address "{value}" should contain between {pattern_address["min"]} and {pattern_address["max"]} characters.')
    
    return value