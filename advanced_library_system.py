from abc import ABC, abstractmethod
import json
import os
 
class Book:
    '''Initializes a set of variables'''
    def __init__(self, title, author, isbn, available):
        self.title = title
        self.author = author
        self._isbn = isbn
        self.available = available
    
    def __str__(self): #displays a human readble format
        return f"Title:{self.title}, Author: {self.author}, ISBN: {self._isbn}, Available: {self.available}"
     
    def mark_borrowed(self, borrower): # a method for users to borrow book
        self.borrower = borrower
        if self.available == True:
            self.available = False
            return f"You have successfully borrowed {self.title}"
        else:
            return f"{self.title} is currently not available"
    
    def mark_returned(self,is_returned): # a method for users to return borrowed books
        self.is_returned = is_returned
        if self.available == False:
            self.available = True
            return f"{self.title} has been successfully returned"
        else:
            return "Book was not returned"
        
class LibraryUser(ABC): #abstract class for the library user
    '''Initializes a set of variables'''
    def __init__(self,name ,user_id, borrowed_books): 
        self.name = name
        self.user_id = user_id
        self._borrowed_books = borrowed_books

    @abstractmethod
    def borrow_book(self): #base method for borrow book
        pass

    @abstractmethod
    def return_book(self): #base method for return book
        pass

    @abstractmethod
    def view_access(self):
        pass

class StudentUser(LibraryUser):
    '''This class inherits from library user, because a student user, will always be a library user'''

    def __init__(self,name, user_id, borrowed_books):
        super().__init__(name, user_id, borrowed_books) #initializes the inherited class method
        self.max_borrow = 3 #student user borrowing limit

    def __str__(self):
        return f"Name: {self.name}, UserId: {self.user_id}, Borrowed books: {self._borrowed_books}"
        
    def borrow_book(self, user_borrow_book):
        self.user_borrow_book = user_borrow_book
        list_of_available_books = ["Beauty", "Power", "Number", "Friend"]
        student_input = input("Enter the name of the book you want to borrow: ")
        student_input_book_number =  int(input("Enter the total number of books you want to borrow:  "))

        if student_input in list_of_available_books: #checks if the book to be borrowed is available 
            print("Book to be borrowed is available")

        else:
            print("Book to be borrowed is not available")

        if student_input_book_number > self.max_borrow : #checks if user is not borrowing more than the maximum number of books
            print(f"Borrowing limit reached. You cannot borrow more than {self.max_borrow}")
        
        else:
            print("You are eligible for borrowing!")

    def return_book(self, book_to_be_returned): #method for users to return boom
        self.book_to_be_returned = book_to_be_returned
        book_to_be_returned = input("Enter the name of the book to be returned: ")

        if book_to_be_returned not in self._borrowed_books:#checks if book to be returned was borrowed from the library
            print("This book was not borrowed by you")
        else:
            print(f"The book was successfully returned")

    def view_access(self):
        print(f"As a student you can borrow {self.max_borrow} books")

class AdminUser(LibraryUser):
    def __init__(self, name, user_id, borrowed_books):
        super().__init__(name, user_id, borrowed_books)
        self. available_books = ["Beauty", "Power", "Number", "Friend"]

    def __str__(self):
        return f"Name: {self.name}, UserId: {self.user_id}, Borrowed books: {self._borrowed_books}"

    def borrow_book(self, admin_input):
        self.admin_input = admin_input
        admin_input = input("What book do you want to borrow?: ").title()
        if admin_input not in self.available_books:
            print("Book to be borrowed not availbale")
        else:
            print("Book successfully borrowed")

    def return_book(self, admin_book_to_be_returned):
        self.admin_book_to_be_returned = admin_book_to_be_returned
        admin_book_to_be_returned = input("What is the name of the book to be returned?: ").title()
        if admin_book_to_be_returned not in self.available_books:
            print("Book was not borrowed form the library")
        else:
            print(f"{admin_book_to_be_returned} successfully returned!")

    def view_access(self):
        print("There is no limitation to the number of books that can be borrwed by an admin user ")

class BookUnavailableError(Exception): # a custom built exception class
    def __init__(self,title):
        self.title = title
        message = f"{self.title} is not available this moment" #error message to be displayed
        super().__init__(message)

class LibraryPersistence():
    '''A class that converts python data to JSON, and vice vera, it also saves data in a file'''
    @staticmethod
    def save_data(library, filename):  #tries to open a file in json format
        try:
            with open (filename, "w") as file: #opens a file
                json.dump(library, file, indent = 4)#converts file to json format
                print(f"Library data has been successfully added to {filename}")

        except Exception as e: #prints general error
            print(f"Error saving data:  {e}")

    @staticmethod
    def load_data(filename):
        if not os.path.exists(filename):#checks if the file exists
            print(f"{filename} does not exists. Starting with an empty data.")
            return []
        
        try: 
            with open(filename, "r") as file:
                data = json.load(file)#convert from json to python dta format
                print("Data successfully loaded")
                return data
            
        except json.JSONDecodeError:#checks the file format
            print(f"{filename}File not in accepted format")
            return []
        
        except Exception as e:#checks for general errors
            print(f"An error occurred: {e}.")
            return []
             
