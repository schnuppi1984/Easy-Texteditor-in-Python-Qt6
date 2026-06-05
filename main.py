"""
Projekt: Einfacher QT6 Text Editor
Autor: Andreas P.
Datum: Juni 2026
Version: 2.0.0
Beschreibung: Portierung von PyQt5 auf PyQt6 mit dynamischen Pfaden für Icons
"""

from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QPushButton, QMenuBar, QTextEdit,
    QHBoxLayout, QWidget, QFontDialog, QColorDialog, QFileDialog,
    QDialog, QVBoxLayout, QMessageBox
)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
from PyQt6.QtCore import QFileInfo
import sys
import os

def resource_path(relative_path):
    """ 
    Sorgt dafür, dass Pfade in PyCharm UND in der späteren .exe immer stimmen.
    Sucht im Hauptverzeichnis oder im Unterordner 'assets'.
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    
    # Pfad im aktuellen Entwicklungsordner prüfen
    lokaler_pfad = os.path.join(os.path.abspath("."), relative_path)
    if os.path.exists(lokaler_pfad):
        return lokaler_pfad
        
    # Falls die Icons in einem 'assets'-Unterordner liegen:
    assets_pfad = os.path.join(os.path.abspath("."), "assets", relative_path)
    if os.path.exists(assets_pfad):
        return assets_pfad
        
    # Falls sie in 'images' liegen:
    images_pfad = os.path.join(os.path.abspath("."), "images", relative_path)
    if os.path.exists(images_pfad):
        return images_pfad
        
    return lokaler_pfad


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Einfacher Text Editor mit PDF Funktion'
        self.top = 400
        self.left = 600
        self.width = 400
        self.height = 300
        self.iconName = 'win.png'

        self.setWindowIcon(QIcon(resource_path(self.iconName)))
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createEditor()
        self.CreateMenu()

        self.show()

    # ---------------- Menü ---------------- #
    def CreateMenu(self):

        mainMenu = self.menuBar()

        fileMenu = mainMenu.addMenu("Datei")
        editMenu = mainMenu.addMenu("Bearbeiten")
        infoMenu = mainMenu.addMenu("Info")

        helpAction = QAction(QIcon(""), 'Help', self)
        helpAction.triggered.connect(self.helpAction)
        infoMenu.addAction(helpAction)

        openAction = QAction(QIcon(resource_path("open.png")), 'Öffnen', self)
        openAction.triggered.connect(self.openAction)
        fileMenu.addAction(openAction)

        saveAction = QAction(QIcon(resource_path("save.png")), 'Speichern unter', self)
        saveAction.triggered.connect(self.saveAction)
        fileMenu.addAction(saveAction)

        printAction = QAction(QIcon(resource_path("print.png")), 'Drucken', self)
        printAction.triggered.connect(self.printDialog)
        fileMenu.addAction(printAction)

        previewAction = QAction(QIcon(resource_path("preprint.png")), 'Druckvorschau', self)
        previewAction.triggered.connect(self.printPreviewDialog)
        fileMenu.addAction(previewAction)

        pdfAction = QAction(QIcon(resource_path("pdf.png")), 'PDF Exportieren', self)
        pdfAction.triggered.connect(self.pdfExport)
        fileMenu.addAction(pdfAction)

        exitAction = QAction(QIcon(resource_path("exit.png")), 'Beenden', self)
        exitAction.triggered.connect(self.exitWindow)
        fileMenu.addAction(exitAction)

        fontAction = QAction(QIcon(resource_path("edit.png")), 'Schrift', self)
        fontAction.triggered.connect(self.fontDialog)
        editMenu.addAction(fontAction)

        colorAction = QAction(QIcon(resource_path("color.png")), 'Schrift Farbe', self)
        colorAction.triggered.connect(self.colorDialog)
        editMenu.addAction(colorAction)

    # ---------------- Funktionen ---------------- #

    def exitWindow(self):
        self.close()

    def createEditor(self):
        self.textEdit = QTextEdit(self)
        self.setCentralWidget(self.textEdit)

    def fontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            self.textEdit.setFont(font)

    def colorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.textEdit.setTextColor(color)

    def printDialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.textEdit.print(printer)

    def printPreviewDialog(self):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        preview = QPrintPreviewDialog(printer, self)
        preview.paintRequested.connect(self.printPreview)
        preview.exec()

    def printPreview(self, printer):
        self.textEdit.print(printer)

    def pdfExport(self):
        fn, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "", "PDF files (*.pdf);;All Files (*)"
        )

        if fn:
            if QFileInfo(fn).suffix() == "":
                fn += ".pdf"

            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setOutputFormat(QPrinter.OutputFormat.PdfFormat)
            printer.setOutputFileName(fn)
            self.textEdit.document().print(printer)

    def openAction(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', '', "Text Files (*.txt);;All Files (*)")

        if fname:
            with open(fname, 'r', encoding="utf-8") as f:
                self.textEdit.setText(f.read())

    def saveAction(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, 'Datei Speichern', ".txt", "Alle Dateien (*);;Text Datei (*.txt)"
        )

        if filename:
            with open(filename, "w", encoding="utf-8") as file:
                file.write(self.textEdit.toPlainText())

    def helpAction(self):
        QMessageBox.about(self, "Entwickelt mit QT6", "Alpha 2.0")


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())