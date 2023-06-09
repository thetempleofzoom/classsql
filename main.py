import requests
import selectorlib
import smtplib, ssl, os
import time
import sqlite3

url = 'http://programmer100.pythonanywhere.com/tours/'

class Tours:
    def scrape(self, url):
        #scrape data from website
        response = requests.get(url)
        source = response.text
        return source

    def extract(self, source):
        extractor = selectorlib.Extractor.from_yaml_file("data.yaml")
        tour = extractor.extract(source)['tourname']
        return tour


class Database:
    def __init__(self, dbpath):
        self.connection = sqlite3.connect(dbpath)
        self.cursor = self.connection.cursor()

    def store(self, newrow, message):
        #check for dups and write if no dups
        self.cursor.execute("INSERT INTO events VALUES(?,?,?)", newrow)
        self.connection.commit()

        email.send(message)

    def check(self, newrow):
        band, city, date = newrow
        print(band, city, date)
        self.cursor.execute("SELECT * FROM events WHERE band=? AND city=? AND date=?", (band, city, date))
        row = self.cursor.fetchall()
        return row

class Email:
    def send(self, message):
        host = 'smtp.gmail.com'
        port = 465
        username = 'shadowysupercoderssc@gmail.com'
        password = os.environ.get('SSCPW')
        receiver = 'shadowysupercoderssc@gmail.com'
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(host=host, port=port, context=context) as server:
            server.login(username, password)
            server.sendmail(username, receiver, message)
            print('mail sent')


if __name__ =="__main__":
    while True:
        tours = Tours()
        email = Email()
        scraped = tours.scrape(url)
        extracted = tours.extract(scraped)

        message = 'Subject: {}\n\n{}'.format('new event found', extracted)
        # code entire message in utf for it to work, not just message body
        message = message.encode('utf-8')

        if extracted != "No upcoming tours":
            database = Database(dbpath="data.db")
            newrow = extracted.split(",")
            newrow = [n.strip() for n in newrow]
            print(newrow)
            row = database.check(newrow)
            if not row:
                database.store(newrow, message)

        time.sleep(2)


