"""Modernized application entry point; original viewer2.py remains intact."""
import sys
from PyQt6.QtWidgets import QApplication
from viewer2 import MainWindow
from theme import apply_theme


def main():
    app = QApplication(sys.argv)
    apply_theme(app)
    window = MainWindow()
    # The legacy window sets a broad font-size rule. Clear that local override
    # so the global theme applies consistently to its existing widgets.
    window.setStyleSheet("")
    window.setWindowTitle("Project L.I.F.E. | Sponsorship Manager")
    window.resize(1200, 760)
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
