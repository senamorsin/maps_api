from window import Window
from PyQt6.QtWidgets import QApplication
from argparse import ArgumentParser
from request_funcs import ll_from_address, image_from_params
import sys

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-l", "--ll", required=True, help="longitude and latitude")
    arg_parser.add_argument("-s", "--spn", required=True, help="span")
    arguments = arg_parser.parse_args()
    ll = arguments.ll
    spn = arguments.spn
    print(ll, spn)

    app = QApplication(sys.argv)
    window = Window()

    image = image_from_params(ll=ll, spn=spn)
    window.set_image(image)

    window.show()
    sys.exit(app.exec())