from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from datetime import datetime,timezone, timedelta

# Initialize Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mistered_user:mister56neuf@localhost/mistered_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Replace with a strong secret key
# CORS(app)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:8081"}}, supports_credentials=True)


# Initialize database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
# Define Models
class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
        }

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False)
    insurance_number = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    severity = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    scheduled_hour = db.Column(db.Integer, nullable=True)  # New column to track scheduled hour

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "address": self.address,
            "phone_number": self.phone_number,
            "insurance_number": self.insurance_number,
            "description": self.description,
            "severity": self.severity,
            "created_at": self.created_at.isoformat(),
            "scheduled_hour": self.scheduled_hour,  # Include in the serialized output
        }

# API Endpoints

# Home Route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Mister Ed Medical Information System!"})


# CSRF Token Simulation
@app.route('/api/set_csrf_token', methods=['GET'])
def set_csrf_token():
    return jsonify({"message": "CSRF token simulation complete"})


# Login
@app.route('/api/login', methods=['POST'])
def login_employee():
    try:
        # Parse incoming JSON data
        data = request.get_json()
        if not data:
            return jsonify({"success": False, "message": "Invalid JSON data provided"}), 400

        # Extract employee_id and password from the request
        employee_id = data.get('employee_id')
        password = data.get('password')

        if not employee_id or not password:
            return jsonify({"success": False, "message": "Employee ID and password are required"}), 400

        # Query the database for the employee
        employee = Employee.query.filter_by(employee_id=employee_id).first()

        # Validate the employee and the password
        if not employee:
            return jsonify({"success": False, "message": "Employee not found"}), 404

        if not check_password_hash(employee.password_hash, password):
            return jsonify({"success": False, "message": "Incorrect password"}), 401

        # Set the session for the user
        session['user_id'] = employee.id
        return jsonify({
            "success": True,
            "user": employee.to_dict(),
        }), 200

    except Exception as e:
        # Log the error for debugging
        app.logger.error(f"An error occurred during login: {e}")
        return jsonify({"success": False, "message": "An internal server error occurred"}), 500



# Logout
@app.route('/api/logout', methods=['POST'])
def logout_employee():
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"})


# User Info
@app.route('/api/user', methods=['GET'])
def get_user_info():
    user_id = session.get('user_id')
    if user_id:
        employee = Employee.query.get(user_id)
        return jsonify(employee.to_dict()), 200
    return jsonify({"message": "Not logged in"}), 401


