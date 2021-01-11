import sqlite3
import sys

from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox, QInputDialog


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('katalog.ui', self)
        con = sqlite3.connect('books.sqlite')
        self.cursor = con.cursor()
        self.listWidget.itemClicked.connect(self.openBook)
        self.pushButton.clicked.connect(self.check)

    def check(self):
        self.listWidget.clear()
        if self.comboBox.currentText() == 'Автор':
            text = 'author'
        else:
            text = 'name'
        result = self.cursor.execute(f"SELECT name FROM books WHERE {text} LIKE '{self.lineEdit.text()}%'").fetchall()
        for i in result:
            self.listWidget.addItem(i[0])

    def openBook(self, item):
        zn = self.cursor.execute(f"SELECT * FROM books WHERE name = '{item.text()}'").fetchone()
        global book
        book = Book(author=zn[1], name=zn[2], year=zn[3], genre=zn[4], image=zn[5])
        book.show()


class Book(QMainWindow):
    def __init__(self, author, name, year, genre, image):
        super().__init__()
        uic.loadUi("book.ui", self)

        self.label.setPixmap(QPixmap(image))
        self.label_6.setText(name)
        self.label_7.setText(author)
        self.label_8.setText(str(year))
        self.label_9.setText(genre)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
