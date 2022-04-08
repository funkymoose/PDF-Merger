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
            
class button(QPushButton):
    def __init__(self, label_text):
        super().__init__()
        self.setText(label_text)
        self.setStyleSheet('''
            font-size:15px;
            width: 90px;
            height: 35;''')

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
        
    
    # Main ui/Layout of the window
    def ui(self):
        mainLayout = QVBoxLayout()
        outputFolderRow = QHBoxLayout()
        buttonLayout = QHBoxLayout()

        self.outputFile = output_field()
        outputFolderRow.addWidget(self.outputFile)

        # Save button
        self.saveButton = button('&Save to')
        self.saveButton.clicked.connect(self.populateFileName)
        outputFolderRow.addWidget(self.saveButton)

        #listbox widget
        self.listBoxWidget = ListWidget(self)

        # This will delete the selected files
        self.deleteButton = button("&Delete")
        self.deleteButton.clicked.connect(self.delete)
        # buttonLayout.addWidget(self.deleteButton)
        buttonLayout.addWidget(self.deleteButton, 1, Qt.AlignRight)

        # Used for merging of files
        self.mergeButton = button("&Merge")
        self.mergeButton.clicked.connect(self.mergeFile)
        buttonLayout.addWidget(self.mergeButton)

        # To reset the window
        self.resetButton = button("&Reset")
        self.resetButton.clicked.connect(self.reset)
        buttonLayout.addWidget(self.resetButton)

        # To close the window
        self.closeButton = button("&Close")
        self.closeButton.clicked.connect(QApplication.quit)
        buttonLayout.addWidget(self.closeButton)


        mainLayout.addLayout(outputFolderRow)
        mainLayout.addWidget(self.listBoxWidget)
        mainLayout.addLayout(buttonLayout)

        self.setLayout(mainLayout)
        
    #     Deleting the items
    def delete(self):
        for item in self.listBoxWidget.selectedItems():
            self.listBoxWidget.takeItem(self.listBoxWidget.row(item))

#     Reset Button for clearing the screen
    def reset(self):
        self.listBoxWidget.clear()
        self.outputFile.setText('')

#     popup message
    def messageDialogueBox(self, message):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("PDF Manager")
        dlg.setIcon(QMessageBox.Information)
        dlg.setText(message)
        dlg.show()

#     file dialogue window for saving the file
    def _saveFilePath(self):
        saving_path, _ = QFileDialog.getSaveFileName(self, "Save PDF file", os.getcwd(), 'PDF File(*.pdf)')
        return saving_path

    def populateFileName(self):
        path = self._saveFilePath()
        if path:
            self.outputFile.setText(path)

#   Merging the pdf files along with raising exceptions
    def mergeFile(self):

        if not self.outputFile.text():
            self.populateFileName()
            return

        if self.listBoxWidget.count()>0:
            pdfMerger = PdfFileMerger()

            try:
                for i in range(self.listBoxWidget.count()):
                    pdfMerger.append(self.listBoxWidget.item(i).text())

                pdfMerger.write(self.outputFile.text())
                pdfMerger.close()

                self.listBoxWidget.clear()
                self.messageDialogueBox("PDF Merge Complete.\nThankyou for using Application.")

            except Exception as e:
                self.messageDialogueBox(e)
        else:
            self.messageDialogueBox("No files found")
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)


pdf_app = PDFApp()
pdf_app.show()

sys.exit(app.exec_())
