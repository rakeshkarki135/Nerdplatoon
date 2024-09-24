
class Book:
     def __init__(self,title,author,isbn,available_copies):
          self.title = title
          self.author = author 
          self.isbn = isbn    
          self.available_copies = available_copies
          
          
     def borrow(self):
          if self.available_copies > 0:
               self.available_copies -= 1
               print(f"Book {self.title} is Borrowed")
          else:
               print(f"Book {self.title} is not available")
          
     def return_book(self):
          self.available_copies +=  1
          print(f"Book {self.title} is returned")
          

class Member:
     def __init__(self,name,member_id,borrowed_books):
          self.name = name
          self.member_id = member_id
          self.borrowed_books = []
          
     def borrow_book(self, book):
          if len(self.borrowed_books) > 2:
               print("Your limit has reached")
          else:
               book.borrow()
               self.borrowed_books.append(book)
               
     def return_book(self,book):
          if book in self.borrowed_books:
               book.return_book()
               self.borrowed_books.remove(book)
          else:
               print("you have not borrowed this book")
               
               
class Library:
     def __init__(self):
          self.books = []
          self.members = []
          
     def add_book(self,book):
          self.books.append(book)
          print(f"Book added : {book} ")
          
     def add_member(self,member):
          self.members.append(member)
          print(f"Member added : {member} ")
          
     def issue_book(self, member,book):
          if book in self.books and member in self.members:
               if book.available_copies > 0:
                    member.borrow_book(book)
                    
               else:
                    print(f"Not Available : {book}")
               
          else:
               print("Member or Book is not found")
          
     
     def return_book(self, member, book):
          if book in self.books and member in self.members:
               member.return_book(book)
          else:
               print("Book or member not found")
                         
                    

          
book1 = Book("1984", "George Orwell", "12345", 5)
book2 = Book("To Kill a Mockingbird", "Harper Lee", "67890", 3)
book3 = Book("The Great Gatsby", "F. Scott Fitzgerald", "54321", 2)

member1 = Member("ram", "M001", 1)
member2 = Member("hari", "M002",2)

library = Library()
library.add_book(book1)
library.add_book(book2)
library.add_book(book3)


library.add_member(member1)
library.add_member(member2)


print("\n--- Transactions ---")

print("ram borrow book")
library.issue_book(member1, book1)

print("hari tries to buy book")
library.issue_book(member2, book1)

print("ram return book")
library.return_book(member1, book1)

print("hari borrow book after returned")
library.issue_book(member2, book1)

print("ram tries to return book she hasnt borrowed")
library.return_book(member1, book2)