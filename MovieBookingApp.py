
import streamlit as st
import pyodbc
import pandas as pd

# ================= DATABASE =================

conn = pyodbc.connect(
    # "Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=MovieDB;Trusted_Connection=True;"
    
    r"Driver={SQL Server};Server=localhost\SQLEXPRESS;Database=MovieDB;Trusted_Connection=True;"

)

cursor = conn.cursor()

# ================= PAGE CONFIG =================

st.set_page_config(
    page_title="Movie Booking System",
    page_icon="🎬",
    layout="wide"
)

# ================= CSS =================

st.markdown("""
<style>

.main{
    background-color:#f5f7fa;
}

.title{
    text-align:center;
    color:#ff4b4b;
    font-size:45px;
    font-weight:bold;
}

.card{
    padding:20px;
    border-radius:15px;
    background:white;
}

</style>
""", unsafe_allow_html=True)

# ================= HEADER =================

st.markdown(
    "<div class='title'>🎬 Movie Booking System</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# ================= SIDEBAR =================

menu = st.sidebar.radio(
    "🎥 Navigation",
    [
        "🏠 Dashboard",
        "➕ Add Movie",
        "🎟️ Book Ticket",
        "❌ Cancel Ticket",
        "📋 Show Movies",
        "🗑️ Delete Movie"
    ]
)

# ================= DASHBOARD =================

if menu == "🏠 Dashboard":

    cursor.execute("SELECT COUNT(*) FROM Movies")
    total_movies = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(AvailableSeats) FROM Movies")
    seats = cursor.fetchone()[0]

    if seats is None:
        seats = 0

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            label="🎥 Total Movies",
            value=total_movies
        )

    with col2:
        st.metric(
            label="🎟️ Available Seats",
            value=seats
        )

    st.info("Welcome to Movie Booking System")

# ================= ADD MOVIE =================

elif menu == "➕ Add Movie":

    st.subheader("➕ Add New Movie")

    with st.form("add_movie"):

        movie_name = st.text_input(
            "🎥 Movie Name"
        )

        seats = st.number_input(
            "🎟️ Total Seats",
            min_value=1
        )

        submit = st.form_submit_button(
            "Add Movie"
        )

        if submit:

            try:

                cursor.execute(
                    """
                    INSERT INTO Movies
                    (MovieName, AvailableSeats)
                    VALUES (?,?)
                    """,
                    (movie_name, seats)
                )

                conn.commit()

                st.success(
                    "Movie Added Successfully"
                )

                st.balloons()

            except:
                st.error(
                    "Movie Already Exists"
                )

# ================= SHOW MOVIES =================

elif menu == "📋 Show Movies":

    st.subheader("🎥 Available Movies")

    search = st.text_input(
        "🔍 Search Movie"
    )

    cursor.execute(
        "SELECT * FROM Movies"
    )

    rows = cursor.fetchall()

    data = []

    for row in rows:

        if search.lower() in row.MovieName.lower():

            data.append(
                {
                    "Movie ID": row.MovieId,
                    "Movie Name": row.MovieName,
                    "Available Seats": row.AvailableSeats
                }
            )

    if data:

        df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True
        )

    else:
        st.warning(
            "No Movies Found"
        )

# ================= BOOK TICKET =================

elif menu == "🎟️ Book Ticket":

    st.subheader("🎟️ Book Ticket")

    movie_name = st.text_input(
        "Movie Name"
    )

    tickets = st.number_input(
        "Number Of Tickets",
        min_value=1
    )

    if st.button("Book Ticket"):

        cursor.execute(
            """
            SELECT AvailableSeats
            FROM Movies
            WHERE MovieName=?
            """,
            (movie_name,)
        )

        movie = cursor.fetchone()

        if movie:

            if movie.AvailableSeats >= tickets:

                remaining = (
                    movie.AvailableSeats
                    - tickets
                )

                cursor.execute(
                    """
                    UPDATE Movies
                    SET AvailableSeats=?
                    WHERE MovieName=?
                    """,
                    (
                        remaining,
                        movie_name
                    )
                )

                conn.commit()

                st.success(
                    "Ticket Booked Successfully"
                )

                st.balloons()

            else:
                st.error(
                    "Seats Not Available"
                )

        else:
            st.error(
                "Movie Not Found"
            )

# ================= CANCEL TICKET =================

elif menu == "❌ Cancel Ticket":

    st.subheader("❌ Cancel Ticket")

    movie_name = st.text_input(
        "Movie Name"
    )

    tickets = st.number_input(
        "Tickets To Cancel",
        min_value=1
    )

    if st.button("Cancel Ticket"):

        cursor.execute(
            """
            SELECT AvailableSeats
            FROM Movies
            WHERE MovieName=?
            """,
            (movie_name,)
        )

        movie = cursor.fetchone()

        if movie:

            total = (
                movie.AvailableSeats
                + tickets
            )

            cursor.execute(
                """
                UPDATE Movies
                SET AvailableSeats=?
                WHERE MovieName=?
                """,
                (
                    total,
                    movie_name
                )
            )

            conn.commit()

            st.success(
                "Ticket Cancelled"
            )

        else:
            st.error(
                "Movie Not Found"
            )

# ================= DELETE MOVIE =================

elif menu == "🗑️ Delete Movie":

    st.subheader("🗑️ Delete Movie")

    movie_name = st.text_input(
        "Movie Name"
    )

    if st.button("Delete Movie"):

        cursor.execute(
            """
            DELETE FROM Movies
            WHERE MovieName=?
            """,
            (movie_name,)
        )

        conn.commit()

        st.success(
            "Movie Deleted Successfully"
        )

# ================= FOOTER =================

st.markdown("---")

st.markdown(
    """
    <center>
    🎬 Movie Booking System <br>
    Developed By Laxit Dange 🚀
    </center>
    """,
    unsafe_allow_html=True
)