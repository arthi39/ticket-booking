import mysql.connector
import pandas as pd
import smtplib
import random
import csv
import datetime

class Election:
    def __init__(self):
        self.candidates = {1: "Yazhini", 2: "Pooja", 3: "Nisha", 4: "Dhivya"}
        self.vote_count = {i: 0 for i in self.candidates.keys()}
        self.conn = mysql.connector.connect(
            host='localhost',
            database='Election',
            user='root',
            password='12345'
        )
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS votes (email VARCHAR(255), candidate INT)")
        self.conn.commit()
 
    def email(self):
        try:
            enter_email = input("Enter your Email id: ")
            otp = random.randint(00000, 99999)
            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login("arthipalanisamy39@gmail.com", "mnec sphi uxpy gecp")
            msg = f"Your OTP is {otp}"
            s.sendmail("your-email@gmail.com", enter_email, msg)
            s.quit()
            otp_input = int(input("Enter your OTP: "))
            if otp == otp_input:
                return enter_email
            else:
                print("Invalid OTP")
                return False
        except smtplib.SMTPException as e:
            print(f"Error sending email: {e}")
            return False

    def voting(self, email):
        while True:
            x = datetime.datetime.now()
            print("\nElection Menu:")
            print("------------")
            print("1. Yazhini ")
            print("2. Pooja")
            print("3. Nisha")
            print("4. Dhivya")
            print("0. Exit")
            vote = int(input("Enter your vote: "))
            if vote == 0:
                self.result()
                print("Exiting the election system. Goodbye!")
                break
            elif vote in self.candidates.keys():
                print(f"Thank you for your voteing! at {x}")
                self.vote_count[vote] += 1
                self.cursor.execute("INSERT INTO votes (email, candidates) VALUES (%s, %s)", (email, vote))
                self.conn.commit()
                print("Vote recorded successfully!")
                self.email()
            else:
                print("Ohh! There no candidate in that number")

    def result(self):
        with open('vote.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["candidate", "votes"])
            for i, j in self.vote_count.items():
                writer.writerow([self.candidates[i], j])
        for i, j in self.vote_count.items():
            print(f"{self.candidates[i]}: {j}")
        max_votes = max(self.vote_count.values())
        winners = [i for i, j in self.vote_count.items() if j == max_votes]
        if len(winners) == 1:
            print(f"The winner is {self.candidates[winners[0]]}")
        else:
            print("It's a tie between:")
            for winner in winners:
                print(self.candidates[winner])

election = Election()
email = election.email()
if email:
    election.voting(email)