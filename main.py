from classes import Record, AddressBook

def main():
    address_book = AddressBook()
    address_book.load_from_file('address_book.pkl')

    while True:
        user_input = str(input(">>> "))

        if user_input.lower() in ["good bye", "close", "exit", "quit"]:
            print("Good Bye!")
            break

        command, *args = user_input.split()

        if command.lower() == "hello":
            print("How can I help you?")
        
        elif command.lower() == "record":
            if len(args) < 1:
                print("Usage: create_record <name> [birthday]")
                continue

            name = args[0]
            birthday = None
            if len(args) > 1:
                birthday = args[1]

            existing_record = address_book.find(name)
            if existing_record:
                print(f"Record {name} already exists.")
            else:
                # Create a new record
                record = Record(name, birthday)

                # Ask for phone numbers
                while True:
                    phone_input = input("Enter phone number (or type 'done' to finish): ")
                    if phone_input.lower() == 'done':
                        break
                    try:
                        record.add_phone(phone_input)
                        print(f"Phone number {phone_input} added successfully.")
                    except ValueError as e:
                        print(f"Error: {e}")

                # Add the new record to the address book
                address_book.add_record(record)
                print(f"Record {name} added successfully.")

        elif command.lower() == "add_record":
            name = args[0]
            birthday = None
            if len(args) > 1:
                birthday = args[1]
            record = Record(name, birthday)
            address_book.add_record(record)
            print(f"Record {name} added successfully.")
        elif command.lower() == "add_phone":
            name = args[0]
            phone = args[1]
            record = address_book.find(name)
            if record:
                result = record.add_phone(phone)
                print(result)
            else:
                print(f"Record {name} not found.")
        elif command.lower() == "remove_phone":
            name = args[0]
            phone = args[1]
            record = address_book.find(name)
            if record:
                result = record.remove_phone(phone)
                print(result)
            else:
                print(f"Record {name} not found.")
        elif command.lower() == "get_phones":
            name = args[0]
            record = address_book.find(name)
            if record:
                phones = record.get_phones()
                if phones:
                    print(f"Phones for {name}: {', '.join(phones)}")
                else:
                    print(f"No phones found for {name}.")
            else:
                print(f"Record {name} not found.")
        elif command.lower() == "iterator":
            batch_size = int(args[0])
            for batch in address_book.iterator(batch_size):
                for record in batch:
                    print(record)
        elif command.lower() == "find":
            name = args[0]
            record = address_book.find(name)
            if record:
                print(record)
            else:
                print(f"Record {name} not found.")
        elif command.lower() == "delete":
            name = args[0]
            result = address_book.delete(name)
            print(result)
        elif command.lower() == "save_to_file":
            filename = args[0]
            address_book.save_to_file(filename)
            print(f"Address book saved to {filename}.")
        elif command.lower() == "search_contacts":
            query = args[0]
            results = address_book.search_contacts(query)
            if results:
                for result in results:
                    print(result)
            else:
                print("No matching contacts found.")
        elif command.lower() == "days_to_birthday":
            name = args[0]
            record = address_book.find(name)
            if record and record.birthday:
                days_left = record.birthday.days_to_birthday()
                if days_left is not None:
                    print(f"Days left to {name}'s birthday: {days_left}")
                else:
                    print(f"No birthday information for {name}.")
            else:
                print(f"Record {name} not found.")
        else:
            print("No such command.")

if __name__ == "__main__":
    main()