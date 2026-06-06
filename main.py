from db import conn, cursor


class MovieBooking:

    def add_movie(self):
        movie_name = input("Enter Movie Name: ")
        seats = int(input("Enter Total Seats: "))

        try:
            cursor.execute(
                "INSERT INTO Movies(MovieName, AvailableSeats) VALUES (?, ?)",
                (movie_name, seats)
            )

            conn.commit()

            print("Movie Added Successfully!")

        except:
            print("Movie Already Exists!")

    def show_movies(self):

        cursor.execute("SELECT * FROM Movies")

        movies = cursor.fetchall()

        if not movies:
            print("No Movies Available!")
            return

        print("\nAvailable Movies")
        print("-" * 50)

        for movie in movies:
            print(
                f"ID: {movie.MovieId} | "
                f"Movie: {movie.MovieName} | "
                f"Seats: {movie.AvailableSeats}"
            )

    def book_ticket(self):

        movie_name = input("Enter Movie Name: ")

        cursor.execute(
            "SELECT AvailableSeats FROM Movies WHERE MovieName=?",
            (movie_name,)
        )

        movie = cursor.fetchone()

        if not movie:
            print("Movie Not Found!")
            return

        seats = int(input("Enter Number Of Tickets: "))

        if seats > movie.AvailableSeats:
            print("Seats Not Available!")
            return

        remaining = movie.AvailableSeats - seats

        cursor.execute(
            "UPDATE Movies SET AvailableSeats=? WHERE MovieName=?",
            (remaining, movie_name)
        )

        conn.commit()

        print("Ticket Booked Successfully!")

    def cancel_ticket(self):

        movie_name = input("Enter Movie Name: ")

        cursor.execute(
            "SELECT AvailableSeats FROM Movies WHERE MovieName=?",
            (movie_name,)
        )

        movie = cursor.fetchone()

        if not movie:
            print("Movie Not Found!")
            return

        seats = int(input("Enter Number Of Tickets To Cancel: "))

        total = movie.AvailableSeats + seats

        cursor.execute(
            "UPDATE Movies SET AvailableSeats=? WHERE MovieName=?",
            (total, movie_name)
        )

        conn.commit()

        print("Ticket Cancelled Successfully!")

    def delete_movie(self):

        movie_name = input("Enter Movie Name To Delete: ")

        cursor.execute(
            "DELETE FROM Movies WHERE MovieName=?",
            (movie_name,)
        )

        conn.commit()

        print("Movie Deleted Successfully!")


booking = MovieBooking()

while True:

    print("\n")
    print("=" * 40)
    print("MOVIE BOOKING SYSTEM")
    print("=" * 40)
    print("1. Add Movie")
    print("2. Book Ticket")
    print("3. Cancel Ticket")
    print("4. Show Movies")
    print("5. Delete Movie")
    print("6. Exit")

    try:

        choice = int(input("Enter Choice: "))

        if choice == 1:
            booking.add_movie()

        elif choice == 2:
            booking.book_ticket()

        elif choice == 3:
            booking.cancel_ticket()

        elif choice == 4:
            booking.show_movies()

        elif choice == 5:
            booking.delete_movie()

        elif choice == 6:
            print("Thank You!")
            break

        else:
            print("Invalid Choice!")

    except ValueError:
        print("Please Enter Valid Number!")