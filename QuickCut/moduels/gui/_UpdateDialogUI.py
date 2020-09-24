# -*- coding: UTF-8 -*-


from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from moduels.component.NormalValue import 常量


class _UpdateDialogUI:
    def setup_ui(self, UpdateDialog):
        UpdateDialog.setObjectName('UpdateDialog')
        UpdateDialog.resize(350, 500)
        UpdateDialog.setWindowFlags(
            Qt.WindowTitleHint | Qt.WindowCloseButtonHint | Qt.Dialog)
        if 常量.platfm == 'Darwin':
            UpdateDialog.setWindowIcon(QIcon('misc/icon.icns'))
        else:
            UpdateDialog.setWindowIcon(QIcon('misc/icon.ico'))
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(UpdateDialog.sizePolicy()
                                      .hasHeightForWidth())
        UpdateDialog.setSizePolicy(size_policy)
        UpdateDialog.setAutoFillBackground(False)
        UpdateDialog.setSizeGripEnabled(False)
        self.horizontal_layout = QHBoxLayout(UpdateDialog)
        self.horizontal_layout.setContentsMargins(10, 10, 10, 10)
        self.horizontal_layout.setObjectName('horizontal_layout')
        self.grid_layout = QGridLayout()
        self.grid_layout.setObjectName('grid_layout')
        self.gitee_button = QPushButton(UpdateDialog)
        self.gitee_button.setEnabled(False)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.gitee_button.sizePolicy()
                                      .hasHeightForWidth())
        self.gitee_button.setSizePolicy(size_policy)
        self.gitee_button.setMaximumSize(QSize(16777215, 30))
        self.gitee_button.setAutoDefault(False)
        self.gitee_button.setObjectName('gitee_button')
        self.grid_layout.addWidget(self.gitee_button, 1, 1, 1, 1)
        self.close_button = QPushButton(UpdateDialog)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.close_button.sizePolicy()
                                      .hasHeightForWidth())
        self.close_button.setSizePolicy(size_policy)
        self.close_button.setMaximumSize(QSize(16777215, 30))
        self.close_button.setAutoDefault(False)
        self.close_button.setDefault(False)
        self.close_button.setObjectName('close_button')
        self.grid_layout.addWidget(self.close_button, 1, 2, 1, 1)
        self.github_button = QPushButton(UpdateDialog)
        self.github_button.setEnabled(False)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.github_button.sizePolicy()
                                      .hasHeightForWidth())
        self.github_button.setSizePolicy(size_policy)
        self.github_button.setMaximumSize(QSize(16777215, 30))
        self.github_button.setAutoDefault(False)
        self.github_button.setObjectName('github_button')
        self.grid_layout.addWidget(self.github_button, 1, 0, 1, 1)
        self.update_info_text = QTextEdit(UpdateDialog)
        self.update_info_text.setEnabled(True)
        self.update_info_text.setDocumentTitle('')
        self.update_info_text.setUndoRedoEnabled(False)
        self.update_info_text.setReadOnly(True)
        self.update_info_text.setObjectName('update_info_text')
        self.grid_layout.addWidget(self.update_info_text, 0, 0, 1, 3)
        self.horizontal_layout.addLayout(self.grid_layout)

        self.retranslate_ui(UpdateDialog)
        QMetaObject.connectSlotsByName(UpdateDialog)

    def retranslate_ui(self, UpdateDialog):
        _translate = QCoreApplication.translate
        UpdateDialog.setWindowTitle(_translate('UpdateDialog', '发现更新'))
        self.gitee_button.setText(_translate('UpdateDialog', '前往Gitee下载'))
        self.close_button.setText(_translate('UpdateDialog', '关闭'))
        self.github_button.setText(
            _translate('UpdateDialog', '前往Github下载'))
        self.update_info_text.setPlaceholderText(
            _translate('UpdateDialog', '获取更新信息失败'))
