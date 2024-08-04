import mysql.connector
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk


# Establishing connection to the MySQL database
conn = mysql.connector.connect(host="localhost", user="root", password="1234", database="airline_mgmt")
cursor = conn.cursor()

# Tkinter root window
root = tk.Tk()
root.title("Airline Management System")
root.attributes('-fullscreen', True)
root.configure(bg="#ADD8E6")

def set_background_image():
    bg_image = Image.open("aero.png")
    bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.Resampling.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    if hasattr(root, 'bg_label'):
        root.bg_label.config(image=bg_photo)
        root.bg_label.image = bg_photo
    else:
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)
        root.bg_label = bg_label
        root.bg_label.image = bg_photo

set_background_image()

def add_flight():
    def submit_flight():
        flight_number = flight_number_entry.get()
        origin = origin_entry.get()
        destination = destination_entry.get()
        departure_time = departure_time_entry.get()
        arrival_time = arrival_time_entry.get()
        seats_available = int(seats_available_entry.get())
        
        query = """INSERT INTO flights (flight_number, origin, destination, departure_time, arrival_time, seats_available)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(query, (flight_number, origin, destination, departure_time, arrival_time, seats_available))
        conn.commit()
        messagebox.showinfo("Success", "Flight added successfully!")
        add_flight_window.destroy()

    add_flight_window = tk.Toplevel(root)
    add_flight_window.title("Add Flight")
    add_flight_window.configure(bg="#ADD8E6")

    tk.Label(add_flight_window, text="Flight Number:", bg="#ADD8E6", fg="black").grid(row=0, column=0)
    flight_number_entry = tk.Entry(add_flight_window)
    flight_number_entry.grid(row=0, column=1)

    tk.Label(add_flight_window, text="Origin:", bg="#ADD8E6", fg="black").grid(row=1, column=0)
    origin_entry = tk.Entry(add_flight_window)
    origin_entry.grid(row=1, column=1)

    tk.Label(add_flight_window, text="Destination:", bg="#ADD8E6", fg="black").grid(row=2, column=0)
    destination_entry = tk.Entry(add_flight_window)
    destination_entry.grid(row=2, column=1)

    tk.Label(add_flight_window, text="Departure Time (YYYY-MM-DD HH:MM:SS):", bg="#ADD8E6", fg="black").grid(row=3, column=0)
    departure_time_entry = tk.Entry(add_flight_window)
    departure_time_entry.grid(row=3, column=1)

    tk.Label(add_flight_window, text="Arrival Time (YYYY-MM-DD HH:MM:SS):", bg="#ADD8E6", fg="black").grid(row=4, column=0)
    arrival_time_entry = tk.Entry(add_flight_window)
    arrival_time_entry.grid(row=4, column=1)

    tk.Label(add_flight_window, text="Seats Available:", bg="#ADD8E6", fg="black").grid(row=5, column=0)
    seats_available_entry = tk.Entry(add_flight_window)
    seats_available_entry.grid(row=5, column=1)

    tk.Button(add_flight_window, text="Submit", command=submit_flight, bg="black", fg="white", width=20, height=2, font=("Helvetica", 12)).grid(row=6, columnspan=2, pady=10)

def book_ticket():
    def submit_booking():
        flight_id = int(flight_id_entry.get())
        passenger_name = passenger_name_entry.get()
        passenger_contact = passenger_contact_entry.get()
        
        query = "SELECT seats_available FROM flights WHERE flight_id = %s"
        cursor.execute(query, (flight_id,))
        result = cursor.fetchone()

        if result and result[0] > 0:
            query = """INSERT INTO bookings (flight_id, passenger_name, passenger_contact)
                       VALUES (%s, %s, %s)"""
            cursor.execute(query, (flight_id, passenger_name, passenger_contact))
            conn.commit()

            query = "UPDATE flights SET seats_available = seats_available - 1 WHERE flight_id = %s"
            cursor.execute(query, (flight_id,))
            conn.commit()

            messagebox.showinfo("Success", "Ticket booked successfully!")
            book_ticket_window.destroy()
        else:
            messagebox.showerror("Error", "No seats available for this flight!")

    book_ticket_window = tk.Toplevel(root)
    book_ticket_window.title("Book Ticket")
    book_ticket_window.configure(bg="#ADD8E6")

    tk.Label(book_ticket_window, text="Flight ID:", bg="#ADD8E6", fg="black").grid(row=0, column=0)
    flight_id_entry = tk.Entry(book_ticket_window)
    flight_id_entry.grid(row=0, column=1)

    tk.Label(book_ticket_window, text="Passenger Name:", bg="#ADD8E6", fg="black").grid(row=1, column=0)
    passenger_name_entry = tk.Entry(book_ticket_window)
    passenger_name_entry.grid(row=1, column=1)

    tk.Label(book_ticket_window, text="Passenger Contact:", bg="#ADD8E6", fg="black").grid(row=2, column=0)
    passenger_contact_entry = tk.Entry(book_ticket_window)
    passenger_contact_entry.grid(row=2, column=1)

    tk.Button(book_ticket_window, text="Submit", command=submit_booking, bg="black", fg="white", width=20, height=2, font=("Helvetica", 12)).grid(row=3, columnspan=2, pady=10)

def cancel_ticket():
    def submit_cancellation():
        booking_id = int(booking_id_entry.get())

        query = "SELECT flight_id FROM bookings WHERE booking_id = %s"
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()

        if result:
            flight_id = result[0]

            query = "DELETE FROM bookings WHERE booking_id = %s"
            cursor.execute(query, (booking_id,))
            conn.commit()

            query = "UPDATE flights SET seats_available = seats_available + 1 WHERE flight_id = %s"
            cursor.execute(query, (flight_id,))
            conn.commit()

            messagebox.showinfo("Success", "Ticket cancelled successfully!")
            cancel_ticket_window.destroy()
        else:
            messagebox.showerror("Error", "Booking ID not found!")

    cancel_ticket_window = tk.Toplevel(root)
    cancel_ticket_window.title("Cancel Ticket")
    cancel_ticket_window.configure(bg="#ADD8E6")

    tk.Label(cancel_ticket_window, text="Booking ID:", bg="#ADD8E6", fg="black").grid(row=0, column=0)
    booking_id_entry = tk.Entry(cancel_ticket_window)
    booking_id_entry.grid(row=0, column=1)

    tk.Button(cancel_ticket_window, text="Submit", command=submit_cancellation, bg="black", fg="white", width=20, height=2, font=("Helvetica", 12)).grid(row=1, columnspan=2, pady=10)

def verify_ticket():
    def submit_verification():
        booking_id = int(booking_id_entry.get())

        query = """SELECT bookings.booking_id, flights.flight_number, bookings.passenger_name, bookings.passenger_contact 
                   FROM bookings 
                   JOIN flights ON bookings.flight_id = flights.flight_id 
                   WHERE bookings.booking_id = %s"""
        cursor.execute(query, (booking_id,))
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("Ticket Info", f"Booking ID: {result[0]}, Flight Number: {result[1]}, Passenger Name: {result[2]}, Contact: {result[3]}")
            verify_ticket_window.destroy()
        else:
            messagebox.showerror("Error", "Booking ID not found!")

    verify_ticket_window = tk.Toplevel(root)
    verify_ticket_window.title("Verify Ticket")
    verify_ticket_window.configure(bg="#ADD8E6")

    tk.Label(verify_ticket_window, text="Booking ID:", bg="#ADD8E6", fg="black").grid(row=0, column=0)
    booking_id_entry = tk.Entry(verify_ticket_window)
    booking_id_entry.grid(row=0, column=1)

    tk.Button(verify_ticket_window, text="Submit", command=submit_verification, bg="black", fg="white", width=20, height=2, font=("Helvetica", 12)).grid(row=1, columnspan=2, pady=10)

def view_flights():
    flights_window = tk.Toplevel(root)
    flights_window.title("View Flights")
    flights_window.configure(bg="#ADD8E6")

    query = "SELECT * FROM flights"
    cursor.execute(query)
    result = cursor.fetchall()

    text = tk.Text(flights_window, bg="#ADD8E6", fg="black")
    for row in result:
        text.insert(tk.END, f"Flight ID: {row[0]}, Flight Number: {row[1]}, Origin: {row[2]}, Destination: {row[3]}, "
                            f"Departure Time: {row[4]}, Arrival Time: {row[5]}, Seats Available: {row[6]}\n")
    text.pack()

def book_priority_slots():
    def submit_priority():
        try:
            passenger_id = passenger_id_entry.get()
            checkin_slot = checkin_slot_entry.get()
            boarding_slot = boarding_slot_entry.get()
            
            query = """INSERT INTO priority_slots (passenger_id, checkin_slot, boarding_slot)
                       VALUES (%s, %s, %s)"""
            cursor.execute(query, (passenger_id, checkin_slot, boarding_slot))
            conn.commit()
            messagebox.showinfo("Success", "Priority slots booked successfully!")
        except:
            messagebox.showerror("Error", "Passenger ID not found!")
        book_priority_slots_window.destroy()

    book_priority_slots_window = tk.Toplevel(root)
    book_priority_slots_window.title("Book Priority Slots")
    book_priority_slots_window.configure(bg="#ADD8E6")

    tk.Label(book_priority_slots_window, text="Passenger ID:", bg="#ADD8E6", fg="black").grid(row=0, column=0)
    passenger_id_entry = tk.Entry(book_priority_slots_window)
    passenger_id_entry.grid(row=0, column=1)

    tk.Label(book_priority_slots_window, text="Check-in Slot (HH:MM:SS):", bg="#ADD8E6", fg="black").grid(row=1, column=0)
    checkin_slot_entry = tk.Entry(book_priority_slots_window)
    checkin_slot_entry.grid(row=1, column=1)

    tk.Label(book_priority_slots_window, text="Boarding Slot (HH:MM:SS):", bg="#ADD8E6", fg="black").grid(row=2, column=0)
    boarding_slot_entry = tk.Entry(book_priority_slots_window)
    boarding_slot_entry.grid(row=2, column=1)

    tk.Button(book_priority_slots_window, text="Submit", command=submit_priority, bg="black", fg="white", width=20, height=2, font=("Helvetica", 12)).grid(row=3, columnspan=2, pady=10)

def view_crowd_levels():
    crowd_levels_window = tk.Toplevel(root)
    crowd_levels_window.title("View Crowd Levels")
    crowd_levels_window.configure(bg="#ADD8E6")

    query = "SELECT area, crowd_level FROM crowd_levels"
    cursor.execute(query)
    result = cursor.fetchall()

    text = tk.Text(crowd_levels_window, bg="#ADD8E6", fg="black")
    for row in result:
        text.insert(tk.END, f"Area: {row[0]}, Crowd Level: {row[1]}\n")
    text.pack()

def schedule_luggage_dropoff():
    def submit_dropoff():
        try:
            booking_id = booking_id_entry.get()
            dropoff_time = dropoff_time_entry.get()
            
            query = """INSERT INTO luggage_dropoff (booking_id, dropoff_time)
                       VALUES (%s, %s)"""
            cursor.execute(query, (booking_id, dropoff_time))
            conn.commit()
            messagebox.showinfo("Success", "Luggage drop-off scheduled successfully!")
        except:
            messagebox.showerror("Error", "Booking ID not found!")
        schedule_luggage_dropoff_window.destroy()

    schedule_luggage_dropoff_window = tk.Toplevel(root)
    schedule_luggage_dropoff_window.title("Schedule Luggage Drop-off")
    schedule_luggage_dropoff_window.configure(bg="#ADD8E6")

    tk.Label(schedule_luggage_dropoff_window, text="Booking ID:", bg="#ADD8E6", fg="black").grid(row=0, column=0)
    booking_id_entry = tk.Entry(schedule_luggage_dropoff_window)
    booking_id_entry.grid(row=0, column=1)

    tk.Label(schedule_luggage_dropoff_window, text="Drop-off Time (YYYY-MM-DD HH:MM:SS):", bg="#ADD8E6", fg="black").grid(row=1, column=0)
    dropoff_time_entry = tk.Entry(schedule_luggage_dropoff_window)
    dropoff_time_entry.grid(row=1, column=1)

    tk.Button(schedule_luggage_dropoff_window, text="Submit", command=submit_dropoff, bg="black", fg="white", width=20, height=2, font=("Helvetica", 12)).grid(row=2, columnspan=2, pady=10)

def exit_program():
    cursor.close()
    conn.close()
    root.destroy()

# Main menu
tk.Label(root, text="AIRLINE MANAGEMENT SYSTEM", font=("Helvetica", 60, "bold"), bg="#ADD8E6", fg="black").pack(pady=20)

button_frame = tk.Frame(root, bg="#ADD8E6")
button_frame.pack(pady=20)

button_width = 25
button_height = 3
button_font = ("Helvetica", 16)

tk.Button(button_frame, text="Add Flight", command=add_flight, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=0, column=0, padx=20, pady=20)
tk.Button(button_frame, text="Book Ticket", command=book_ticket, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=0, column=1, padx=20, pady=20)
tk.Button(button_frame, text="Cancel Ticket", command=cancel_ticket, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=0, column=2, padx=20, pady=20)
tk.Button(button_frame, text="Verify Ticket", command=verify_ticket, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=0, column=3, padx=20, pady=20)
tk.Button(button_frame, text="View Flights", command=view_flights, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=1, column=0, padx=20, pady=20)
tk.Button(button_frame, text="Book Priority Slots", command=book_priority_slots, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=1, column=1, padx=20, pady=20)
tk.Button(button_frame, text="View Crowd Levels", command=view_crowd_levels, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=1, column=2, padx=20, pady=20)
tk.Button(button_frame, text="Schedule Luggage Drop-off", command=schedule_luggage_dropoff, bg="black", fg="white", width=button_width, height=button_height, font=button_font).grid(row=1, column=3, padx=20, pady=20)

tk.Button(root, text="Exit", command=exit_program, bg="black", fg="white", width=button_width, height=button_height, font=button_font).pack(pady=20)

root.mainloop()

# Close the cursor and connection when done
cursor.close()
conn.close()
