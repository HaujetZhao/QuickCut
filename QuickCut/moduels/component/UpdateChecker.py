
class UpdateChecker:
    def __init__(self):
        self._github_thread, self._gitee_thread = QThread(), QThread()
        self._github_worker = _UpdateCheckerWorker('github')
        self._github_worker.moveToThread(self._github_thread)
        self._github_thread.started.connect(self._github_worker.run)
        self._gitee_worker = _UpdateCheckerWorker('gitee')
        self._gitee_worker.moveToThread(self._gitee_thread)
        self._gitee_thread.started.connect(self._gitee_worker.run)

        self._update_dialog = UpdateDialog()
        self._github_worker.signal.connect(self._update_dialog.set_result)
        self._gitee_worker.signal.connect(self._update_dialog.set_result)

    def check_for_update(self):
        self._github_thread.start()
        self._gitee_thread.start()

    @property
    def update_dialog(self):
        return self._update_dialog
