import smtplib
import mysql.connector
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class arthicinimas:
    def __init__(self):
        self.movies = ['3', 'star', 'indian 2']
        self.classes = {"first class": 250, "second class": 150}
        self.gst_rate = 0.18  #Assuming 18% GST
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="arthi_theater"
        )
        self.cursor = self.db.cursor()

    def create_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS arthi_theater")

        self.db.commit()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS movie (
                id INT AUTO_INCREMENT PRIMARY KEY,
                movies_name VARCHAR(255),
                email VARCHAR(255),
                total DECIMAL(10, 2)
            )
        """)
        self.db.commit()

    def display_movies(self):
        print("ARTHI CINIMAS")
        print("Available movies:")
        for movie in self.movies:
            print(movie)

    def get_movie_details(self):
        enter_movie = input("Enter movie name: ")
        if enter_movie in self.movies:
            print("Movie is available")
            return enter_movie
        else:
            print("Movie is not available")
            return None

    def get_class_details(self):
        Enter_class = input("Enter your class: ")
        if Enter_class in self.classes:
            print("your ticket price is", self.classes[Enter_class])
            return Enter_class
        else:
            print("class is not available")
            return None

    def calculate_total(self, Enter_class, how_many):
        base_total = self.classes[Enter_class] * int(how_many)
        gst_amount = base_total * self.gst_rate
        total = base_total + gst_amount
        print(f"Your total price including GST is {total:.2f}")
        return total, gst_amount

    def make_payment(self, cm, pay):
        if cm == "on hand" and pay == "paid":
            print("Your ticket is successfully booked")
            return True
        elif cm == "online" and pay == "paid":
            print("Your ticket is successfully booked")
            return True
        else:
            print("Sorry!!! Your ticket is not booked")
            return False

    def send_email(self, bill, total, gst_amount,):
        try:
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("arthipalanisamy39@gmail.com", "mnec sphi uxpy gecp")
            msg = MIMEMultipart()
            msg['From'] = "arthipalanisamy39@gmail.com"
            msg['To'] = bill
            msg['Subject'] = "Your Ticket Booking Confirmation"
        
            body = (
            
                f"Base Price: {total - gst_amount:.2f}\n\n"
                f"GST Amount: {gst_amount:.2f}\n"
                f"Total Price: {total:.2f}\n\n"
                f"Thank you for booking with us!"
            )
            msg.attach(MIMEText(body, 'plain'))
            
            s.sendmail(msg['From'], msg['To'], msg.as_string())
            s.quit()

            print("Email sent successfully!")
        except smtplib.SMTPException as e:
            print("Error sending email:", e)
        except Exception as e:
            print("An error occurred:", e)

    def book_tickets(self):
        self.display_movies()
        enter_movie = self.get_movie_details()
        if enter_movie:
            Enter_class = self.get_class_details()
            if Enter_class:
                how_many = int(input("Number of tickets: "))
                total, gst_amount = self.calculate_total(Enter_class, how_many)
                cm = input("Is cash pay in online or on hand: ")
                pay = input("paid/unpaid? ")
                if self.make_payment(cm, pay):
                    bill = input("Enter your Email for bill: ")
                    self.send_email(bill, total, gst_amount,)
                    self.cursor.execute("""INSERT INTO movie ( movies_name , email, total) VALUES (%s, %s, %s)""", (enter_movie , bill, total))
                    self.db.commit()
                    print("Ticket booking successfully!")

if __name__ == "__main__":
    arthi_cinimas = arthicinimas()
    arthi_cinimas.create_database()   
    arthi_cinimas.create_table()
    while True:
        command = input("Type 'book' to book a ticket or 'exit' to exit: ")
        if command.lower() == 'exit':
            break
        elif command.lower() == 'book':
            arthi_cinimas.book_tickets()
        else:
            print("Invalid command. Please try again.")
 