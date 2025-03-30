import csv
from datetime import datetime
import os
import logging

logger = logging.getLogger(__name__)

class AttendanceManager:
    def __init__(self, filename='attendance.csv'):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create attendance file if it doesn't exist"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Date', 'Time'])

    def mark_attendance(self, name):
        """Mark attendance for a person"""
        try:
            current_time = datetime.now()
            date = current_time.strftime('%Y-%m-%d')
            time = current_time.strftime('%H:%M:%S')
            
            with open(self.filename, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, date, time])
            
            return True
        except Exception as e:
            logger.error(f"Error marking attendance: {str(e)}")
            return False

    def get_all_records(self):
        """Retrieve all attendance records"""
        try:
            records = []
            with open(self.filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    records.append(row)
            return records
        except Exception as e:
            logger.error(f"Error reading attendance records: {str(e)}")
            return []
