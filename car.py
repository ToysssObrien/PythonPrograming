import sys
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6 import uic
import mysql.connector as con
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl
from mysqlconnector import db, cur
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('booking.ui', self)

        self.db_connection = db
        self.cursor = cur
        # Populate car type combo box
        self.populate_car_types()

        # Populate location combo boxes
        self.populate_locations(self.cbFrom)
        self.populate_locations(self.cbTo)

        # Set current date and time in the dateTimeEdit widget
        current_datetime = QDateTime.currentDateTime()
        self.dateTimeEdit.setDateTime(current_datetime)

        # Connect the button click event to the handling method
        self.btnBook.clicked.connect(self.book_button_clicked)

        # Connect the PDF generation to a button (modify as needed)
        self.btnPrint.clicked.connect(self.generate_pdf)

    def populate_car_types(self):
        # Replace the following list with actual car types from your database
        car_types = ['Gold Class', 'First Class']
        self.cbCarType.addItems(car_types)

    def populate_locations(self, combo_box):
        # Replace the following list with actual locations from your database
        locations = ['Sisaket', 'Ubonratchatani', 'Buriram', 'Bangkok']
        combo_box.addItems(locations)

    def book_button_clicked(self):
        # Get user input from GUI elements
        name = self.txtName.text()
        seat_no = self.txtSeatNo.text()
        car_type = self.cbCarType.currentText()
        from_location = self.cbFrom.currentText()
        to_location = self.cbTo.currentText()
        time = self.dateTimeEdit.dateTime().toString(Qt.DateFormat.ISODate)
        phone = self.txtPhone.text()

        # Insert data into the database
        query = "INSERT INTO booking (name, seatNo, cartype, fromLC, toLC, b_time, phone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (name, seat_no, car_type, from_location, to_location, time, phone)

        self.cursor.execute(query, values)
        self.db_connection.commit()

        # Display confirmation message
        self.show_message("Booking request submitted!")

    def generate_pdf(self):
        # Get user input from GUI elements
        name = self.txtName.text()
        seat_no = self.txtSeatNo.text()
        car_type = self.cbCarType.currentText()
        from_location = self.cbFrom.currentText()
        to_location = self.cbTo.currentText()
        time = self.dateTimeEdit.dateTime().toString(Qt.DateFormat.ISODate)
        phone = self.txtPhone.text()

        # Create a PDF file with a slip layout
        pdf_filename = 'booking_slip.pdf'
        pdf = canvas.Canvas(pdf_filename, pagesize=letter)

        # Set up the content of the PDF slip
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(100, 800, "Booking Confirmation Slip")
        pdf.line(100, 795, 500, 795)

        form_fields = [
            ("Name:", name),
            ("Seat Number:", seat_no),
            ("Car Type:", car_type),
            ("From Location:", from_location),
            ("To Location:", to_location),
            ("Booking Time:", time),
            ("Phone:", phone),
        ]

        y_position = 750
        for label, value in form_fields:
            pdf.setFont("Helvetica", 12)
            pdf.drawString(100, y_position, label)
            pdf.drawString(200, y_position, value)
            y_position -= 20

        # Save the PDF file
        pdf.save()

        # Display confirmation message
        self.show_message(f"Booking request submitted!\nPDF saved to {pdf_filename}")

        QDesktopServices.openUrl(QUrl.fromLocalFile(pdf_filename))

    def show_message(self, message):
        # Implement message display logic based on your GUI (e.g., popup dialog)
        QMessageBox.information(self, "Information", message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
