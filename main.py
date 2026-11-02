"""Launch the existing application with diagnostic startup logging.

Run with: python -u main.py
The original viewer2.py remains unchanged.
"""
import logging
from pathlib import Path
import sys
import traceback

LOG_PATH = Path.home() / "database-modern-startup.log"


def main():
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        encoding="utf-8",
    )
    try:
        print("Database-Modern: importing Qt...", flush=True)
        from PyQt6.QtWidgets import QApplication
        print("Database-Modern: importing application...", flush=True)
        from viewer2 import MainWindow
        from theme import apply_theme
        print("Database-Modern: creating QApplication...", flush=True)
        app = QApplication(sys.argv)
        print("Database-Modern: constructing main window...", flush=True)
        window = MainWindow()
        window.setWindowTitle("Project L.I.F.E. | Sponsorship Manager")
        window.resize(1200, 760)
        # Apply after window construction, avoiding global widget restyling
        # during legacy initialization. Keep a single global style source.
        apply_theme(app)
        window.setStyleSheet("")
        print("Database-Modern: showing window...", flush=True)
        window.show()
        print("Database-Modern: event loop running.", flush=True)
        return app.exec()
    except Exception:
        details = traceback.format_exc()
        logging.exception("Startup failed")
        print(details, file=sys.stderr, flush=True)
        print(f"Startup log: {LOG_PATH}", file=sys.stderr, flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
