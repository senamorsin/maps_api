from PyQt6.QtWidgets import QMainWindow, QLabel
from PyQt6.QtGui import QPixmap
from request_funcs import image_from_params
from PyQt6.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maps.API мучения")
        self.setGeometry(100, 100, 1000, 800)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setGeometry(50, 50, 900, 700)
        
        self.ll = None
        self.spn = None

    def set_image(self, image_data: bytes):
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        print('done')

    def keyPressEvent(self, event):
        symbol = event.key()
        if symbol == Qt.Key.Key_PageUp:
            if float(self.spn.split(',')[0]) < 10:
                spn = self.spn.split(',')
                self.spn = f'{float(spn[0]) + 0.5},{float(spn[1]) + 0.5}'
                new_image = image_from_params(ll=self.ll, spn=self.spn)
                self.set_image(new_image)
        elif symbol == Qt.Key.Key_PageDown:
            if float(self.spn.split(',')[0]) > 0.6:
                spn = self.spn.split(',')
                self.spn = f'{float(spn[0]) - 0.5},{float(spn[1]) - 0.5}'
                new_image = image_from_params(ll=self.ll, spn=self.spn)
                self.set_image(new_image)
            else:
                if float(self.spn.split(',')[0]) > 0.11:
                    spn = self.spn.split(',')
                    self.spn = f'{float(spn[0]) - 0.1},{float(spn[1]) - 0.1}'
                    new_image = image_from_params(ll=self.ll, spn=self.spn)
                    self.set_image(new_image)
                else:
                    if float(self.spn.split(',')[0]) > 0.015:
                        spn = self.spn.split(',')
                        self.spn = f'{float(spn[0]) - 0.01},{float(spn[1]) - 0.01}'
                        new_image = image_from_params(ll=self.ll, spn=self.spn)
                        self.set_image(new_image)
        print(self.spn)