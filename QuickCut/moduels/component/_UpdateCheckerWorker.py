
class _UpdateCheckerWorker(QObject):
    _github_api = \
        'https://api.github.com/repos/HaujetZhao/QuickCut/releases/latest'
    _gitee_api = \
        'https://gitee.com/api/v5/repos/haujet/QuickCut/releases/latest'
    _gitee_release = 'https://gitee.com/haujet/QuickCut/releases'
    signal = pyqtSignal(tuple)

    def __init__(self, site, parent=None):
        super().__init__(parent)
        assert site in ('github', 'gitee')
        self._site = site

    @pyqtSlot()
    def run(self):
        try:
            result = self._make_request()
        except requests.RequestException:
            result = (self._site, False, None, None)
        self.signal.emit(result)

    @_request_retry()
    def _make_request(self):
        if self._site == 'github':
            api_url = self._github_api
        else:
            api_url = self._gitee_api
        r = requests.get(api_url, timeout=5)
        if r.status_code != 200:
            raise requests.HTTPError('status code is not 200')
        r_json = r.json()

        latest_version = r_json['tag_name']
        if latest_version.casefold() != version.casefold():
            update_avail = True
        else:
            update_avail = False

        if update_avail:
            update_info = r_json['body']
            if self._site == 'github':
                release_url = r_json['html_url']
            else:
                release_url = f'{self._gitee_release}/{latest_version}'
        else:
            update_info = None
            release_url = None
        return self._site, update_avail, update_info, release_url