# Register
@app.route('/api/register', methods=['POST'])
def register_employee():
    data = request.get_json()
    print("Received data:", data)  # Add this line
    try:
        hashed_password = generate_password_hash(data['password'])
        employee = Employee(
            employee_id=data['employee_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password_hash=hashed_password,
        )
        db.session.add(employee)
        db.session.commit()
        return jsonify({"success": "User registered successfully"}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing key: {e}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Booking appointment 
@app.route('/api/appointments', methods=['POST'])
def book_appointment():
    """Endpoint to book an appointment."""
    try:
        # Parse the incoming JSON data
        data = request.get_json()

        # Create a new appointment object
        appointment = Appointment(
            first_name=data['first_name'],
            last_name=data['last_name'],
            address=data['address'],
            phone_number=data['phone_number'],
            insurance_number=data.get('insurance_number'),
            description=data.get('description'),
            severity= data.get('severity')
        )

        # Save the appointment to the database
        db.session.add(appointment)
        db.session.commit()

        # Return the saved appointment as a response
        return jsonify(appointment.to_dict()), 201
    except KeyError as e:
        # Handle missing keys in the request data
        return jsonify({"error": f"Missing key: {e}"}), 400
    except Exception as e:
        # Handle other errors
        return jsonify({"error": str(e)}), 500


@app.route('/api/appointments/today-overview', methods=['GET'])
def get_today_overview():
    """Fetch today's overview: Appointments and Pending Triage."""
    now = datetime.utcnow()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    # Count appointments since midnight
    appointments_count = Appointment.query.filter(Appointment.created_at >= midnight).count()

    # Count unscheduled patients
    pending_triage_count = Appointment.query.filter(Appointment.scheduled_hour == None, Appointment.created_at >= midnight).count()

    return jsonify({
        "appointments": appointments_count,
        "pending_triage": pending_triage_count
    }), 200


@app.route('/api/appointments/recent-activity', methods=['GET'])
def get_recent_activity():
    """Fetch recent activity (last 10 bookings)."""
    # Fetch recent activity (last 10 bookings)
    recent_activity = Appointment.query.order_by(Appointment.created_at.desc()).limit(10).all()

    return jsonify({
        "recent_activity": [
            {
                "id": appt.id,
                "message": f"{appt.first_name} {appt.last_name} booked an appointment at {appt.created_at.strftime('%H:%M')}"
            }
            for appt in recent_activity
        ]
    }), 200


# Patients in ER
@app.route('/api/appointments/current-schedule', methods=['GET'])
def get_current_schedule():
    """Fetch all patients who are scheduled."""
    # Query all patients with a non-null `scheduled_hour`
    scheduled_patients = Appointment.query.filter(
        Appointment.scheduled_hour.isnot(None)
    ).all()

    return jsonify({
        "scheduled_patients": [
            {
                "id": appt.id,
                "time": f"{appt.scheduled_hour}:00 - {(appt.scheduled_hour + 1) % 24}:00",  # Format the hour interval
                "patientName": f"{appt.first_name} {appt.last_name}",
                "priority": appt.severity
            }
            for appt in scheduled_patients
        ]
    }), 200


@app.route('/api/appointments/triage-results', methods=['GET'])
def get_triage_results():
    """Fetch triage results and scheduled appointments."""
    now = datetime.utcnow()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)

    appointments = Appointment.query.filter(Appointment.created_at >= midnight).all()

    triage_results = [
        appt for appt in appointments if appt.scheduled_hour is None
    ]
    schedule = {}
    for appt in appointments:
        if appt.scheduled_hour is not None:
            if appt.scheduled_hour not in schedule:
                schedule[appt.scheduled_hour] = []
            schedule[appt.scheduled_hour].append(appt)

    response = {
        "triage_results": [appt.to_dict() for appt in triage_results],
        "schedule": {
            hour: [appt.to_dict() for appt in appts]
            for hour, appts in schedule.items()
        },
    }
    return jsonify(response), 200

# get the list of the people scheduled today
@app.route('/api/appointments/update-schedule', methods=['POST'])
def update_schedule():
    """Update the schedule for a specific patient."""
    data = request.get_json()
    patient_id = data.get('id')
    schedule_time = data.get('schedule_time')

    if not patient_id or schedule_time is None:
        return jsonify({"success": False, "message": "Invalid data provided"}), 400

    appointment = Appointment.query.get(patient_id)
    if not appointment:
        return jsonify({"success": False, "message": "Appointment not found"}), 404

    appointment.scheduled_hour = schedule_time
    db.session.commit()

    return jsonify({"success": True, "message": "Schedule updated successfully"}), 200


@app.route('/api/appointments/history', methods=['GET'])
def get_patient_history():
    """
    Fetch the appointment history of a patient by their first and last name.
    """
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')

    if not first_name or not last_name:
        return jsonify({"error": "Missing first_name or last_name parameter"}), 400

    try:
        # Query appointments by first and last name
        appointments = Appointment.query.filter_by(first_name=first_name, last_name=last_name).all()
        
        # If no appointments are found
        if not appointments:
            return jsonify([]), 200

        # Serialize the appointments to JSON
        appointment_history = [appointment.to_dict() for appointment in appointments]

        return jsonify(appointment_history), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/appointments/all-records', methods=['GET'])
@cross_origin(origins="http://localhost:8081")
def get_all_patients():
    patients = Appointment.query.all()
    return jsonify({
        "patients": [
            {
                "id": patient.id,
                "first_name": patient.first_name,
                "last_name": patient.last_name,
                "phone_number": patient.phone_number,
                "address": patient.address,
                "severity": patient.severity,
                "scheduled_hour": patient.scheduled_hour,
                "date": patient.created_at.date().isoformat()  # Include the date
            }
            for patient in patients
        ]
    }), 200



# Run Flask App
if __name__ == '__main__':
    with app.app_context():
        #db.create_all()   Create tables if not exists
        app.run(debug=True)
