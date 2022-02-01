import sys, io, os

if hasattr(sys, 'frozen'):
    os.environ['Path'] = sys._MEIPASS+';'+os.environ['Path']

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QDialog, QFileDialog, QMessageBox,QAbstractItemView

from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon
from PyPDF2 import PdfFileMerger

# This function will resolve the issue if the files cannot be located and path issues
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Application window
class PDFApp(QWidget):
#    We'll use QWidget as parent class and inherit the methods
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Merger by Somesh P.")
        self.setWindowIcon(QIcon(resource_path("download.ico")))
        self.resize(1200, 500)
        self.ui()
        # self.saveButton.clicked.connect(self.populateFileName)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)


pdf_app = PDFApp()
pdf_app.show()

sys.exit(app.exec_())
