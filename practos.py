import pickle
import os
from abc import ABC, abstractmethod

class Person(ABC):
    def __init__(self, name):
        self._name = name
    @abstractmethod
    def perform_action(self):
        pass

class User(Person):
    def __init__(self, name, borrowed_books=None):
        super().__init__(name)
        self.__borrowed_books = borrowed_books if borrowed_books else []

    def borrow_book(self, book_title, books):
        for book in books:
            if book.title == book_title:
                if book.status == "доступна":
                    book.status = "выдана"
                    self.__borrowed_books.append(book_title)
                    print(f"Вы взяли книгу: {book_title}")
                    return True
                else:
                    print("Книга уже выдана")
                    return False
        print("Книга не найдена.")
        return False

    def return_book(self, book_title, books):
        if book_title not in self.__borrowed_books:
            print("У вас нет этой книги.")
            return False
        for book in books:
            if book.title == book_title:
                book.status = "доступна"
                self.__borrowed_books.remove(book_title)
                print(f"Вы вернули книгу: {book_title}")
                return True
        return False

    def show_borrowed_books(self):
        if self.__borrowed_books:
            print("Ваши книги:")
            for book in self.__borrowed_books:
                print(f"- {book}")
        else:
            print("У вас нет взятых книг.")

    def get_borrowed_books(self):
        return self.__borrowed_books

    def perform_action(self):
        print("\nМеню пользователя")
        print("1. Просмотреть доступные книги")
        print("2. Взять книгу")
        print("3. Вернуть книгу")
        print("4. Мои книги")
        print("5. Выйти")


class Librarian(Person):
    def perform_action(self):
        print("\nМеню библиотекаря")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Зарегистрировать пользователя")
        print("4. Показать всех пользователей")
        print("5. Показать все книги")
        print("6. Выйти")

class Book:
    def __init__(self, title, author, status="доступна"):
        self.title = title
        self.author = author
        self.status = status

    def __str__(self):
        return f"{self.title} ({self.author}) - {self.status}"



def load_books():
    books = []
    try:
        with open("books2.pkl", "rb") as f:
            books=pickle.load(f)
    except FileNotFoundError:
        pass
    return books

def save_books(books):
    with open("books2.pkl", "wb") as f:
            pickle.dump(books,f)

def load_users():
    users = []
    try:

        with open("users2.pkl", "rb") as f:
            users=pickle.load(f)

    except FileNotFoundError:
        pass
    return users

def save_users(users):
    with open("users2.pkl", "wb") as f:
            pickle.dump(users,f)

def load_librarians():
    librarians = []
    try:
        with open("librarians2.pkl", "rb") as f:
            librarians=pickle.load(f)

    except FileNotFoundError:
        pass
    return librarians

def save_librarians(librarians):
    with open("librarians2.pkl", "wb") as f:
            pickle.dump(librarians,f)

def find_user(users, name):
    for user in users:
        if user._name == name:
            return user
    return None

def main():
    books = load_books()
    users = load_users()
    librarians = load_librarians()

    if not librarians:
        print("Добавьте первого библиотекаря")
        librarians.append(Librarian("Месси"))
        save_librarians(librarians)

    print("Добро пожаловать в библиотеку")
    role = input("Выберите роль (1 - библиотекарь, 2 - пользователь):крч если библиотекарь то у него для теста есть аккаунт Месси ").strip()

    if role == "1":
        name = input("Введите имя библиотекаря: ").strip()
        current_librarian = None
        for lib in librarians:
            if lib._name == name:
                current_librarian = lib
                break
        if not current_librarian:
            print("Библиотекарь не найден.")
            return

        while True:
            current_librarian.perform_action()
            choice = input("Ваш выбор: ").strip()

            if choice == "1":
                title = input("Название книги: ")
                author = input("Автор: ")
                books.append(Book(title, author))
                print("Книга добавлена.")

            elif choice == "2":
                title = input("Название книги для удаления: ")
                books = [b for b in books if b.title != title]
                print("Книга удалена (если существовала).")

            elif choice == "3":
                name = input("Имя нового пользователя: ")
                if find_user(users, name):
                    print("Пользователь уже существует.")
                else:
                    users.append(User(name))
                    print("Пользователь зарегистрирован.")

            elif choice == "4":
                if users:
                    for u in users:
                        print(f"- {u._name}")
                else:
                    print("Нет пользователей.")

            elif choice == "5":
                if books:
                    for b in books:
                        print(b)
                else:
                    print("Нет книг.")

            elif choice == "6":
                break

            else:
                print("Неверный выбор.")

    elif role == "2":
        name = input("Введите ваше имя: ").strip()
        current_user = find_user(users, name)
        if not current_user:
            print("Пользователь не найден. ")
            return

        while True:
            current_user.perform_action()
            choice = input("Ваш выбор: ").strip()

            if choice == "1":
                available = [b for b in books if b.status == "доступна"]
                if available:
                    for b in available:
                        print(f"- {b.title} ({b.author})")
                else:
                    print("Нет доступных книг.")

            elif choice == "2":
                title = input("Название книги: ")
                current_user.borrow_book(title, books)

            elif choice == "3":
                title = input("Название книги для возврата: ")
                current_user.return_book(title, books)

            elif choice == "4":
                current_user.show_borrowed_books()

            elif choice == "5":
                break

            else:
                print("Неверный выбор.")

    else:
        print("Ошииббкааа")


    save_books(books)
    save_users(users)
    save_librarians(librarians)
    print("Данные сохранены.")


if __name__ == "__main__":
    main()