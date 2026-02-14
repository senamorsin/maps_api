from window import Window
from PyQt6.QtWidgets import QApplication
from argparse import ArgumentParser
from request_funcs import ll_from_address, image_from_params
import sys

if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-l", "--ll",
                            help="longitude and latitude",
                            default='30,59')
    arg_parser.add_argument("-s", "--spn",
                            help="span",
                            default='1,1')

    arguments = arg_parser.parse_args()
    ll = arguments.ll
    spn = arguments.spn

    app = QApplication(sys.argv)
    window = Window()

    image = image_from_params(ll=ll, spn=spn)
    window.set_image(image)
    window.ll = ll
    window.spn = spn

    window.show()
    sys.exit(app.exec())