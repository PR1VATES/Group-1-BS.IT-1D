from tkinter import Tk, Label, StringVar, Entry, Button, OptionMenu, ttk, messagebox, Frame, font
from tkcalendar import DateEntry
from tkinter import Toplevel, Button
from database_operations import generate_pdf, close_database_connection
from tkinter import Canvas, Scrollbar
import sqlite3
import random

class AirlineReservationGUI:
    def __init__(self, root):
        self.seat_selection_window = None
        self.root = root
        self.root.title("Airline Reservation System")
        self.root.geometry("1200x600")  # Set GUI size to 800x700
        self.root.resizable(False, False)  # Disable window resizing

        # Define custom font size
        custom_font = font.Font(size=13)  # Change 12 to your desired font size

        # Initialize database connection and cursor
        self.conn = sqlite3.connect('airline_reservation.db')
        self.cursor = self.conn.cursor()

        # Create reservations table if not exists
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS reservations (
                                id INTEGER PRIMARY KEY,
                                name TEXT NOT NULL,
                                source TEXT NOT NULL,
                                destination TEXT NOT NULL,
                                departure_date TEXT NOT NULL,
                                return_date TEXT NOT NULL,
                                age INTEGER NOT NULL,
                                email TEXT NOT NULL,
                                phone_number TEXT NOT NULL,
                                travel_class TEXT NOT NULL,
                                seat_number TEXT NOT NULL,
                                number_of_persons INTEGER NOT NULL,
                                departure_time TEXT NOT NULL
                            )''')
        self.conn.commit()

        # Labels for input fields with left alignment
        Label(root, text="Name:", font=custom_font, anchor="w").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        Label(root, text="From:", font=custom_font, anchor="w").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        Label(root, text="To:", font=custom_font, anchor="w").grid(row=1, column=2, padx=10, pady=5, sticky="w")
        Label(root, text="Return Date:", font=custom_font, anchor="w").grid(row=2, column=2, padx=10, pady=5, sticky="w")
        Label(root, text="Age:", font=custom_font, anchor="w").grid(row=3, column=0, padx=10, pady=5, sticky="w")
        Label(root, text="Email:", font=custom_font, anchor="w").grid(row=3, column=2, padx=10, pady=5, sticky="w")
        Label(root, text="Phone Number:", font=custom_font, anchor="w").grid(row=4, column=0, padx=10, pady=5, sticky="w")
        Label(root, text="Travel Class:", font=custom_font, anchor="w").grid(row=4, column=2, padx=10, pady=5, sticky="w")
        Label(root, text="Departure Date:", font=custom_font, anchor="w").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        Label(root, text="Number of Persons:", font=custom_font, anchor="w").grid(row=5, column=0, padx=10, pady=5, sticky="w")
        Label(root, text="Seat Number:", font=custom_font, anchor="w").grid(row=6, column=0, padx=10, pady=5, sticky="w")

        # Entry widgets for user input
        self.name_entry = Entry(root, font=custom_font)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        # OptionMenus for selecting countries
        self.from_var = StringVar(root)
        self.from_var.set("Select Country")
        OptionMenu(root, self.from_var, "Tokyo", "Seoul", "Sydney", "Paris", "London", "New York", "Berlin", "Madrid", "Philippines").grid(row=1, column=1, sticky="w")
        self.to_var = StringVar(root)
        self.to_var.set("Select Country")
        OptionMenu(root, self.to_var, "Tokyo", "Seoul", "Sydney", "Paris", "London", "New York", "Berlin", "Madrid", "Philippines").grid(row=1, column=3, sticky="w")

        # DateEntry widgets for selecting dates
        self.departure_date_entry = DateEntry(root, width=12, background="white", foreground="grey", date_pattern="yyyy-mm-dd", font=custom_font)
        self.departure_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.return_date_entry = DateEntry(root, width=12, background="white", foreground="grey", date_pattern="yyyy-mm-dd", font=custom_font)
        self.return_date_entry.grid(row=2, column=3, padx=10, pady=5, sticky="w")

        # Entry widget for age input
        self.age_entry = Entry(root, font=custom_font)
        self.age_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        self.age_entry.config(validate="key", validatecommand=(root.register(self.validate_number), '%P'))

        # Entry widgets for email and phone number input
        self.email_entry = Entry(root, font=custom_font)
        self.email_entry.grid(row=3, column=3, padx=10, pady=5, sticky="w")

        self.phone_entry = Entry(root, font=custom_font)
        self.phone_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # OptionMenu for selecting travel class
        self.travel_class_var = StringVar(root)
        self.travel_class_var.set("Economy")
        OptionMenu(root, self.travel_class_var, "Economy", "Business", "First Class").grid(row=4, column=3, sticky="w")

        # Entry widget for number of persons
        self.num_persons_entry = Entry(root, font=custom_font)
        self.num_persons_entry.grid(row=5, column=1, padx=10, pady=5, sticky="w")
        self.num_persons_entry.config(validate="key", validatecommand=(root.register(self.validate_number), '%P'))

        # Label to display selected seat number
        self.selected_seat_label = Label(root, text="", font=custom_font)
        self.selected_seat_label.grid(row=6, column=1, padx=10, pady=5, sticky="w")

        # Buttons for actions
        Button(root, text="Make Reservation", command=self.make_reservation, font=custom_font).grid(row=7, column=0, pady=5, padx=5, sticky="w")
        Button(root, text="Print Reservation (PDF)", command=self.print_reservation_pdf, font=custom_font).grid(row=7, column=1, pady=5, padx=5, sticky="w")
        Button(root, text="Remove Reservation", command=self.remove_reservation, font=custom_font).grid(row=7, column=2, pady=5, padx=5, sticky="w")
        Button(root, text="Select Seat", command=self.open_seat_selection_popup, font=custom_font).grid(row=6, column=2, pady=5, padx=5, sticky="w")
            
        # Treeview for displaying available schedules
        self.tree_frame = Frame(root)
        self.tree_frame.grid(row=9, column=0, columnspan=4, padx=10, pady=10, sticky="w")
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Name", "From", "To", "Departure Date", "Return Date",  "Age" ,"Email" , "Phone Number","Travel Class",  "Seat Number", "Number of Persons", "Departure Time"), show="headings")
        self.tree.pack(side="left", fill="both", expand=True)

        # Set column headings for the Treeview
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("From", text="From")
        self.tree.heading("To", text="To")
        self.tree.heading("Departure Date", text="Departure Date")
        self.tree.heading("Return Date", text="Return Date")
        self.tree.heading("Departure Time", text="Departure Time")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Phone Number", text="Phone Number")
        self.tree.heading("Travel Class", text="Travel Class")
        self.tree.heading("Seat Number", text="Seat Number")
        self.tree.heading("Number of Persons", text="No. Passengers")

        # Set column widths for the Treeview
        self.tree.column("ID", width=30, anchor="center")
        self.tree.column("Name", width=100, anchor="center")
        self.tree.column("From", width=100, anchor="center")
        self.tree.column("To", width=100, anchor="center")
        self.tree.column("Departure Date", width=100, anchor="center")
        self.tree.column("Return Date", width=100, anchor="center")
        self.tree.column("Departure Time", width=100, anchor="center")
        self.tree.column("Age", width=50, anchor="center")
        self.tree.column("Email", width=150, anchor="center")
        self.tree.column("Phone Number", width=100, anchor="center")
        self.tree.column("Travel Class", width=80, anchor="center")
        self.tree.column("Seat Number", width=80, anchor="center")
        self.tree.column("Number of Persons", width=100, anchor="center")

        # Display available schedules as soon as GUI launches
        self.show_available_schedules()
        
    def open_seat_selection_popup(self):
        # Check if the seat selection window is already open
        if self.seat_selection_window is not None and self.seat_selection_window.winfo_exists():
            self.seat_selection_window.destroy()

        # Create a new window for seat selection
        self.seat_selection_window = Toplevel(self.root)
        self.seat_selection_window.title("Seat Selection")

        # Create a canvas for the seat grid
        canvas = Canvas(self.seat_selection_window, width=200, height=200, bg="white")
        canvas.pack(side="left", fill="both", expand=True)

        # Create a frame for the scrollable area
        seat_frame = Frame(canvas)
        seat_frame.bind("<Configure>", lambda event, canvas=canvas: canvas.configure(scrollregion=canvas.bbox("all")))

        # Add scrollbars
        scrollbar = Scrollbar(self.seat_selection_window, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add buttons for seat selection
        for i in range(1, 201):  # Assuming 200 max number of seats
            btn = Button(seat_frame, text=str(i), command=lambda num=i: self.select_seat(num))
            btn.grid(row=(i - 1) // 4, column=(i - 1) % 4, padx=5, pady=5)

            # Highlight button if seat already selected
            if self.is_seat_selected(self.departure_date_entry.get_date().strftime('%Y-%m-%d'), self.from_var.get(), str(i)):
                btn.config(bg="blue")

        # Place seat frame on canvas
        canvas.create_window((0, 0), window=seat_frame, anchor="nw")

    def is_seat_selected(self, departure_date, source, seat_number):
        # Check if the seat is already selected for the specific date and location
        self.cursor.execute('''
            SELECT * FROM reservations
            WHERE departure_date=? AND source=? AND seat_number=?
        ''', (departure_date, source, seat_number))
        return self.cursor.fetchone() is not None

    def select_seat(self, seat_number):
        # Set the selected seat number in the label
        self.selected_seat_label.config(text=str(seat_number))

    def validate_number(self, value):
        # Validate if the input is a valid integer
        try:
            if value:
                int(value)
            return True
        except ValueError:
            return False

    def check_duplicate_reservation(self, departure_date, source, seat_number):
        # Check if there is an existing reservation with the same departure date, source location, and seat number
        self.cursor.execute('''
            SELECT * FROM reservations
            WHERE departure_date=? AND source=? AND seat_number=?
        ''', (departure_date, source, seat_number))
        existing_reservation = self.cursor.fetchone()
        return existing_reservation is not None

    def make_reservation(self):
        # Get values from the GUI
        name = self.name_entry.get()
        source = self.from_var.get()
        destination = self.to_var.get()
        departure_date = self.departure_date_entry.get_date().strftime('%Y-%m-%d')
        return_date = self.return_date_entry.get_date().strftime('%Y-%m-%d')
        age = self.age_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_entry.get()
        travel_class = self.travel_class_var.get()
        seat_number = self.selected_seat_label.cget("text")
        num_persons = self.num_persons_entry.get()  # Get number of persons

        # Check if all required fields are filled
        if not (name and source and destination and departure_date and return_date and age and email and phone_number and travel_class and seat_number and num_persons):
            messagebox.showinfo("Error", "Please fill in all required fields.")
            return

        # Check if "From" and "To" countries are selected
        if source == "Select Country" or destination == "Select Country":
            messagebox.showinfo("Error", "Please select departure and destination countries.")
            return

        # Check for duplicate reservation for the selected seat
        if self.check_duplicate_reservation(departure_date, source, seat_number):
            messagebox.showinfo("Error", "This seat is already reserved by another passenger.")
            return

        # Generate a random time in 12-hour format for departure_time
        hour = random.randint(1, 12)
        minute = random.randint(0, 59)
        am_pm = random.choice(["AM", "PM"])
        departure_time = f"{hour:02d}:{minute:02d} {am_pm}"

        # Insert the reservation into the database
        try:
            self.cursor.execute('''
                INSERT INTO reservations (name, source, destination, departure_date, return_date, age, email, phone_number, travel_class, seat_number, number_of_persons, departure_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, source, destination, departure_date, return_date, age, email, phone_number, travel_class, seat_number, num_persons, departure_time))
            self.conn.commit()
            messagebox.showinfo("Success", "Reservation made successfully.")
            # Refresh the Treeview to reflect the changes
            self.show_available_schedules()
        except Exception as e:
            messagebox.showinfo("Error", f"Failed to make reservation: {str(e)}")

    def show_available_schedules(self):
        # Clear existing items in the Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Retrieve and display available schedules in the Treeview
        self.cursor.execute("SELECT * FROM reservations")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row)

    def print_reservation_pdf(self):
        # Get the selected reservation ID from the Treeview
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Error", "Please select a reservation to print.")
            return
        reservation_id = self.tree.item(selected_item)['values'][0]

        # Get reservation details including email and phone number
        reservation_details = self.get_reservation_details(reservation_id)

        if not reservation_details:
            messagebox.showinfo("Error", "Failed to retrieve reservation details.")
            return

        # Generate PDF for the selected reservation
        pdf_filename = f"reservation_{reservation_id}.pdf"
        generate_pdf(pdf_filename, reservation_details)
        messagebox.showinfo("Success", f"PDF generated successfully: {pdf_filename}")

    def remove_reservation(self):
        # Ask for confirmation before removing the reservation
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to remove this reservation?")
        if confirmation:
            # Get the selected reservation ID from the Treeview
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showinfo("Error", "Please select a reservation to remove.")
                return
            reservation_id = self.tree.item(selected_item)['values'][0]

            # Remove the selected reservation from the database
            self.cursor.execute('DELETE FROM reservations WHERE id=?', (reservation_id,))
            self.conn.commit()

            # Show success message
            messagebox.showinfo("Success", f"Reservation {reservation_id} removed successfully.")

            # Refresh the Treeview to reflect the changes
            self.show_available_schedules()

    def get_reservation_details(self, reservation_id):
        # Retrieve reservation details from the database based on ID
        self.cursor.execute('SELECT * FROM reservations WHERE id=?', (reservation_id,))
        reservation_details = self.cursor.fetchone()
        return reservation_details

if __name__ == "__main__":
    root = Tk()
    app = AirlineReservationGUI(root)
    root.mainloop()

    # Close the database connection when the application is closed
    close_database_connection()
