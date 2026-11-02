"""Launch the modern shell while retaining all legacy database workflows."""
import logging
from pathlib import Path
import sys
import traceback

LOG_PATH = Path.home() / "database-modern-startup.log"


def main():
    logging.basicConfig(filename=LOG_PATH, level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s",
                        encoding="utf-8")
    try:
        print("Database-Modern: importing Qt...", flush=True)
        from PyQt6.QtWidgets import QApplication
        print("Database-Modern: importing application...", flush=True)
        from modern_window import ModernMainWindow
        from theme import apply_theme
        app = QApplication(sys.argv)
        print("Database-Modern: constructing main window...", flush=True)
        window = ModernMainWindow()
        window.setWindowTitle("Project L.I.F.E. | Sponsorship Manager")
        window.resize(1250, 780)
        apply_theme(app)
        window.setStyleSheet("")
        window.show()
        print("Database-Modern: event loop running.", flush=True)
        return app.exec()
    except Exception:
        logging.exception("Startup failed")
        print(traceback.format_exc(), file=sys.stderr, flush=True)
        print(f"Startup log: {LOG_PATH}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
