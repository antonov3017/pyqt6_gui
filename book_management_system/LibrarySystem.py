from PyQt6.QtWidgets import QMainWindow, QDialog, QMessageBox, QTableWidgetItem
from MainGUI import Ui_MainWindow
from AddBook import Add_Dialog
from AddMember import Member_Dialog
from ViewBook import View_Dialog
from ViewMember import Member_UI
import mysql.connector as mc


class LibrarySystem(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()

        self.toolButton_addbook.clicked.connect(self.add_book)
        self.toolButton_addmember.clicked.connect(self.add_member)
        self.toolButton_viewbook.clicked.connect(self.view_books)
        self.toolButton_viewmember.clicked.connect(self.view_members)

        self.lineEdit_bookid.returnPressed.connect(self.book_id)
        self.lineEdit_memberid.returnPressed.connect(self.member_id)

        self.toolButton_issue.clicked.connect(self.issue_book)

        self.lineEdit_submission.returnPressed.connect(self.load_issue)

        self.toolButton_submit.clicked.connect(self.submit_book)

        self.toolButton_renew.clicked.connect(self.renew_book)

    def add_book(self):
        dialog = QDialog()
        ui = Add_Dialog()

        ui.setupUi(dialog)
        dialog.exec()


    def add_member(self):
        dialog = QDialog()
        ui = Member_Dialog()

        ui.setupUi(dialog)
        dialog.exec()

    def view_books(self):
        dialog = QDialog()
        ui = View_Dialog()
        ui.setupUi(dialog)
        dialog.exec()

    def view_members(self):
        dialog = QDialog()
        ui = Member_UI()
        ui.setupUi(dialog)
        dialog.exec()


    def book_id(self):
        id = self.lineEdit_bookid.text()

        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )

            mycursor = mydb.cursor()
            query = "SELECT * FROM tbl_addbook WHERE id =  '"+ id +  "'"
            mycursor.execute(query)

            result = mycursor.fetchall()

            for row in result:
                self.label_bookname.setText("Book Name : " + row[0])
                self.label_bookauthor.setText("Book Author : " + row[2])

        except mc.Error as e:
            print("Error")



    def member_id(self):
        id = self.lineEdit_memberid.text()

        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )

            mycursor = mydb.cursor()
            query = "SELECT * FROM tbl_addmember WHERE id = '" + id + "' "
            mycursor.execute(query)

            result = mycursor.fetchall()

            for row in result:
                self.label_membername.setText("Member Name : " + row[1])
                self.label_contactinfo.setText("Member Email : " + row[3])


        except mc.Error as e:
            print("Error occured")



    def issue_book(self):
        b_id = self.lineEdit_bookid.text()
        m_id = self.lineEdit_memberid.text()


        try:
            mydb = mc.connect(
                host = "localhost",
                user= "root",
                password = "",
                database = "library"
            )

            mycursor = mydb.cursor()
            query = "INSERT INTO tbl_issue (bookID, memberID) VALUES (%s, %s)"
            query2 = "UPDATE tbl_addbook SET isAvail = FALSE WHERE id =  '" + b_id + "'  "
            value = (b_id, m_id)

            mycursor.execute(query, value)
            mycursor.execute(query2)
            mydb.commit()

            QMessageBox.about(self, "Issue Book", "Book Issued Successfully")

        except mc.Error as e:
            print("Error occured")

    def load_issue(self):
        issue_id = self.lineEdit_submission.text()

        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )

            mycursor = mydb.cursor()
            mycursor.execute("SELECT * FROM tbl_issue WHERE bookID =  '" + issue_id +  "'  ")
            result = mycursor.fetchall()

            self.tableWidget_bookinfo.setRowCount(0)

            for row_number, row_data in enumerate(result):
                self.tableWidget_bookinfo.insertRow(row_number)

                for column_number, data in enumerate(row_data):
                    self.tableWidget_bookinfo.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        except mc.Error as e:
            print("Error occured")


    def submit_book(self):
        issue_id = self.lineEdit_submission.text()

        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )

            if issue_id == "":
                QMessageBox.about(self, "Book Submission", "Please choose a book")
                return

            mycursor = mydb.cursor()
            query = "DELETE FROM tbl_issue WHERE bookID = '" + issue_id + "'  "
            query2 = "UPDATE tbl_addbook SET isAvail = TRUE WHERE id =  '"  + issue_id +  "' "

            mycursor.execute(query)
            mycursor.execute(query2)
            mydb.commit()
            QMessageBox.about(self, "Book Submission", "Book Submitted Successfully")


        except mc.Error as e:
            print("Error occured")

    def renew_book(self):
        issue_id = self.lineEdit_submission.text()


        try:
            mydb = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="library"
            )

            if issue_id == "":
                QMessageBox.about(self, "Renew Book", "Please choose a book")
                return

            mycursor = mydb.cursor()
            query = "UPDATE tbl_issue SET issueTime = CURRENT_TIMESTAMP, renewCount=renewCount+1 WHERE bookID  = '" + issue_id + "'  "
            mycursor.execute(query)
            mydb.commit()
            QMessageBox.about(self, "Book Renew", "Book Renewed Successfully")


        except mc.Error as e:
            print("Error occured", e)
