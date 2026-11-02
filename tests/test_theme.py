"""Non-database smoke checks for the new theme module."""
import unittest
from theme import APP_STYLESHEET


class ThemeTests(unittest.TestCase):
    def test_theme_styles_tables(self):
        self.assertIn("QTableView", APP_STYLESHEET)

    def test_theme_styles_keyboard_focus(self):
        self.assertIn("QLineEdit:focus", APP_STYLESHEET)


if __name__ == "__main__":
    unittest.main()
