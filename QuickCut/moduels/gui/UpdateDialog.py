
class UpdateDialog(QDialog, _UpdateDialogUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui(self)
        self.close_button.clicked.connect(self.close)
        self.github_set = False
        self.gitee_set = False
        self.update_avail = False

    @pyqtSlot(tuple)
    def set_result(self, result):
        site, avail, info, url = result
        assert site in ('github', 'gitee')

        # Prepare buttons
        if site == 'github':
            if url is not None:
                self.github_button.clicked.connect(
                    lambda: webbrowser.open(url))
            self.github_button.setEnabled(avail)
            self.github_set = True
        else:
            if url is not None:
                self.gitee_button.clicked.connect(
                    lambda: webbrowser.open(url))
            self.gitee_button.setEnabled(avail)
            self.gitee_set = True
        # Prepare release info
        if avail:
            self.update_avail = True
        if self.update_info_text.toMarkdown() == '' and info is not None:
            self.update_info_text.setMarkdown(info)

        # Show dialog when it has both results of Github and Gitee, and
        # update is available
        if self.github_set and self.gitee_set and self.update_avail:
            self.show()
