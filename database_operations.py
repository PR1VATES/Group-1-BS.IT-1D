import sqlite3
from tkinter import messagebox
from reportlab.pdfgen import canvas

def create_database():
    # Create SQLite database and table for storing reservations
    conn = sqlite3.connect('airline_reservation.db')  # Connect to the SQLite database or create it if it doesn't exist
    cursor = conn.cursor()  # Create a cursor object to interact with the database
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            source TEXT,
            destination TEXT,
            departure_date TEXT,
            return_date TEXT,
            age INTEGER,
            travel_class TEXT,
            seat_number INTEGER
        )
    ''')  # Create a table called 'reservations' if it doesn't exist with the specified columns
    conn.commit()  # Commit changes to the database
    conn.close()  # Close the database connection

def make_reservation(name, source, destination, departure_date, return_date, age, travel_class, seat_number):
    create_database()  # Ensure that the database and table exist before making a reservation

    # Validate input: Check if all fields are filled
    if not all([name, source, destination, departure_date, return_date, age, travel_class, seat_number]):
        messagebox.showerror("Error", "Please fill in all fields.")  # Show error message if any field is empty
        return

    # Check availability and make reservation
    conn = sqlite3.connect('airline_reservation.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute('''
        INSERT INTO reservations (name, source, destination, departure_date, return_date, age, travel_class, seat_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, source, destination, departure_date, return_date, age, travel_class, seat_number))  # Insert reservation details into the database
    conn.commit()  # Commit changes to the database
    conn.close()  # Close the database connection

    messagebox.showinfo("Success", "Reservation made successfully.")  # Show success message

def check_availability(departure_date, seat_number):
    create_database()  # Ensure that the database and table exist before checking availability

    # Check if the seat number and date are available
    conn = sqlite3.connect('airline_reservation.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute('SELECT * FROM reservations WHERE departure_date=? AND seat_number=?', (departure_date, seat_number))
    result = cursor.fetchone()  # Fetch the first matching row
    conn.close()  # Close the database connection

    if result:
        messagebox.showinfo("Availability", f"The seat number {seat_number} on {departure_date} is not available.")  # Show message if seat is not available
    else:
        messagebox.showinfo("Availability", f"The seat number {seat_number} on {departure_date} is available.")  # Show message if seat is available

def show_available_schedules(tree):
    create_database()  # Ensure that the database and table exist before displaying schedules

    # Clear previous data from the Treeview
    for item in tree.get_children():
        tree.delete(item)

    # Get all available schedules from the database
    conn = sqlite3.connect('airline_reservation.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute('SELECT * FROM reservations')  # Retrieve all rows from the 'reservations' table
    schedules = cursor.fetchall()  # Fetch all rows as a list of tuples
    conn.close()  # Close the database connection

    # Display schedules in the Treeview
    for schedule in schedules:
        tree.insert("", "end", values=schedule)  # Insert each schedule as a new row in the Treeview


def delete_reservation_from_database(reservation_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('airline_reservation.db')
    cursor = conn.cursor()

    # Delete the reservation with the given ID
    cursor.execute('DELETE FROM reservations WHERE id = ?', (reservation_id,))
    conn.commit()

    # Close the database connection
    conn.close()

    # Show success message
    messagebox.showinfo("Success", "Reservation deleted successfully.")

def close_database_connection():
    # Close the SQLite database connection
    conn = sqlite3.connect('airline_reservation.db')  # Connect to the SQLite database
    conn.close()  # Close the database connection

def generate_pdf(filename, reservation_details):
    # Create a PDF document
    pdf = canvas.Canvas(filename)  # Create a PDF canvas with the specified filename

    # Set font and size
    pdf.setFont("Helvetica", 12)  # Set the font and size for text in the PDF

    # Add reservation details to the PDF
    pdf.drawString(100, 800, "Reservation Details:")  # Add heading for reservation details
    pdf.drawString(100, 780, f"Reservation ID: {reservation_details[0]}")  # Add reservation ID
    pdf.drawString(100, 760, f"Name: {reservation_details[1]}")  # Add passenger name
    pdf.drawString(100, 740, f"From: {reservation_details[2]}")  # Add source
    pdf.drawString(100, 720, f"To: {reservation_details[3]}")  # Add destination
    pdf.drawString(100, 700, f"Departure Date: {reservation_details[4]}")  # Add departure date
    pdf.drawString(100, 680, f"Return Date: {reservation_details[5]}")  # Add return date
    pdf.drawString(100, 660, f"Age: {reservation_details[6]}")  # Add passenger age
    pdf.drawString(100, 640, f"Email: {reservation_details[7]}")  # Add email
    pdf.drawString(100, 620, f"Phone Number: {reservation_details[8]}")  # Add phone number
    pdf.drawString(100, 600, f"Travel Class: {reservation_details[9]}")  # Add travel class
    pdf.drawString(100, 580, f"Seat Number: {reservation_details[10]}")  # Add seat number
    pdf.drawString(100, 560, f"Number of Persons: {reservation_details[11]}")  # Add number of persons
    pdf.drawString(100, 540, f"Departure Time: {reservation_details[12]}")  # Add departure time

    # Save the PDF
    pdf.save()