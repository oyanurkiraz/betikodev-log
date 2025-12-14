# tests/test_parser.py
import unittest
from datetime import datetime
from src.parser import parse_log_line

class TestParser(unittest.TestCase):
    
    def test_valid_log_line(self):
        """Geçerli bir log satırının doğru ayrıştırıldığını test eder."""
        line = "[2025-12-09 14:23:15] INFO (user_id=12, post_id=34): Test mesajı içeriği"
        record = parse_log_line(line)
        
        self.assertIsNotNone(record, "Log kaydı None dönmemeli.")
        self.assertEqual(record.level, "INFO")
        self.assertEqual(record.user_id, 12)
        self.assertEqual(record.post_id, 34)
        self.assertEqual(record.message, "Test mesajı içeriği")
        self.assertEqual(record.timestamp, datetime(2025, 12, 9, 14, 23, 15))

    def test_invalid_log_line(self):
        """Formatı bozuk bir satırın None döndürdüğünü test eder."""
        line = "Bu tamamen hatalı bir log satırıdır."
        record = parse_log_line(line)
        self.assertIsNone(record, "Hatalı satır için None dönmeli.")

    def test_error_property(self):
        """is_error özelliğinin doğru çalışıp çalışmadığını test eder."""
        line = "[2025-12-09 14:23:15] ERROR (user_id=1, post_id=1): Hata var"
        record = parse_log_line(line)
        self.assertTrue(record.is_error)

if __name__ == '__main__':
    unittest.main()