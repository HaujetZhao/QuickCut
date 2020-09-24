
class ConsoleTab(QTableWidget):
    def __init__(self):
        super().__init__()
        self.initGui()

    def initGui(self):
        self.layout = QVBoxLayout()
        self.consoleEditBox = QTextEdit(self, readOnly=True)
        self.layout.addWidget(self.consoleEditBox)
        self.setLayout(self.layout)
