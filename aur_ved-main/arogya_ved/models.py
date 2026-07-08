from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String)
    role = Column(String, default="citizen")  # admin, employee, citizen
    hashed_password = Column(String, nullable=False)
    # Profile
    age = Column(Integer)
    gender = Column(String)
    aadhaar = Column(String)
    employee_id = Column(String)
    designation = Column(String)
    experience = Column(Integer)
    healthcare_center = Column(String)
    department = Column(String)
    nearest_phc = Column(String)
    # Location
    state = Column(String)
    district = Column(String)
    village = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    # Health
    medical_conditions = Column(Text, default="[]")
    health_score = Column(Integer, default=75)
    risk_score = Column(Integer, default=30)
    # Status
    is_verified = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Notifications
    notifications = relationship("Notification", back_populates="user")
    appointments = relationship("Appointment", back_populates="user")


class PHC(Base):
    __tablename__ = "phcs"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    district = Column(String)
    state = Column(String)
    village = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    doctors = Column(Integer, default=2)
    nurses = Column(Integer, default=5)
    beds = Column(Integer, default=20)
    available_beds = Column(Integer, default=10)
    medicine_stock = Column(Integer, default=70)  # percentage
    health_score = Column(Integer, default=75)
    icu_beds = Column(Integer, default=0)
    oxygen_cylinders = Column(Integer, default=10)
    ambulances = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


class DiseaseReport(Base):
    __tablename__ = "disease_reports"
    id = Column(Integer, primary_key=True, index=True)
    disease = Column(String, nullable=False)
    cases = Column(Integer, default=0)
    village = Column(String)
    district = Column(String)
    state = Column(String)
    risk_level = Column(String, default="low")  # low, medium, high, critical
    reported_by = Column(Integer, ForeignKey("users.id"))
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class MedicineStock(Base):
    __tablename__ = "medicine_stocks"
    id = Column(Integer, primary_key=True, index=True)
    medicine_name = Column(String, nullable=False)
    quantity = Column(Integer, default=0)
    phc_name = Column(String)
    updated_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class HealthCamp(Base):
    __tablename__ = "health_camps"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String)
    district = Column(String)
    state = Column(String)
    date = Column(String)
    time = Column(String)
    camp_type = Column(String)
    organizer = Column(String)
    capacity = Column(Integer, default=100)
    registered = Column(Integer, default=0)
    lat = Column(Float)
    lng = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    appointments = relationship("Appointment", back_populates="camp")


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    camp_id = Column(Integer, ForeignKey("health_camps.id"), nullable=True)
    appointment_date = Column(String)
    appointment_time = Column(String)
    phc_name = Column(String)
    status = Column(String, default="pending")  # pending, confirmed, completed, cancelled
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="appointments")
    camp = relationship("HealthCamp", back_populates="appointments")


class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    message = Column(Text)
    notif_type = Column(String, default="info")  # reminder, alert, camp, warning
    priority = Column(String, default="medium")  # low, medium, high
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="notifications")


class EmployeeRegistration(Base):
    __tablename__ = "employee_registrations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")  # pending, approved, rejected
    rejection_reason = Column(Text)
    reviewed_by = Column(Integer)
    reviewed_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)


class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String)
    phone = Column(String)
    aadhaar = Column(String)
    # Health info
    disease = Column(String)  # primary disease
    medicines = Column(Text)  # JSON array of medicines
    # Location
    village = Column(String)
    district = Column(String)
    state = Column(String)
    phc_name = Column(String)
    # Documents
    prescription_photo = Column(String)  # path to photo/pdf
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationship
    prescriptions = relationship("Prescription", back_populates="patient")


class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    medicine_name = Column(String)
    dosage = Column(String)
    duration = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    patient = relationship("Patient", back_populates="prescriptions")
