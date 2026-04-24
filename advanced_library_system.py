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
        return f"\nTitle:{self.title}, Author: {self.author}, ISBN: {self._isbn}, Available: {self.available}"
     

    def mark_borrowed(self): # a method for users to borrow book 
        if self.available == True:
            self.available = False
            return f"\nYou have successfully borrowed {self.title}"
        
        else:
            return f"\n{self.title} is currently not available"
    

    def mark_returned(self): # a method for users to return borrowed book
            
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
    def view_access(self):
        pass

class StudentUser(LibraryUser):
    '''This class inherits from library user, because a student user, will always be a library user'''

    def __init__(self,name, user_id, borrowed_books ):
        super().__init__(name, user_id, borrowed_books) #initializes the inherited class method

        self.max_borrow = 3 #student user borrowing limit

    def __str__(self):
        return f"Name: {self.name}, UserId: {self.user_id}, Borrowed books: {self._borrowed_books}"


    def view_access(self):
        print(f"As a student you can borrow {self.max_borrow} books")

class AdminUser(LibraryUser):
    def __init__(self, name, user_id, borrowed_books):
        super().__init__(name, user_id, borrowed_books)
 
    def __str__(self):
        return f"Name: {self.name}, UserId: {self.user_id}, Borrowed books: {self._borrowed_books}"

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
            print(f"{filename} does not exists. \nStarting with an empty data.")
            return []
        
        try: 
            with open(filename, "r") as file:
                data = json.load(file)#convert from json to python data format
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
            {"Name": "Miracle", "Email": "miracle@gmail.com", "Role": "admin"},
            {"Name": "John", "Email": "john@gmail.com", "Role": "student"},
            {"Name": "Seyi", "Email": "seyi@gmail.com", "Role": "admin"},
            {"Name": "Josphine", "Email": "josphine@gmail.com", "Role": "student"},
            {"Name": "Betty", "Email": "betty@gmail.com", "Role": "admin"}
            ]
 
        self.borrowed_books = LibraryPersistence.load_data("borrowed.json")

        if not self.borrowed_books:
            self.borrowed_books = [] 
       

    def add_books(self):
        new_book = input("\nWhat is the name of the book you want to add?: ").title().strip()

        if new_book in self.books:
            print("Book already exists in the library.")
            return
        self.books.append(new_book)
        LibraryPersistence.save_data(self.books, self.books_file)
        print("New book has been successfully added.")


    def register_user(self): #a method to register  new users
        user_name = input("\nEnter in  valid name: ").title().strip()
        user_email = input ("Enter in a valid  email:").lower().strip()
        user_role = input("Are you a student or an admin?: ").lower().strip()

        if user_role not in ["student", "admin"]:
            return "Invalid role"
        
        for user in self.users: #checks if it is alrready a registerd user
           if user["Email"] == user_email :
                return "User has registered before"

        self.users.append({"Name": user_name, "Email": user_email, "Role": user_role}) #saves user data
        LibraryPersistence.save_data(self.users, self.users_file)
        return "New user has been successfully registered"


    def borrow_book(self, user): #a method to borrow books

        if isinstance(user, StudentUser):
            if len(user._borrowed_books) >= user.max_borrow:
               print("Limit reached for the number of books that can be borrowed.")
               return []
             
            else:
                print("'\nStudent can borrow a maximum of three books")
                user_requested_book = input("\nWhat book do you want to borrow?: ").title()
                return self._process_borrow_book(user_requested_book, user)
    
        else:
            admin_requested_book = input("What book do you want to borrow: ").title()
            return self._process_borrow_book(admin_requested_book, user)

    
    def _process_borrow_book(self, book_title, user): #helper function for borrow_book method

        try:
            if book_title not in self.books:
                raise BookUnavailableError(book_title)
        
            self.books.remove(book_title)
            self.borrowed_books.append(book_title)
            user._borrowed_books.append(book_title)
            LibraryPersistence.save_data(self.books, self.books_file)
            LibraryPersistence.save_data(self.borrowed_books, "borrowed.json")
            return "Book has been successfully borrowed."
        
        except BookUnavailableError as e:
           print(f"An error occured: {e}")

        
    def return_book(self, user):   
                 
        book_to_return = input ("\nWhat book do you want to return?: ").title().strip()

        if book_to_return not in user._borrowed_books: #checks if borrowed nook was borrowed from the library
            return f"This book was not borrowed"
        
        if book_to_return not in self.borrowed_books:
            return "Book not found in the library borrowed records"
        
        else:
           self.borrowed_books.remove(book_to_return)
           self.books.append(book_to_return)
           user._borrowed_books.remove(book_to_return)
           LibraryPersistence.save_data(self.books, self.books_file) #saves data in json
           LibraryPersistence.save_data(self.borrowed_books, "borrowed.json") #saves data in json
           return "The book has been successfully returned"
    

def run():
    print(" === Welcome to the Vantag Library Management System ===")

    #creates classes objects
    my_library = Library()                                            # defined here
    my_book = Book("Fairy tale", "Mary Jen", 1235, "Yes")             # defined here
    student_user_1 = StudentUser("Toluwani Edgal", "BU24SEN1005", []) # defined here
    admin_user_1 = AdminUser("Miracle John", 2357, [])                # defined here

   

    print(my_book)   
    print(my_library.register_user())                            
    my_library.borrow_book(student_user_1)  # accessible here
    my_library.borrow_book(admin_user_1)    # accessible here

    student_user_1.view_access()            # accessible here
    admin_user_1.view_access()              # accessible here

    print(my_library.return_book(student_user_1))  # accessible here
    print(my_library.return_book(admin_user_1))    # accessible here
    my_library.add_books()                         # accessible here
          

    print(my_book.mark_borrowed())
    print(my_book.mark_returned())

    book_available = BookUnavailableError("Beauty")
    print(book_available)

   
   
    
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


if __name__ == "__main__":
    run()