import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from face_utils import FaceProcessor
from attendance import AttendanceManager

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "default-secret-key")

try:
    # Initialize face processor and attendance manager
    face_processor = FaceProcessor()
    attendance_manager = AttendanceManager()
    logger.info("Successfully initialized FaceProcessor and AttendanceManager")
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/view_attendance')
def view_attendance():
    try:
        attendance_records = attendance_manager.get_all_records()
        return render_template('view_attendance.html', records=attendance_records)
    except Exception as e:
        logger.error(f"Error retrieving attendance records: {str(e)}")
        return "Error loading attendance records", 500

@app.route('/api/register', methods=['POST'])
def register_face():
    try:
        image_data = request.json['image']
        name = request.json['name']
        success, message = face_processor.register_face(image_data, name)
        return jsonify({'success': success, 'message': message})
    except Exception as e:
        logger.error(f"Error during registration: {str(e)}")
        return jsonify({'success': False, 'message': 'Registration failed'}), 400

@app.route('/api/verify', methods=['POST'])
def verify_face():
    try:
        image_data = request.json['image']
        success, name = face_processor.verify_face(image_data)
        if success:
            attendance_manager.mark_attendance(name)
            return jsonify({'success': True, 'name': name})
        return jsonify({'success': False, 'message': 'Face not recognized'})
    except Exception as e:
        logger.error(f"Error during verification: {str(e)}")
        return jsonify({'success': False, 'message': 'Verification failed'}), 400

@app.route('/download_attendance')
def download_attendance():
    try:
        return send_file(
            'attendance.csv',
            as_attachment=True,
            download_name='attendance.csv',
            mimetype='text/csv'
        )
    except Exception as e:
        logger.error(f"Error downloading attendance: {str(e)}")
        return "Error downloading attendance file", 400