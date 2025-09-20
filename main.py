import sys,requests,os
from PyQt5.QtGui import QPixmap
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow,QApplication,QLabel,QWidget,QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import QVBoxLayout
from requests import HTTPError


class UI(QMainWindow):
    def __init__(self):
        super(UI,self).__init__()
        uic.loadUi('bitcoin.ui',self)
        # Define Widgets
        self.label_price = self.findChild(QLabel,'label_price')
        self.label_picture = self.findChild(QLabel,'label_picture')
        self.pushButton_price = self.findChild(QPushButton,'pushButton_price')
        self.pushButton_chart = self.findChild(QPushButton,'pushButton_chart')
        self.chart = self.findChild(QWidget,'chart')

        # connect pushbutton
        self.pushButton_price.clicked.connect(self.update_price)
        self.pushButton_chart.clicked.connect(self.update_chart)
        self.show()

    def update_price(self):
            data = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd").json()
            price = data["bitcoin"]["usd"]
            self.label_price.setText(f" قیمت بیتکوین{price}$")
            # print(price)

    def update_chart(self):
        # پاک کردن layout قبلی
        if self.chart.layout() is not None:
            for i in reversed(range(self.chart.layout().count())):
                self.chart.layout().itemAt(i).widget().setParent(None)

        from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
        from matplotlib.figure import Figure
        import datetime, requests
        from PyQt5.QtWidgets import QVBoxLayout

        # گرفتن داده
        url = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
        params = {"vs_currency": "usd", "days": "90"}
        data = requests.get(url, params=params).json()
        prices = data["prices"]
        dates = [datetime.datetime.fromtimestamp(p[0] / 1000) for p in prices]
        values = [p[1] for p in prices]

        # رسم نمودار
        figure = Figure()
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)
        ax.plot(dates, values)
        ax.set_title("Bitcoin Price (Last 90 Days)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (USD)")

        # اضافه کردن Canvas به QWidget
        layout = QVBoxLayout(self.chart)
        layout.addWidget(canvas)
        self.chart.setLayout(layout)


os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = r"F:\aferdos\پایتون\GUI\venv\Lib\site-packages\PyQt5\Qt5\plugins\platforms"
app = QApplication(sys.argv)
window = UI()
app.exec_()