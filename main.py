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

@args_parser_typed(str)
def record_func(name):

    global contact_name
    contact_name = name

    global birthday
    birthday = None

    global contact_birthday
    birthday = None
    if len(info_contact) > 1:
        birthday = info_contact[1]
    elif len(info_contact) > 2:
        raise ValueError("Incorrect arguments amount")
    

    existing_record = address_book.find(name)
    if existing_record:
        print(f"Record {name} already exists.")
    else:
        # Create a new record
        global record_obj
        record_obj = Record(contact_name, birthday)

        # Ask for phone numbers
        while True:
            phone_input = input("Enter phone number (or type 'done' to finish): ")
            if phone_input.lower() == 'done':
                break
            try:
                validate_phone_number(phone_input)
                record_obj.add_phone(phone_input)
                print(f"Phone number {phone_input} added successfully.")
            except ValueError as e:
                print(f"Error: {e}")

        # Add the new record to the address book
        # address_book.add_record(record)
        print(f"Record {name} added successfully.")


@args_parser_typed(str)
def add_phone_func(phone):
    if record_obj:
        validate_phone_number(phone)
        result = record_obj.add_phone(phone)
        print(result)
    else:
        print(f"Record not found.")

@args_parser_typed(str)
def remove_phone_func(phone):
    if record_obj:
        result = record_obj.remove_phone(phone)
        print(result)
    else:
        print(f"Record {contact_name} not found.")

@args_parser_typed(str, str)
def edit_phone_func(old_phone, new_phone):
    if record_obj:
        validate_phone_number(new_phone)
        result = record_obj.edit_phone(old_phone, new_phone)
        print(result)
    else:
        print(f"Record {contact_name} not found.")


@args_parser_typed(str)
def get_phones_func(str):
    if record_obj:
        phones = record_obj.get_phones()
        if phones:
            print(f"Phones for {contact_name}: {', '.join(phones)}")
        else:
            print(f"No phones found for {contact_name}.")
    else:
        print(f"Record {contact_name} not found.")

@args_parser_typed(str)
def add_record_func(name):
    address_book.add_record(record_obj)
    print(f"Record added successfully.")

@args_parser_typed(int)
def iterator_func(size):
    for batch in address_book.iterator(size):
        for record in batch:
            print(record)

@args_parser_typed(str)
def find_func(name):
    is_record = address_book.find(name)
    if is_record:
        print(is_record)
    else:
        print(f"Record {name} not found.")


@args_parser_typed(str)
def delete_func(name):
    result = address_book.delete(name)
    print(result)

# @args_parser_typed(str)
# def save_to_file_func(filename):
#     address_book.save_to_file(filename)
#     print(f"Address book saved to file.")

@args_parser_typed(str)
def search_contacts_func(query):
    results = address_book.search_contacts(query)
    if results:
        for result in results:
            print(result)
    else:
        print("No matching contacts found.")

@args_parser_typed(str)
def days_to_birthday_func(name):
    if record_obj and contact_birthday:
        days_left = record_obj.birthday.days_to_birthday()
        if days_left is not None:
            print(f"Days left to {contact_name}'s birthday: {days_left}")
        else:
            print(f"No birthday information for {contact_name}")
    else:
        print(f"Record {contact_name} not found.")

def hello_handler():
    return "How can I help you?"

def show_all_func():
    if address_book:
        for record in address_book.data.values():
            print(record)
    else:
        print("Address book is empty.")

def main():
    global address_book

    address_book = AddressBook()
    address_book.load_from_file('address_book.pkl')

    table = {
        "record": record_func, #
        "add_phone": add_phone_func,#
        "hello": hello_handler,#
        "remove": remove_phone_func,#
        "edit": edit_phone_func,#
        "get_phone": get_phones_func,#
        "add_record": add_record_func,#
        "iterator": iterator_func,#
        "find": find_func,#
        "delete": delete_func,#
        # "save": save_to_file_func,
        "search": search_contacts_func,#
        "show all": show_all_func,
        "days_to_birthday": days_to_birthday_func
    }
   

    while True:
        user_input = str(input(">>> "))

        if user_input.lower() in ["good bye", "close", "exit", "quit"]:
            address_book.save_to_file('address_book.pkl')
            print("Good Bye!")
            break

        first_space = user_input.find(" ")
        handler_name = user_input[:first_space].lower()
        args = user_input[first_space:].strip()       

        if user_input.lower() == "hello":
            handler_name = "hello"
        
        if user_input.lower() == "show all":
            handler_name = "show all"

        if handler_name == "record":
            global info_contact
            info_contact = args.split(" ")
            second_space = args.find(" ")
            if second_space != -1:
                args = args[:second_space]
            else:
                pass

        if handler_name in table:
            
            try:
             
                if user_input.lower() == "hello":
                    result = table[handler_name]()

                elif user_input.lower() == "show all":
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
    print(
        """Instruction for the bot. Comands:
        hello - greeting. Using: hello
        show all - show all contacts. Using: show all
        
        1. record - create new record. Using: record (contact name) (birthday) - not necessarily)
        2. add_phone - add phone to the record. Using: add_phone (phone)
        3. remove - remove phone. Using: remove (phone)
        4. edit - edit phone. Using: edit (old phone) (new phone)
        5. get_phone - show all contact numbers. Using: get_phone (contact name)
        6. days_to_birthday - shows the days until the contact's birthday. Using: days_to_birthday (contact_name)
        *Use the commands above before adding the entry to address book
        7. add_record - add record to address book. Using: add_record (contact name)
        8. iterator - returns a generator based on Address Book entries. Using: iterator (number)
        9. find - find cotact on Adress Book. Using: find (contact name)
        10. delete - delete contact on Adress Book. Using: delete (contact name)
        11. search - searching for a contact by number or name: Using: search (contact name or phone)"""
    )
    main()
