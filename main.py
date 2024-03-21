from classes import Record, Name, Birthday, Phone, Email, Address, Group
from address_book import AddressBook
from colorama import init, Fore
from abc import ABC, abstractmethod

book = AddressBook()
commands = dict()

def error_handler(func):
    """Error handler for program runtime."""
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f'{Fore.RED}Oops! {e}{Fore.RESET}')
    return wrapper

@error_handler
def input_command(value: str = None):
    """Prompt the user to input a command with error handling."""
    if not value:
        print(f'{Fore.GREEN}Enter a command to execute: {Fore.RESET}', end='')
        user_input = input()
    else:
        user_input = value

    user_input = user_input.split(maxsplit=1)
    command = user_input[0].casefold()

    if not (command in commands):
        raise ValueError(f'InputCommand - Command "{command}" not recognized.')

    command_info = commands[command]

    if command_info['param']:
        if len(user_input) == 1:
            raise ValueError(f'InputCommand - No arguments provided for command execution.')

        params = user_input[1].split()
        params_count = len(params)
        func_params_count = len(command_info['param'].split(' '))
        
        if params_count != func_params_count:
            raise ValueError(f'InputCommand - Incorrect number of arguments - "{params_count}". Expected arguments - "{func_params_count}"')

    func = command_info['func']

    if command_info['param']:
        func.execute(*params) if not command_info['print'] else print(f'{Fore.YELLOW}{func.execute(*params)}{Fore.RESET}')
    else:
        func.execute() if not command_info['print'] else print(f'{Fore.YELLOW}{func.execute()}{Fore.RESET}')

"""Abstract base class for all commands."""
class AbstractCommand(ABC):
    def __init__(self, book: AddressBook):
        self.book = book

    @abstractmethod
    def execute(self, *args):
        pass

"""Greetings message."""
class Hello(AbstractCommand): 
    def execute(self):
        print(f'{Fore.GREEN}Greetings, my mentor!{Fore.GREEN}')

commands.update({
    'hello': {
        'desc': 'Greetings message.', 
        'func': Hello(book), 
        'param': None, 
        'print': False
    }
})

"""Выполнение команды справки."""
class Help(AbstractCommand):
    def execute(self):
        result = f'{"Команда":<10}{"Параметры":<40}{"Описание":<50}\n'
        for key, value in commands.items():
            param = value['param'] if value['param'] is not None else 'Без параметров'
            desc = value['desc']
            result += f'{key:<10}{param:<40}{desc:<50}\n'
        result = result.rstrip('\n')
        return result

commands.update({
    'help': {
        'desc': 'Help with commands.', 
        'func': Help(book), 
        'param': None,
        'print': True
    },
})

"""Add a contact field."""
class AddValueContact(AbstractCommand):
        def execute(self, name: str, obj_type: type, value: str) -> None:
            contact = book.find_contact(Record(name))
            book.change_contact('add', contact, eval(obj_type.capitalize()), value)

commands.update({
    'add': {
        'desc': 'Add a contact field.', 
        'func': AddValueContact(book), 
        'param': '[name] [type] [value]', 
        'print': False
    }
})

"""Delete a contact field."""
class DelValueContact(AbstractCommand):
    def execute(self, name: str, obj_type: type, value: str) -> None:

        contact = book.find_contact(Record(name))
        book.change_contact('delete', contact, eval(obj_type.capitalize()), value)

commands.update({
    'del': {
        'desc': 'Delete a contact field.', 
        'func': DelValueContact(book), 
        'param': '[name] [type] [value]', 
        'print': False
    }
})

"""Change a contact field."""
class ChangeValueContact(AbstractCommand):
    def execute(self, name: str, obj_type: type, new_value: str, old_value: str = None) -> None:

        contact = book.find_contact(Record(name))
        book.change_contact('change', contact, eval(obj_type.capitalize()), new_value, old_value)

commands.update({
    'change': {
        'desc': 'Change a contact.', 
        'func': ChangeValueContact(book), 
        'param': '[name] [type] [new_value] [old_value]', 
        'print': False
    }
})

"""Show birthdays in the current week."""
class ShowBirthdaysWeek(AbstractCommand):
    def execute():
        return book.get_upcoming_birthdays()

commands.update({
    'birthday': {
        'desc': 'Show birthdays for the week.', 
        'func': ShowBirthdaysWeek(book), 
        'param': None, 
        'print': True
    }
})

"""Delete a contact by name."""
class DeleteContact(AbstractCommand):
    def execute(self, name: str) -> None:
        book.delete_contact(Record(name))

commands.update({
    'delete': {
        'desc': 'Delete a contact.', 
        'func': DeleteContact(book), 
        'param': '[name]', 
        'print': False
    }
})

"""Find a contact by name."""
class FindContact(AbstractCommand):
    def execute(self, name: str) -> Record:
        print('Contact found:')
        return book.find_contact(Record(name))

commands.update({
    'find': {
        'desc': 'Find a contact.', 
        'func': FindContact(book), 
        'param': '[name]', 
        'print': True
    }
})

"""Create a new contact in the address book."""
class AddNewContact(AbstractCommand):
    def execute(self, name: str) -> None:
        book.add_contact(Record(name))

commands.update({
    'new': {
        'desc': 'Create a new contact.', 
        'func': AddNewContact(book), 
        'param': '[name]', 
        'print': False
    }
})

"""Show all contacts."""
class ShowAllContacts(AbstractCommand):
    def execute(self) -> AddressBook:
        return book

commands.update({
    'all': {
        'desc': 'Show all contacts.', 
        'func': ShowAllContacts(book), 
        'param': None, 
        'print': True
    }
})

"""Exit the program."""
class ExitBot(AbstractCommand):
    def execute(self) -> None:
        print(f'{Fore.GREEN}Farewell, my mentor!{Fore.GREEN}')
        exit()

commands.update({
    'exit': {
        'desc': 'Close the program.', 
        'func': ExitBot(book), 
        'param': None,
        'print': False
    }
})

"""Main program function."""
def main():
    init()
    input_command('hello')
    while True:
        input_command()

if __name__ == "__main__":
    main()