import re
from classes import Record, AddressBook

def args_parser_typed(*type_args):
    def args_parser(func):
        def wrapper(args):
            function_args = args.split(" ")

            if len(type_args) != len(function_args):
                raise ValueError("Incorrect arguments amount")

            for i in range(len(type_args)):
                function_args[i] = type_args[i](function_args[i])

            try:
                return func(*function_args)

            except TypeError as err:
                raise ValueError(f"Error: {err}")

            except ValueError as err:
                raise ValueError(f"Handler error: {err}")

            except KeyError as err:
                raise KeyError(f"Error: {err}")

        return wrapper
    return args_parser

def validate_phone_number(contact_number):
    if re.match(r'^\d{10}$', contact_number) is None:
        raise ValueError("The contact number is not valid.")

@args_parser_typed(str, str)
def record_func(name, birthday):
    existing_record = address_book.find(name)
    if existing_record:
        print(f"Record {name} already exists.")
    else:
        # Create a new record
        global record
        record = Record(name, birthday)

        # Ask for phone numbers
        while True:
            phone_input = input("Enter phone number (or type 'done' to finish): ")
            if phone_input.lower() == 'done':
                break
            validate_phone_number(phone_input)
            try:
                record.add_phone(phone_input)
                print(f"Phone number {phone_input} added successfully.")
            except ValueError as e:
                print(f"Error: {e}")


@args_parser_typed(str, int)
def add_phone_func(name, phone):
    is_record = address_book.find(name)
    if is_record:
        result = record.add_phone(phone)
        print(result)
    else:
        print(f"Record {name} not found.")

@args_parser_typed(str, int)
def remove_phone_func(name, phone):
    is_record = address_book.find(name)
    if is_record:
        result = record.remove_phone(phone)
        print(result)
    else:
        print(f"Record {name} not found.")

@args_parser_typed(int, int)
def edit_phone_func(name, old_phone, new_phone):
    is_record = address_book.find(name)
    if is_record:
        result = record.edit_phone(old_phone, new_phone)
        print(result)
    else:
        print(f"Record {name} not found.")

@args_parser_typed(str)
def find_phone_func(phone):
    pass

@args_parser_typed()
def get_phones_func():
    pass

@args_parser_typed(Record)
def add_record_func(record):
    #для додавання запису потрібно написати слово record!!!
    address_book.add_record(record)
    print(f"Record added successfully.")

@args_parser_typed(int)
def iterator_func(size):
    pass

@args_parser_typed(str)
def find_func(name):
    is_record = address_book.find(name)
    if is_record:
        print(is_record)
        return True
    else:
        print(f"Record {name} not found.")
        return False


@args_parser_typed(str)
def delete_func(name):
    pass

@args_parser_typed(str)
def save_to_file_func(filename):
    pass

@args_parser_typed(str)
def search_contacts_func(query):
    pass

@args_parser_typed()
def days_to_birthday_func():
    pass

def hello_handler():
    return "How can I help you?"


@args_parser_typed(str, str)
def load_from_file(filename):
    pass


def main():
    global address_book

    address_book = AddressBook()
    address_book.load_from_file('address_book.pkl')

    table = {
        "record": record_func,
        "add_phone": add_phone_func,
        "hello": hello_handler,
        "remove_phone": remove_phone_func,
        "edit_phone": edit_phone_func,
        "find_phone": find_phone_func,
        "get_phones": get_phones_func,
        "add_record": add_record_func,
        "iterator": iterator_func,
        "find": find_func,
        "delete": delete_func,
        "save_to_file": save_to_file_func,
        "search_contacts": search_contacts_func,
        "days_to_birthday": days_to_birthday_func
    }
   

    while True:
        user_input = str(input(">>> "))

        if user_input.lower() in ["good bye", "close", "exit", "quit"]:
            print("Good Bye!")
            break

        first_space = user_input.find(" ")
        handler_name = user_input[:first_space].lower()
        args = user_input[first_space:].strip()       

        if user_input.lower() == "hello":
            handler_name = "hello"

        if handler_name in table:
            
            try:
             
                if user_input.lower() == "hello":
                    result = table[handler_name]()

                else:             
                    result = table[handler_name](args)

                if result:
                    print(result)

            except (ValueError, KeyError) as e:
                print(f"{e}")
        else:
            print("No such command")

if __name__ == "__main__":
    main()
