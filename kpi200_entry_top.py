import sys
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QFileDialog,
)
from openpyxl import Workbook

BASE_URL = 'https://finance.naver.com'
ENTRY_URL = BASE_URL + '/sise/entryJongmok.naver'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36'
}

COLUMN_HEADERS = ['종목명', '현재가', '전일비', '등락률', '거래량', '거래대금(천)', '시가총액(억)']


def fetch_entry_page(page: int = 1) -> str:
    params = {
        'type': 'KPI200',
        'page': str(page),
    }
    response = requests.get(ENTRY_URL, headers=HEADERS, params=params, timeout=10)
    response.encoding = 'euc-kr'
    response.raise_for_status()
    return response.text


def parse_entry_list(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', class_='type_1')
    if table is None:
        return []

    rows = table.find_all('tr')
    items = []
    for row in rows:
        cols = [td.get_text(strip=True) for td in row.find_all('td')]
        if len(cols) != len(COLUMN_HEADERS):
            continue

        item = dict(zip(COLUMN_HEADERS, cols))
        items.append(item)

    return items


def parse_total_pages(html: str) -> int:
    soup = BeautifulSoup(html, 'html.parser')
    nav_table = soup.find('table', class_='Nnavi')
    if nav_table is None:
        return 1

    page_numbers = []
    for link in nav_table.find_all('a'):
        text = link.get_text(strip=True)
        if text.isdigit():
            page_numbers.append(int(text))

    return max(page_numbers) if page_numbers else 1


def fetch_all_entries() -> tuple[list[dict[str, str]], int]:
    first_html = fetch_entry_page(1)
    entries = parse_entry_list(first_html)
    total_pages = parse_total_pages(first_html)

    for page in range(2, total_pages + 1):
        html = fetch_entry_page(page)
        entries.extend(parse_entry_list(html))

    return entries, total_pages


class EntryTableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('KPI200 편입종목상위')
        self.resize(950, 650)

        self.entries = []
        self.total_pages = 0

        self.status_label = QLabel('데이터를 로딩 중입니다...', self)
        self.refresh_button = QPushButton('새로고침', self)
        self.refresh_button.clicked.connect(self.load_data)
        self.save_button = QPushButton('엑셀 저장', self)
        self.save_button.clicked.connect(self.save_to_excel)
        self.save_button.setEnabled(False)

        self.table_widget = QTableWidget(self)
        self.table_widget.setColumnCount(len(COLUMN_HEADERS))
        self.table_widget.setHorizontalHeaderLabels(COLUMN_HEADERS)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setEditTriggers(QTableWidget.NoEditTriggers)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.save_button)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addLayout(button_layout)
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.load_data()

    def load_data(self) -> None:
        try:
            entries, total_pages = fetch_all_entries()
        except Exception as exc:
            message = f'데이터를 가져오는 중 오류가 발생했습니다:\n{exc}'
            QMessageBox.critical(self, '오류', message)
            self.status_label.setText('데이터 로딩 실패')
            return

        self.entries = entries
        self.total_pages = total_pages
        self.save_button.setEnabled(bool(self.entries))

        self.table_widget.setRowCount(len(entries))
        for row, entry in enumerate(entries):
            for col, header in enumerate(COLUMN_HEADERS):
                item = QTableWidgetItem(entry.get(header, ''))
                self.table_widget.setItem(row, col, item)

        self.status_label.setText(f'총 {total_pages} 페이지, {len(entries)}개 항목 로드 완료')

    def save_to_excel(self) -> None:
        if not self.entries:
            QMessageBox.warning(self, '저장 불가', '저장할 데이터가 없습니다.')
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            '엑셀 파일로 저장',
            'kpi200_entry_top.xlsx',
            'Excel Files (*.xlsx)',
        )
        if not filename:
            return

        try:
            workbook = Workbook()
            worksheet = workbook.active
            worksheet.title = 'KPI200 편입종목상위'
            worksheet.append(COLUMN_HEADERS)
            for entry in self.entries:
                worksheet.append([entry.get(header, '') for header in COLUMN_HEADERS])
            workbook.save(filename)
        except Exception as exc:
            QMessageBox.critical(self, '저장 오류', f'엑셀 파일 저장 중 오류가 발생했습니다:\n{exc}')
            return

        QMessageBox.information(self, '저장 완료', f'엑셀 파일을 저장했습니다:\n{filename}')


def main() -> None:
    app = QApplication(sys.argv)
    window = EntryTableWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
