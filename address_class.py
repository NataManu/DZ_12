import pickle
from collections import UserDict
from datetime import datetime


class BirthdayError(Exception):
    ...


class PhoneError(Exception):
    ...


class PhoneHaveLetter(Exception):
    ...
    

class Field:
    def __init__(self, value) -> None:
        self.value = value
    
    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        return self.value == other.value 
        

class Name(Field):
    ...
    

class Phone(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        san_phone = (
            value.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if len(san_phone) != 12:
            raise PhoneError 
        for i in san_phone:
            if i not in ['0','1','2','3','4','5','6','7','8','9']:
                raise PhoneHaveLetter
        self.__value =  san_phone
        
    def __str__(self) -> str:
        return self.__value


class Birthday(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise BirthdayError
        
    def __str__(self) -> str:
        return self.__value.strftime("%d-%m-%Y")


class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday: Birthday = None) -> None:
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday
        if not birthday:
            self.birthday = ""                     
    
    def add_phone(self, phone: Phone):
        if phone in self.phones:
            return f"Phone {phone} alredy exists at contact {self.name}"
        else:
            self.phones.append(phone)
            return f"Phone {phone} added to contact {self.name}"
                
    def change_phone(self, old_phone:Phone, new_phone:Phone):
        if new_phone in self.phones:
            return f"Phone {new_phone} alredy exists at contact {self.name}"    
        if old_phone in self.phones:
            self.phones[self.phones.index(old_phone)] = new_phone
            return f"{self.name}: phone {old_phone} changed to {new_phone}"
        return f"Phone {old_phone} does not exist at contact {self.name}"
    
    def del_phone(self, phone:Phone):
        if phone in self.phones:
            self.phones.remove(phone)
            return f"{self.name}: phone {phone} deleted"
        return f"Phone {phone} does not exist at contact {self.name}"
    
    def days_to_birthday(self):
        if self.birthday:
            day_now = datetime.now().date()
            day_dn = datetime(day=self.birthday.value.day, month=self.birthday.value.month, year=datetime.now().year).date()
            if day_now > day_dn:
                day_dn = datetime(day=self.birthday.value.day, month=self.birthday.value.month, year=datetime.now().year+1).date()
            difference = day_dn-day_now 
            return f"Birthday {self.name} : {self.birthday} in {difference.days} days"
        return f"The contact {self.name} has no data"

    def add_birthday(self, birthday):
        self.birthday = birthday
        return self.days_to_birthday()

    def __str__(self) -> str:
        return f"{self.name} : {', '.join(str(p) for p in self.phones)}  {str(self.birthday)}"


class AddressBook(UserDict):
    def save_to_file(self):
        with open("address.bin", "wb") as f:
            pickle.dump(self, f)

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        self.save_to_file()
        return f"Contact {record} added success"

    def read_from_file(self):
        try:
            with open("address.bin", "rb") as f:
                try:
                    self = pickle.load(f) 
                except EOFError:
                    print('File "address.bin" EOFError')
                except pickle.UnpicklingError:
                    print('File "address.bin" pickle.UnpicklingError')
        except FileNotFoundError:
            print('File "address.bin" FileNotFoundError')
        return(self) 
    
    def iterator(self, n=5):
        result = []
        count = 0
        for rec in self.data:
            result.append(str(self.data[rec]))
            count += 1
            if count >= n:
                yield "\n".join(result)
                count = 0
                result = []
        if result:
            yield "\n".join(result)  

    def search_str(self, search:str):
        result = ""
        for i in self:
            if search.lower() in str(self[i]).lower():
                result += str(self[i])+"\n"
        return result               

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
    
