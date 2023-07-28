from address_class import AddressBook, Birthday, Name, Phone, Record, BirthdayError, PhoneError, PhoneHaveLetter


address_book = AddressBook()
address_book = address_book.read_from_file()


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
        except KeyError:
            result = "This name does not exist."
        except BirthdayError:
            result = f'Not added. False birthday format. Input "dd-mm-yyyy"'
        except PhoneHaveLetter:
            result = f"Phone has invalid symbols"
        except PhoneError:
            result = f"Phone must have 12 digits"
        #except FileError:
            #result = "File open error"
        except ValueError:
            result = "ValueError"            
        except IndexError:
            result = "Give me parameters please."
        return result
    return wrapper


@input_error
def add_command(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if len(args) > 2:
        phone = Phone(args[1])
        birthday = Birthday(args[2])
        if rec :
            return rec.add_phone(phone), rec.add_birthday(birthday)
        rec = Record(name, phone, birthday)
        return address_book.add_record(rec)

    elif len(args) > 1:
        phone = Phone(args[1])
        if rec :
            return rec.add_phone(phone)
        rec = Record(name, phone)
        return address_book.add_record(rec)
    
    else:
        if rec:
            return f"Contact {name} alredy exists"
        else:
            rec = Record(name)
            return address_book.add_record(rec)


@input_error
def change_command(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"


@input_error
def del_command(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.del_phone(phone)
    return f"No contact {name} in address book"


@input_error
def phone_command(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        return str(rec)
    return f"No contact {name} in address book"


@input_error
def birthday_command(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if len(args) > 1:
        birthday = Birthday(args[1])
        if rec :
            return rec.add_birthday(birthday)
        rec = Record(name, birthday=birthday)
        return address_book.add_record(rec)
    else:
        if rec:
            return f"Contact {name} alredy exists"
        else:
            rec = Record(name)
            return address_book.add_record(rec)


@input_error
def show_birthday_command(*args):
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.days_to_birthday()
    return f"No contact {name} in address book"
    

def show_all_command(*args):
    return address_book


def show_pages_command(*args):
    try:
        page = int(args[0])        
    except ValueError:
        page = 5
    except IndexError:
        page = 5 

    i = 0
    for rec in address_book.iterator(page):
        i += 1
        print("\n",f"-page {i}-")
        print(rec)
    return ""


@input_error
def search_str_command(*args):
    search_str = address_book.search_str(args[0])
    return search_str


def exit_command(*args):
    return "Bye"


def unknown_command(*args):
    return "Invalid command"


def hello_command(*args):
    return "How can I help you?>>>"


COMMANDS = {
            add_command: ("add", "+"),
            change_command: ("change", ),
            del_command: ("delete", "remove"),
            phone_command: ("phone", ),
            birthday_command: ("birthday", ),
            show_birthday_command: ("show birthday", ),
            hello_command: ("hello", ),
            show_all_command: ("show all", ),
            show_pages_command: ("show pages", ),
            search_str_command: ("search", "find"),
            exit_command: ("exit", "close", "bye", "good bye", "stop")
            }

def parser(text:str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split()
                return cmd, data 
    return unknown_command, []


def main():
    print("Hello!")

    while True:
        user_input = input(">>>")
        cmd, data = parser(user_input)
        result = cmd(*data)
        print(result)
        
        if cmd == exit_command:
            address_book.save_to_file()
            break


if __name__ == "__main__":
    main()

