import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import QThread, pyqtSignal
from yt_dlp import YoutubeDL

class DownloadThread(QThread):
    download_finished = pyqtSignal(str)
    download_progress = pyqtSignal(str)

    def __init__(self, url, output_path):
        super().__init__()
        self.url = url
        self.output_path = output_path

    def run(self):
        try:
            ydl_opts = {
                'outtmpl': f'{self.output_path}/%(title)s.%(ext)s',
                'format': 'best',
                'progress_hooks': [self.hook],
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
            self.download_finished.emit(f"'{self.url}' 동영상 다운로드가 완료되었습니다.")
        except Exception as e:
            self.download_finished.emit(f"다운로드 중 오류 발생: {e}")

    def hook(self, d):
        if d['status'] == 'downloading':
            p = d['_percent_str']
            self.download_progress.emit(f"다운로드 중: {p}")
        elif d['status'] == 'finished':
            self.download_progress.emit("다운로드 완료.")

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('YouTube Downloader')
        self.setGeometry(100, 100, 600, 150)

        main_layout = QVBoxLayout()

        # URL 입력
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText('유튜브 동영상 URL을 입력하세요')
        url_layout.addWidget(QLabel('URL:'))
        url_layout.addWidget(self.url_input)
        main_layout.addLayout(url_layout)

        # 저장 경로 선택
        path_layout = QHBoxLayout()
        self.path_label = QLabel('저장 경로: 현재 디렉토리')
        self.output_path = '.'
        path_button = QPushButton('경로 선택', self)
        path_button.clicked.connect(self.select_output_path)
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(path_button)
        main_layout.addLayout(path_layout)

        # 다운로드 버튼
        self.download_button = QPushButton('다운로드', self)
        self.download_button.clicked.connect(self.start_download)
        main_layout.addWidget(self.download_button)

        # 상태 메시지
        self.status_label = QLabel('준비됨', self)
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

    def select_output_path(self):
        folder_path = QFileDialog.getExistingDirectory(self, "저장할 폴더 선택")
        if folder_path:
            self.output_path = folder_path
            self.path_label.setText(f'저장 경로: {self.output_path}')

    def start_download(self):
        url = self.url_input.text()
        if not url:
            self.status_label.setText('URL을 입력해주세요.')
            return

        self.status_label.setText('다운로드 시작...')
        self.download_button.setEnabled(False)

        self.download_thread = DownloadThread(url, self.output_path)
        self.download_thread.download_finished.connect(self.download_finished)
        self.download_thread.download_progress.connect(self.update_progress)
        self.download_thread.start()

    def download_finished(self, message):
        self.status_label.setText(message)
        self.download_button.setEnabled(True)

    def update_progress(self, message):
        self.status_label.setText(message)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloaderApp()
    ex.show()
    sys.exit(app.exec_())