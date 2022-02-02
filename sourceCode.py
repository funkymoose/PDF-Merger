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

# Class for the drag and drop accessibility
class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent=None)
        self.setAcceptDrops(True)
        self.setStyleSheet('''font-size: 25px''')
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            return super().dragEnterEvent(event)  #return to original event state

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction) #return to original event state
            event.accept()
        else:
            return super().dragMoveEvent(event)

    def dropEvent(self,event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            pdffiles = []
            for url in event.mimeData().urls():
                if url.isLocalFile():
                   if url.toString().endswith('.pdf'):
                       pdffiles.append(str(url.toLocalFile()))
            self.addItems(pdffiles)
        else:
            return super().dropEvent(event)
        
# ignoring the files which are not in pdf format
class output_field(QLineEdit):
    def __init__(self):
        super().__init__()
        self.height = 55
        self.setStyleSheet('font-size: 30px')
        self.setFixedHeight(self.height)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()

            if event.mimeData().urls():
                self.setText((event.mimeData().urls()[0].toLocalFile()))
        else:
            event.ignore()

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
