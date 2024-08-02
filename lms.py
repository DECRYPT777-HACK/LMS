import mysql.connector
from datetime import datetime, timedelta

# Connect to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="passward",
    database="LibraryManagement"
)

cursor = db.cursor()

def add_member(name, email, phone):
    join_date = datetime.now().date()
    query = "INSERT INTO Members (name, email, phone, join_date) VALUES (%s, %s, %s, %s)"
    values = (name, email, phone, join_date)
    cursor.execute(query, values)
    db.commit()
    print("Member added successfully!")

def delete_member(member_id):
    query = "DELETE FROM Members WHERE member_id = %s"
    cursor.execute(query, (member_id,))
    db.commit()
    print("Member deleted successfully!")

def add_book(title, author, published_year):
    query = "INSERT INTO Books (title, author, published_year) VALUES (%s, %s, %s)"
    values = (title, author, published_year)
    cursor.execute(query, values)
    db.commit()
    print("Book added successfully!")

def delete_book(book_id):
    query = "DELETE FROM Books WHERE book_id = %s"
    cursor.execute(query, (book_id,))
    db.commit()
    print("Book deleted successfully!")


def issue_book(member_id, book_id):
    issue_date = datetime.now().date()
    due_date = issue_date + timedelta(days=14)  # 2 weeks loan period
    query = "INSERT INTO Transactions (member_id, book_id, issue_date, due_date, fine) VALUES (%s, %s, %s, %s, %s)"
    values = (member_id, book_id, issue_date, due_date, 0.0)
    cursor.execute(query, values)
    
    update_query = "UPDATE Books SET available = %s WHERE book_id = %s"
    cursor.execute(update_query, (False, book_id))
    
    db.commit()
    print("Book issued successfully!")

def return_book(transaction_id):
    return_date = datetime.now().date()
    query = "SELECT due_date FROM Transactions WHERE transaction_id = %s"
    cursor.execute(query, (transaction_id,))
    due_date = cursor.fetchone()[0]
    
    fine = 0.0
    if return_date > due_date:
        days_late = (return_date - due_date).days
        fine = days_late * 1.0  # $1 fine for each day late
    
    update_query = "UPDATE Transactions SET return_date = %s, fine = %s WHERE transaction_id = %s"
    cursor.execute(update_query, (return_date, fine, transaction_id))
    
    book_id_query = "SELECT book_id FROM Transactions WHERE transaction_id = %s"
    cursor.execute(book_id_query, (transaction_id,))
    book_id = cursor.fetchone()[0]
    
    book_update_query = "UPDATE Books SET available = %s WHERE book_id = %s"
    cursor.execute(book_update_query, (True, book_id))
    
    db.commit()
    print(f"Book returned successfully! Fine: ${fine:.2f}")

def main():
    while True:
        print("Library Management System")
        print("1. Add Member")
        print("2. Delete Member")
        print("3. Add Book")
        print("4. Delete Book")
        print("5. Issue Book")
        print("6. Return Book")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            name = input("Enter member name: ")
            email = input("Enter member email: ")
            phone = input("Enter member phone: ")
            add_member(name, email, phone)
        
        elif choice == '2':
            member_id = int(input("Enter member ID to delete: "))
            delete_member(member_id)
        
        elif choice == '3':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            published_year = int(input("Enter book published year: "))
            add_book(title, author, published_year)
        
        elif choice == '4':
            book_id = int(input("Enter book ID to delete: "))
            delete_book(book_id)
        
        elif choice == '5':
            member_id = int(input("Enter member ID: "))
            book_id = int(input("Enter book ID: "))
            issue_book(member_id, book_id)
        
        elif choice == '6':
            transaction_id = int(input("Enter transaction ID: "))
            return_book(transaction_id)
        
        elif choice == '7':
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
