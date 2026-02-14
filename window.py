from PyQt6.QtWidgets import QMainWindow, QLabel, QCheckBox, QLineEdit, QPushButton
from PyQt6.QtGui import QPixmap
from request_funcs import image_from_params, ll_from_address
from PyQt6.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Maps.API мучения")
        self.setGeometry(100, 100, 1000, 800)
        self.theme = 'light'
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setGeometry(50, 50, 700, 500)

        self.theme_switch = QCheckBox('Темная тема', self)
        self.theme_switch.setGeometry(800, 50, 150, 30)
        self.theme_switch.stateChanged.connect(self.on_theme_change)
        self.theme_switch.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        self.address_edit = QLineEdit(self)
        self.address_edit.setGeometry(800, 100, 150, 30)
        self.address_edit.setPlaceholderText("Введите адрес")

        self.search_button = QPushButton("Найти", self)
        self.search_button.setGeometry(800, 150, 150, 30)
        self.search_button.clicked.connect(self.on_search)

        self.marks = ['30,59,pm2dgl']   
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
                new_image = image_from_params(ll=self.ll, spn=self.spn, theme = self.theme, pt='~'.join(self.marks))
                self.set_image(new_image)
        elif symbol == Qt.Key.Key_PageDown:
            if float(self.spn.split(',')[0]) > 0.6:
                spn = self.spn.split(',')
                self.spn = f'{float(spn[0]) - 0.5},{float(spn[1]) - 0.5}'
                new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                self.set_image(new_image)
            else:
                if float(self.spn.split(',')[0]) > 0.11:
                    spn = self.spn.split(',')
                    self.spn = f'{float(spn[0]) - 0.1},{float(spn[1]) - 0.1}'
                    new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                    self.set_image(new_image)
                else:
                    if float(self.spn.split(',')[0]) > 0.015:
                        spn = self.spn.split(',')
                        self.spn = f'{float(spn[0]) - 0.01},{float(spn[1]) - 0.01}'
                        new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                        self.set_image(new_image)
        elif symbol == Qt.Key.Key_Left:
            ll = self.ll.split(',')
            if float(self.ll.split(',')[0]) > -175:
                self.ll = f'{float(ll[0]) - float(self.spn.split(',')[0]) / 2},{float(ll[1])}'
                new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                self.set_image(new_image)
        elif symbol == Qt.Key.Key_Right:
            if float(self.ll.split(',')[0]) < 175:
                ll = self.ll.split(',')
                self.ll = f'{float(ll[0]) + float(self.spn.split(',')[0]) / 2},{float(ll[1])}'
                new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                self.set_image(new_image)
        elif symbol == Qt.Key.Key_Up:
            if float(self.ll.split(',')[1]) < 85:
                ll = self.ll.split(',')
                self.ll = f'{float(ll[0])},{float(ll[1]) + float(self.spn.split(',')[1]) / 2}'
                new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                self.set_image(new_image)
        elif symbol == Qt.Key.Key_Down:
            if float(self.ll.split(',')[1]) > -85:
                ll = self.ll.split(',')
                self.ll = f'{float(ll[0])},{float(ll[1]) - float(self.spn.split(',')[1]) / 2}'
                new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                self.set_image(new_image)

    def on_theme_change(self):
        if self.theme == 'light':
            self.theme = 'dark'
        else:
            self.theme = 'light'
        new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
        self.set_image(new_image)
    
    def on_search(self):
        address = self.address_edit.text()
        self.address_edit.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.search_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocus()
        if address:
            ll = ll_from_address(address)
            if ll:
                self.ll = ll
                self.marks[0] = f'{self.ll},pm2dgl'
                self.spn = '0.005,0.005'
                new_image = image_from_params(ll=self.ll, spn=self.spn, theme=self.theme, pt='~'.join(self.marks))
                self.set_image(new_image)