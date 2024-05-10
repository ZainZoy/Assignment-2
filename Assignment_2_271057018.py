import os
import pickle


class CinemaSystem:

    def __init__(self):
        self.movies = {}
        self.screens = {}

    def add_movie(self, title, genre, seats):
        self.movies[title] = {"Genre": genre, "Seats_available": list(range(1, seats + 1))}
        print("Movie added")

    def remove_movie(self, title):
        if title in self.movies:
            del self.movies[title]
            print("Movie removed")
        else:
            print("Movie not found")

    def print_movie_list(self):
        print("Available movies:")
        for title, info in self.movies.items():
            print(f"Title: {title}, Genre: {info['Genre']}, Seats available: {info['Seats_available']}")

    def add_screen(self, screen_type):
        self.screens[screen_type] = []
        print(f"Screen of type {screen_type} added")

    def fill_time_slot(self, screen_type, time, movie_title):
        if screen_type in self.screens:
            self.screens[screen_type].append({"Time": time, "Movie": movie_title})
            print(f"Time slot filled for screen type {screen_type} with movie {movie_title} at time {time}")
        else:
            print(f"Screen type {screen_type} does not exist")

    def book_seats(self, movie_title, seat):
        if movie_title in self.movies:
            if seat in self.movies[movie_title]["Seats_available"]:
                self.movies[movie_title]["Seats_available"].remove(seat)
                print(f"Seat {seat} has been booked for {movie_title}")
            else:
                print(f"Seat {seat} is not available for {movie_title}")
        else:
            print(f"Movie {movie_title} not found")


class User:

    def __init__(self, cinema_system):
        self.cinema_system = cinema_system

    def book_seats(self, movie_title, seat):
        self.cinema_system.book_seats(movie_title, seat)


class AdminActions:

    def __init__(self, cinema_system):
        self.cinema_system = cinema_system

    def add_movie(self):
        title = input("Enter the movie title: ")
        genre = input("Enter the movie genre: ")
        seats = int(input("Enter the number of seats available: "))
        self.cinema_system.add_movie(title, genre, seats)

    def remove_movie(self):
        title = input("Enter the title of the movie to remove: ")
        self.cinema_system.remove_movie(title)

    def add_screen(self):
        screen_type = input("Enter the type of screen: ")
        self.cinema_system.add_screen(screen_type)

    def fill_time_slots(self):
        screen_type = input("Enter the screen type: ")
        time = input("Enter the time slot: ")
        movie_title = input("Enter the movie title: ")
        self.cinema_system.fill_time_slot(screen_type, time, movie_title)


class UserActions:

    def __init__(self, cinema_system):
        self.cinema_system = cinema_system

    def view_movie_details(self):
        self.cinema_system.print_movie_list()

    def book_movie_ticket(self):
        movie_title = input("Enter the movie title you want to book: ")
        seat = int(input("Enter the seat number you want to book: "))
        self.cinema_system.book_seats(movie_title, seat)


def save_data(data_to_save, filename):
    with open(filename, "wb") as file_to_write:
        pickle.dump(data_to_save, file_to_write)


def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as file_to_read:
            return pickle.load(file_to_read)
    return {}


data_loaded = load_data("new_data.pkl")

print("Welcome to ZZFlix Cinema System")

while True:
    print("1 - Sign Up\n2 - Login\n3 - Exit")
    choice = int(input("Choose any of the above options: "))

    if choice == 1:
        username = input("Enter your username: ")
        password = input("Enter your password (least 7 characters long): ")

        if len(password) <=7 :
            print("Password should be at least 7 characters long. Please enter again.")
            continue

        if username in data_loaded:
            print("Username already exists. Please try again.")
            continue

        data_loaded[username] = password
        save_data(data_loaded, "new_data.pkl")
        print("Account created successfully!")

    elif choice == 2:
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        if username not in data_loaded or data_loaded[username] != password:
            print("Invalid username or password. Please try again.")
            continue

        print("Login successful!")

        entity = int(input("Select entity:\n1 - User\n2 - Admin\nEnter: "))
        if entity == 1:  # User
            cinema_system = CinemaSystem()  # Create an instance of CinemaSystem
            user_actions = UserActions(cinema_system)
            user_actions.view_movie_details()
            user_actions.book_movie_ticket()

        elif entity == 2:
            cinema_system = CinemaSystem()  # Create an instance of CinemaSystem
            admin_actions = AdminActions(cinema_system)
            action = int(
                input("Select action:\n1 - Add Movie\n2 - Remove Movie\n3 - Add Screen\n4 - Fill Time Slots\nEnter: "))

            if action == 1:
                admin_actions.add_movie()
            elif action == 2:
                admin_actions.remove_movie()
            elif action == 3:
                admin_actions.add_screen()
            elif action == 4:
                admin_actions.fill_time_slots()
            else:
                print("Invalid action")

    elif choice == 3:
        print("Thank you for using our ZZFlix Cinema System")
        break

    else:
        print("Invalid choice. Please select a valid option.")