class LibrarySearch:
    @staticmethod
    def search(library,book_search = None):

        if book_search is None:
            book_search = input("What is the name of the book you are looking for?: ")

        user_book = [] #temporarily stores books matched by users

        for book in library:#loop to check the availablity of a book in the library
            if book_search.lower() in book.lower():
                print(f"{book} was found in the list of avaiilable books")
                user_book.append(book) #add matched

        if not user_book: #checks if the lsit is empty
            print("No book matches your search")
        else:
            print("Books found")
            for book in user_book:
                print("List of searched books:", book)#prints the list of all searched books
    
class Library():
    '''The main program class'''
    def __init__(self, books_file = "books.json" , users_file = "users.json"):
        self.books_file = books_file
        self.users_file = users_file

        self.books = LibraryPersistence.load_data(books_file) #saves books in a json file
        if not self.books:
            self.books = ["Mary In Wonder Land","The Good Kid", "Beauty And The Beast", "Cooking Show", "The Barren Land"]
        

        self.users = LibraryPersistence.load_data(users_file) #saves users in a json files
        if not self.users: #checks if users to be registered is already registered
           self.users = [
            {"Name": "Miracle", "Email": "miracle@gmail.com"},
            {"Name": "John", "Email": "john@gmail.com"},
            {"Name": "Seyi", "Email": "seyi@gmail.com"},
            {"Name": "Josphine", "Email": "josphine@gmail.com"},
            {"Name": "Betty", "Email": "betty@gmail.com"}
            ]
           
        LibraryPersistence.save_data(self.borrowed_books, "borrowed.json") #stores borrowed books in a json file
        self.borrowed_books = [] #empty list to temporarily store borrowed books
       

    def add_books(self, new_book):
        self.new_book = new_book
        new_book = input("What is the name of the book you want to add?: ")
        if new_book in self.books:
            print("Book already exists in the library.")
            return
        self.books.append(new_book)
        LibraryPersistence.save_data(self.books, self.books_file)
        print("New book has been successfully added.")

    def register_user(self): #a method to register  new users
        user_name = input("Enter in  valid name: ").title()
        user_email = input ("Enter in a valid  email:").lower()
        
        for user in self.users: #checks if it is alrready a registerd user
           if user["Name"] == user_name and user["Email"] == user_email:
             return "User has registered before"

        self.users.append({"Name": user_name, "Email": user_email}) #saves user data
        LibraryPersistence.save_data(self.users, self.users_file)
        return "New user has been successfully registered"


    def borrow_book(self, requested_book): #a method to borrow books
        self.requested_book = requested_book
        requested_book = input("Which book do you want to borrow?: ").title()

        try:
            if requested_book not in self.books: #checks if book to be borrowed is available
                raise BookUnavailableError(requested_book)
            
            self.books.remove(requested_book)
            self.borrowed_books.append(requested_book)
            return " The book has been successfully borrowed"
        
      
        except BookUnavailableError as e: #prints custom exception error
            return str(e)

    def return_book(self):
        book_to_return = input ("What book do you want to return?: ").title()

        if book_to_return not in self.borrowed_books: #checks if borrowed nook was borrowed from the library
            return f"This book was not borrowed"
        
        self.borrowed_books.remove(book_to_return)
        self.books.append(book_to_return)
        LibraryPersistence.save_data(self.books, self.books_file) #saves data in json
        LibraryPersistence.save_data(self.borrowed_books, "borrowed.json") #saves data in json
        return "The book has been successfully returned"



#creates classes objects
my_book = Book("Fairy tale", "Mary Jen", 1235, "Yes")
student_user_1 = StudentUser("Toluwani Edgal", "BU24SEN1005", "None")
admin_user_1 = AdminUser("Miracle John", 2357, "None")

#displays the output of the object
print(my_book)
print(student_user_1)
print(admin_user_1)

#displays the output in the various methods belonging to the different classes
print(my_book.mark_borrowed("Jane"))
print(my_book.mark_returned("Jane"))
print(student_user_1.borrow_book("Beauty"))
print(student_user_1.return_book("Jane"))
print(student_user_1.view_access())
print(admin_user_1.borrow_book("Power"))
print(admin_user_1.return_book("Power"))
print(admin_user_1.view_access())

book_available = BookUnavailableError("Beauty")
print(book_available)

#creates a library object              
my_library = Library()

#displays the output for the various methods belonghing to the library class
print(my_library.add_books("Snow White"))
print(my_library.register_user())
print(my_library.borrow_book("Power"))
print(my_library.return_book())

my_library_books = [
    "The Lord of the Rings: The Fellowship of the Ring",
    "A Game of Thrones",
    "The Hitchhiker's Guide to the Galaxy",
    "Lord of the Flies",
    "The Little Prince",
    "Pride and Prejudice",
]

LibrarySearch.search(my_library_books, book_search = "good")
LibrarySearch.search(my_library_books, book_search = "The Little Prince")
