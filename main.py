import sys,requests,os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QWidget,QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import datetime
from PyQt5.QtWidgets import QVBoxLayout
from requests import HTTPError


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('bitcoin.ui',self)
        # Define Widgets
        self.label_price = self.findChild(QLabel,'label_price')
        self.label = self.findChild(QLabel,'label')
        self.label_picture = self.findChild(QLabel,'label_picture')
        self.pushButton_price = self.findChild(QPushButton,'pushButton_price')
        self.pushButton_chart = self.findChild(QPushButton,'pushButton_chart')
        self.chart = self.findChild(QWidget,'chart')

        # connect pushbutton
        self.pushButton_price.clicked.connect(self.update_price)
        self.pushButton_chart.clicked.connect(self.update_chart)
        self.show()
        self.label.setText('bitcoin price')
    def update_price(self):
            data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
            price = data["bitcoin"]["usd"]
            self.label_price.setText(f" قیمت بیتکوین{price}$")
            try:
                response = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd")
                response.raise_for_status()

            except requests.exceptions.HTTPError as http_error:
                match response.status_code:
                    case 400:
                        self.display_error("درخواست نامعتبر:\nورودی خود را بررسی کنید")
                    case 401:
                        self.display_error("خطای دسترسی:\nکلید API نامعتبر است")
                    case 403:
                        self.display_error("دسترسی ممنوع:\nاجازه دسترسی وجود ندارد")
                    case 404:
                        self.display_error("یافت نشد:\nداده مورد نظر پیدا نشد")
                    case 500:
                        self.display_error("خطای داخلی سرور:\nلطفاً بعداً دوباره تلاش کنید")
                    case 502:
                        self.display_error("درگاه نامعتبر:\nپاسخ نامعتبر از سرور دریافت شد")
                    case 503:
                        self.display_error("سرویس در دسترس نیست:\nسرور در حال حاضر در دسترس نیست")
                    case 504:
                        self.display_error("پایان مهلت درگاه:\nپاسخی از سرور دریافت نشد")
                    case _:
                        self.display_error(f"خطای HTTP رخ داد:\n{http_error}")

            except requests.exceptions.ConnectionError:
                self.display_error("خطای اتصال:\nاتصال اینترنت خود را بررسی کنید")

            except requests.exceptions.Timeout:
                self.display_error("خطای زمان‌بر شدن:\nپاسخ سرور خیلی طول کشید")

            except requests.exceptions.TooManyRedirects:
                self.display_error("تعداد تغییر مسیر زیاد:\nنشانی (URL) را بررسی کنید")

            except requests.exceptions.RequestException as req_error:
                self.display_error(f"خطای درخواست:\n{req_error}")
            # print(price)

    def update_chart(self):

        if self.chart.layout() is not None:
            for i in reversed(range(self.chart.layout().count())):
                self.chart.layout().itemAt(i).widget().setParent(None)

        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": "90"}
        data = requests.get(url, params=params).json()
        prices = data["prices"]
        dates = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
        values = [p[1] for p in prices]


        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        ax.plot(dates, values)
        ax.set_title("Bitcoin Price (Last 90 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")

        layout = QVBoxLayout(self.chart)
        layout.addWidget(canvas)
        self.chart.setLayout(layout)
        # print(self.label_price)

    def display_error(self,message):
        self.label.setStyleSheet("font-size : 30px")
        self.label.setText(message)
        self.label.setWordWrap(True)


os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"F:\aferdos\پایتون\GUI\venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
app = QApplication(sys.argv)
window = UI()
app.exec_()