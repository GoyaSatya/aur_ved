from fastapi import FastAPI, Request, Depends, HTTPException, Form, UploadFile, File, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from jinja2 import Environment, FileSystemLoader
from starlette.templating import Jinja2Templates
import uvicorn, json, random, os, math
from datetime import datetime, timedelta

from database import engine, get_db, Base
from models import User, DiseaseReport, MedicineStock, HealthCamp, Appointment, Notification, PHC, Patient, Prescription

# Create uploads directory if it doesn't exist
os.makedirs("uploads", exist_ok=True)
from auth import create_access_token, hash_password, verify_password, get_current_user
from ai_engine import (predict_disease_outbreak, forecast_demand, get_health_score,
                       get_ai_recommendations, simulate_scenario, get_digital_twin_data)
from india_data import INDIA_STATES, INDIA_PHC_LOCATIONS

Base.metadata.create_all(bind=engine)
app = FastAPI(title="HealthPulse AI", version="1.0.0")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Jinja2 env — works correctly with starlette's new TemplateResponse(request, name) API
_jinja_env = Environment(loader=FileSystemLoader("templates"), autoescape=True)
templates = Jinja2Templates(env=_jinja_env)

def seed_data(db: Session):
    if db.query(User).first():
        return
    admin = User(name="Admin Officer", email="admin@healthpulse.gov.in",
        phone="9000000001", role="admin", hashed_password=hash_password("Admin@123"),
        is_verified=True, is_approved=True, state="Telangana", district="Hyderabad")
    citizen = User(name="Satya Prakash", email="satya@example.com",
        phone="9876543210", role="citizen", hashed_password=hash_password("Citizen@123"),
        is_verified=True, is_approved=True, age=34, gender="Male",
        state="Odisha", district="Khordha", village="Bhubaneswar",
        medical_conditions=json.dumps(["Diabetes", "Blood Pressure"]),
        health_score=78, risk_score=42, nearest_phc="PHC Bhubaneswar",
        lat=20.2961, lng=85.8245)
    employee = User(name="Dr. Goyanshi Mohanty", email="priya@phc.gov.in",
        phone="9111111111", role="employee", hashed_password=hash_password("Employee@123"),
        is_verified=True, is_approved=True, designation="Doctor", experience=8,
        state="Telangana", district="Warangal", village="Hanamkonda",
        healthcare_center="PHC Hanamkonda")
    db.add_all([admin, citizen, employee])
    db.flush()
    phcs = [
        # Telangana
        PHC(name="PHC Hanamkonda", district="Warangal", state="Telangana", village="Hanamkonda",
            lat=18.0007, lng=79.5941, doctors=3, nurses=8, beds=30, available_beds=12,
            medicine_stock=75, health_score=82, oxygen_cylinders=14, ambulances=2),
        PHC(name="PHC Kazipet", district="Warangal", state="Telangana", village="Kazipet",
            lat=17.9784, lng=79.5142, doctors=2, nurses=6, beds=20, available_beds=5,
            medicine_stock=45, health_score=58, oxygen_cylinders=6, ambulances=1),
        PHC(name="CHC Warangal Urban", district="Warangal", state="Telangana", village="Warangal",
            lat=17.9784, lng=79.5941, doctors=8, nurses=20, beds=80, available_beds=35,
            medicine_stock=88, health_score=91, oxygen_cylinders=25, ambulances=4),
        PHC(name="PHC Narsampet", district="Warangal", state="Telangana", village="Narsampet",
            lat=17.9260, lng=79.8940, doctors=2, nurses=5, beds=15, available_beds=3,
            medicine_stock=38, health_score=42, oxygen_cylinders=4, ambulances=1),
        # Odisha
        PHC(name="PHC Bhubaneswar", district="Khordha", state="Odisha", village="Bhubaneswar",
            lat=20.2961, lng=85.8245, doctors=4, nurses=9, beds=35, available_beds=15,
            medicine_stock=80, health_score=85, oxygen_cylinders=18, ambulances=3),
        PHC(name="PHC Cuttack", district="Cuttack", state="Odisha", village="Cuttack",
            lat=20.4625, lng=85.8829, doctors=3, nurses=7, beds=25, available_beds=8,
            medicine_stock=65, health_score=78, oxygen_cylinders=12, ambulances=2),
    ]
    db.add_all(phcs)
    db.flush()
    diseases = [
        DiseaseReport(disease="Diarrhea", cases=12, village="Hanamkonda", district="Warangal",
                      state="Telangana", risk_level="medium", reported_by=3),
        DiseaseReport(disease="Malaria", cases=18, village="Kazipet", district="Warangal",
                      state="Telangana", risk_level="high", reported_by=3),
        DiseaseReport(disease="Dengue", cases=9, village="Narsampet", district="Warangal",
                      state="Telangana", risk_level="medium", reported_by=3),
        DiseaseReport(disease="Typhoid", cases=4, village="Warangal", district="Warangal",
                      state="Telangana", risk_level="low", reported_by=3),
    ]
    db.add_all(diseases)
    camps = [
        # Telangana
        HealthCamp(name="Free Diabetes Screening Camp", location="PHC Hanamkonda",
            district="Warangal", state="Telangana", date=(datetime.now()+timedelta(days=1)).strftime("%Y-%m-%d"),
            time="10:00 AM - 3:00 PM", camp_type="Diabetes", organizer="District Health Dept",
            lat=18.0007, lng=79.5941),
        HealthCamp(name="Eye Checkup Camp", location="Community Hall, Warangal",
            district="Warangal", state="Telangana", date=(datetime.now()+timedelta(days=3)).strftime("%Y-%m-%d"),
            time="9:00 AM - 1:00 PM", camp_type="Eye", organizer="Lions Club + PHC",
            lat=17.9784, lng=79.5941),
        HealthCamp(name="Women Health & Anemia Camp", location="PHC Kazipet",
            district="Warangal", state="Telangana", date=(datetime.now()+timedelta(days=5)).strftime("%Y-%m-%d"),
            time="10:00 AM - 2:00 PM", camp_type="Women Health", organizer="State Health Mission",
            lat=17.9784, lng=79.5142),
        # Odisha
        HealthCamp(name="Free Health Checkup Camp", location="PHC Bhubaneswar",
            district="Khordha", state="Odisha", date=(datetime.now()+timedelta(days=2)).strftime("%Y-%m-%d"),
            time="9:00 AM - 2:00 PM", camp_type="General", organizer="Odisha State Health Mission",
            lat=20.2961, lng=85.8245),
        HealthCamp(name="Dengue Awareness & Screening Camp", location="Community Hall, Bhubaneswar",
            district="Khordha", state="Odisha", date=(datetime.now()+timedelta(days=4)).strftime("%Y-%m-%d"),
            time="10:00 AM - 4:00 PM", camp_type="General", organizer="Municipal Corporation",
            lat=20.2700, lng=85.8400),
        HealthCamp(name="Maternal & Child Health Camp", location="PHC Cuttack",
            district="Cuttack", state="Odisha", date=(datetime.now()+timedelta(days=6)).strftime("%Y-%m-%d"),
            time="8:00 AM - 1:00 PM", camp_type="Women Health", organizer="UNICEF",
            lat=20.4625, lng=85.8829),
    ]
    db.add_all(camps)
    db.flush()
    notifs = [
        Notification(user_id=2, title="Diabetes Checkup Due",
            message="You have a due Diabetes checkup. It's been 6 months since your last visit.",
            notif_type="reminder", priority="high"),
        Notification(user_id=2, title="Free Health Camp Tomorrow",
            message="Free health camp near you tomorrow at PHC Bhubaneswar.",
            notif_type="camp", priority="medium"),
        Notification(user_id=2, title="BP Checkup Due",
            message="Your BP checkup is due. Please schedule an appointment.",
            notif_type="reminder", priority="medium"),
    ]
    db.add_all(notifs)
    db.commit()

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    try:
        seed_data(db)
    except Exception as e:
        db.rollback()
    finally:
        db.close()

# ── Public Pages ──────────────────────────────────────────────────────────────
@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request, "landing.html")

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")

@app.get("/register/employee", response_class=HTMLResponse)
async def employee_register_page(request: Request):
    return templates.TemplateResponse(request, "employee_register.html")

# ── Dashboard Pages ────────────────────────────────────────────────────────────
@app.get("/citizen/dashboard", response_class=HTMLResponse)
async def citizen_dashboard(request: Request):
    return templates.TemplateResponse(request, "citizen_dashboard.html")

@app.get("/admin/dashboard", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    return templates.TemplateResponse(request, "admin_dashboard.html")

@app.get("/employee/dashboard", response_class=HTMLResponse)
async def employee_dashboard(request: Request):
    return templates.TemplateResponse(request, "employee_dashboard.html")

# ── Auth API ──────────────────────────────────────────────────────────────────
@app.post("/api/auth/register")
async def register(response: Response, name: str = Form(...), email: str = Form(...), phone: str = Form(...),
    password: str = Form(...), role: str = Form("citizen"), age: int = Form(None),
    gender: str = Form(None), state: str = Form(None), district: str = Form(None),
    village: str = Form(None), medical_conditions: str = Form("[]"),
    nearest_phc: str = Form(None), lat: float = Form(None), lng: float = Form(None),
    db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(name=name, email=email, phone=phone, role=role,
        hashed_password=hash_password(password), age=age, gender=gender,
        state=state, district=district, village=village, nearest_phc=nearest_phc,
        medical_conditions=medical_conditions, is_verified=True,
        is_approved=(role == "citizen"), health_score=random.randint(60, 95),
        risk_score=random.randint(15, 55), lat=lat, lng=lng)
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({"sub": str(user.id), "role": user.role})
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)
    return {"access_token": token, "role": user.role, "name": user.name,
            "redirect": f"/{user.role}/dashboard"}

@app.post("/api/auth/login")
async def login(response: Response, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not user.is_approved:
        raise HTTPException(status_code=403, detail="Account pending approval")
    token = create_access_token({"sub": str(user.id), "role": user.role})
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=86400)
    return {"access_token": token, "role": user.role, "name": user.name,
            "redirect": f"/{user.role}/dashboard"}

@app.post("/api/auth/employee-register")
async def employee_register(full_name: str = Form(...), email: str = Form(...),
    phone: str = Form(...), password: str = Form(...), aadhaar: str = Form(...),
    employee_id: str = Form(...), designation: str = Form(...), experience: int = Form(...),
    healthcare_center: str = Form(...), district: str = Form(...),
    state: str = Form(...), village: str = Form(...), department: str = Form(...),
    db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(name=full_name, email=email, phone=phone, role="employee",
        hashed_password=hash_password(password), aadhaar=aadhaar, employee_id=employee_id,
        designation=designation, experience=experience, healthcare_center=healthcare_center,
        district=district, state=state, village=village, department=department,
        is_verified=False, is_approved=False)
    db.add(user)
    db.commit()
    return {"message": "Registration submitted. Pending admin approval.", "status": "pending"}

# Helper function to get user or return default
def get_user_or_default(request, db):
    token = request.cookies.get("access_token") or request.headers.get("Authorization","").replace("Bearer ","")
    if token:
        try:
            return get_current_user(token, db)
        except:
            pass
    return None

# ── Citizen API ────────────────────────────────────────────────────────────────
@app.get("/api/citizen/profile")
async def get_citizen_profile(request: Request, db: Session = Depends(get_db)):
    user = get_user_or_default(request, db)
    if user:
        conditions = []
        try: conditions = json.loads(user.medical_conditions or "[]")
        except: pass
        return {"name": user.name, "age": user.age, "gender": user.gender, "email": user.email,
                "phone": user.phone, "village": user.village, "district": user.district,
                "state": user.state, "medical_conditions": conditions,
                "health_score": user.health_score or 78, "risk_score": user.risk_score or 42,
                "nearest_phc": user.nearest_phc or "PHC Hanamkonda",
                "blood_pressure": "120/80", "blood_sugar": "110 mg/dl",
                "weight": "70 kg", "last_checkup": "6 months ago", "bmi": 24.6,
                "upcoming_checkups": 2, "active_conditions": len(conditions)}
    # Return default profile for unauthenticated users
    return {"name": "Guest User", "age": 35, "gender": "Male", "email": "guest@example.com",
            "phone": "9876543210", "village": "Bhubaneswar", "district": "Khordha",
            "state": "Odisha", "medical_conditions": ["Diabetes", "Blood Pressure"],
            "health_score": 78, "risk_score": 42,
            "nearest_phc": "PHC Bhubaneswar",
            "blood_pressure": "120/80", "blood_sugar": "110 mg/dl",
            "weight": "70 kg", "last_checkup": "6 months ago", "bmi": 24.6,
            "upcoming_checkups": 2, "active_conditions": 2}

@app.get("/api/citizen/notifications")
async def get_citizen_notifications(request: Request, db: Session = Depends(get_db)):
    user = get_user_or_default(request, db)
    if user:
        notifs = db.query(Notification).filter(Notification.user_id == user.id).order_by(Notification.created_at.desc()).limit(10).all()
        return [{"id": n.id, "title": n.title, "message": n.message, "type": n.notif_type,
                 "priority": n.priority, "time_ago": "1 day ago", "read": n.is_read} for n in notifs]
    # Return default notifications for unauthenticated users
    return [
        {"id": 1, "title": "Diabetes Checkup Due", "message": "You have a due Diabetes checkup. It's been 6 months since your last visit.", "type": "reminder", "priority": "high", "time_ago": "1 day ago", "read": False},
        {"id": 2, "title": "Free Health Camp Tomorrow", "message": "Free health camp near you tomorrow at PHC Bhubaneswar.", "type": "camp", "priority": "medium", "time_ago": "2 days ago", "read": False},
        {"id": 3, "title": "BP Checkup Due", "message": "Your BP checkup is due. Please schedule an appointment.", "type": "reminder", "priority": "medium", "time_ago": "5 days ago", "read": False}
    ]

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points in km using Haversine formula"""
    R = 6371  # Earth radius in km
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.get("/api/citizen/camps")
async def get_health_camps(request: Request, db: Session = Depends(get_db)):
    # Default to Bhubaneswar, Odisha if user not found
    user_lat = 20.2961
    user_lng = 85.8245
    user_state = "Odisha"
    user_district = "Khordha"

    user = get_user_or_default(request, db)
    if user:
        # Use user's lat/lng if available, otherwise try to get from location
        if user.lat is not None and user.lng is not None:
            user_lat = user.lat
            user_lng = user.lng
        user_state = user.state or "Odisha"
        user_district = user.district or "Khordha"

    # Get all camps
    all_camps = db.query(HealthCamp).all()

    # Calculate distance for each camp and sort
    camps_with_distance = []
    for camp in all_camps:
        # If camp has no lat/lng, try to approximate or skip
        if camp.lat is None or camp.lng is None:
            # Default distance for camps without coordinates
            distance = 9999.0
        else:
            distance = haversine_distance(user_lat, user_lng, camp.lat, camp.lng)

        camps_with_distance.append({
            "camp": camp,
            "distance": distance
        })

    # Sort by distance, then by date
    camps_with_distance.sort(key=lambda x: (x["distance"], x["camp"].date))

    # Return only nearest 6 camps
    return [{"id": c["camp"].id, "name": c["camp"].name, "location": c["camp"].location,
             "date": c["camp"].date, "time": c["camp"].time, "type": c["camp"].camp_type,
             "organizer": c["camp"].organizer, "state": c["camp"].state,
             "district": c["camp"].district, "lat": c["camp"].lat, "lng": c["camp"].lng,
             "distance_km": round(c["distance"], 1)}
            for c in camps_with_distance[:6]]

@app.get("/api/citizen/reminders")
async def get_reminders(request: Request, db: Session = Depends(get_db)):
    nearest_phc = "PHC Bhubaneswar"
    user_state = "Odisha"
    user_district = "Khordha"
    camp_id = 4  # Default to PHC Bhubaneswar camp

    user = get_user_or_default(request, db)
    if user:
        nearest_phc = user.nearest_phc or "PHC Bhubaneswar"
        user_state = user.state or "Odisha"
        user_district = user.district or "Khordha"
        # Find a camp in user's district for camp_id
        local_camp = db.query(HealthCamp).filter(
            (HealthCamp.state == user_state) & (HealthCamp.district == user_district)
        ).order_by(HealthCamp.date).first()
        if local_camp:
            camp_id = local_camp.id

    return [
        {"disease": "Diabetes Screening", "message": "It has been 6 months since your last checkup.",
         "location": nearest_phc, "date": "Next available slot (10:00 AM - 2:00 PM)",
         "priority": "high", "icon": "🩺", "camp_id": camp_id},
        {"disease": "Blood Pressure Check", "message": "BP not checked for 3 months.",
         "location": nearest_phc, "date": "Next available slot",
         "priority": "medium", "icon": "❤️", "camp_id": None},
    ]

@app.post("/api/citizen/book-appointment")
async def book_appointment(request: Request, camp_id: int = Form(...), db: Session = Depends(get_db)):
    # Try to get user from token; if not logged in, still confirm booking for demo
    token = request.cookies.get("access_token") or request.headers.get("Authorization","").replace("Bearer ","")
    user_id = None
    try:
        user = get_current_user(token, db)
        user_id = user.id
    except Exception:
        user_id = 2  # fallback to demo citizen for unauthenticated booking demo

    camp = db.query(HealthCamp).filter(HealthCamp.id == camp_id).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Camp not found")

    # Check if already booked
    existing = db.query(Appointment).filter(
        Appointment.user_id == user_id,
        Appointment.camp_id == camp.id
    ).first()
    if existing:
        return {"message": f"Already booked at {camp.name}", "date": camp.date, "time": camp.time, "status": "already_booked"}

    appt = Appointment(user_id=user_id, camp_id=camp.id, appointment_date=camp.date,
                       appointment_time=camp.time, phc_name=camp.location, status="confirmed")
    db.add(appt)
    # Increment registered count
    if camp.registered is not None:
        camp.registered += 1
    db.commit()
    return {"message": f"Appointment confirmed at {camp.name}", "date": camp.date,
            "time": camp.time, "location": camp.location, "status": "confirmed"}

# ── Admin API ──────────────────────────────────────────────────────────────────
@app.get("/api/admin/stats")
async def get_admin_stats(db: Session = Depends(get_db)):
    return {"total_citizens": db.query(User).filter(User.role=="citizen").count(),
            "total_employees": db.query(User).filter(User.role=="employee").count(),
            "pending_approvals": db.query(User).filter(User.role=="employee", User.is_approved==False).count(),
            "total_phcs": db.query(PHC).count(),
            "total_disease_reports": db.query(DiseaseReport).count(),
            "active_alerts": 3, "health_camps": db.query(HealthCamp).count(),
            "high_risk_districts": 2}

@app.get("/api/admin/pending-employees")
async def get_pending_employees(db: Session = Depends(get_db)):
    employees = db.query(User).filter(User.role=="employee", User.is_approved==False).all()
    return [{"id": e.id, "name": e.name, "email": e.email, "phone": e.phone,
             "designation": e.designation, "healthcare_center": e.healthcare_center,
             "district": e.district, "state": e.state,
             "submitted": e.created_at.strftime("%d %b %Y") if e.created_at else "N/A"} for e in employees]

@app.post("/api/admin/approve-employee/{user_id}")
async def approve_employee(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    user.is_approved = True; user.is_verified = True
    db.commit()
    return {"message": "Employee approved successfully"}

@app.post("/api/admin/reject-employee/{user_id}")
async def reject_employee(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user: raise HTTPException(status_code=404, detail="User not found")
    db.delete(user); db.commit()
    return {"message": "Employee rejected"}

@app.get("/api/admin/disease-reports")
async def get_disease_reports(db: Session = Depends(get_db)):
    reports = db.query(DiseaseReport).order_by(DiseaseReport.created_at.desc()).all()
    return [{"id": r.id, "disease": r.disease, "cases": r.cases, "village": r.village,
             "district": r.district, "risk_level": r.risk_level,
             "date": r.created_at.strftime("%d %b %Y") if r.created_at else "N/A"} for r in reports]

@app.get("/api/admin/phcs")
async def get_phcs(db: Session = Depends(get_db)):
    phcs = db.query(PHC).all()
    return [{"id": p.id, "name": p.name, "district": p.district, "state": p.state,
             "village": p.village, "doctors": p.doctors, "nurses": p.nurses,
             "beds": p.beds, "available_beds": p.available_beds,
             "medicine_stock": p.medicine_stock, "health_score": p.health_score,
             "lat": p.lat, "lng": p.lng} for p in phcs]

@app.post("/api/admin/add-disease-report")
async def add_disease_report(disease: str = Form(...), cases: int = Form(...),
    village: str = Form(...), district: str = Form(...), state: str = Form(...),
    db: Session = Depends(get_db)):
    risk = "low"
    if cases >= 20: risk = "critical"
    elif cases >= 15: risk = "high"
    elif cases >= 8: risk = "medium"
    report = DiseaseReport(disease=disease, cases=cases, village=village,
                           district=district, state=state, risk_level=risk, reported_by=1)
    db.add(report); db.commit()
    return {"message": "Disease report added", "risk_level": risk}

# ── Employee API ───────────────────────────────────────────────────────────────
DEFAULT_STOCK = [
    {"medicine": "ORS Packets",      "quantity": 450,  "unit": "packets"},
    {"medicine": "Paracetamol",      "quantity": 1200, "unit": "tablets"},
    {"medicine": "Malaria Kit",      "quantity": 32,   "unit": "kits"},
    {"medicine": "IV Fluids",        "quantity": 80,   "unit": "bottles"},
    {"medicine": "Oxygen Cylinders", "quantity": 6,    "unit": "cylinders"},
    {"medicine": "BP Medicines",     "quantity": 600,  "unit": "tablets"},
    {"medicine": "Antibiotics",      "quantity": 250,  "unit": "strips"},
    {"medicine": "Insulin",          "quantity": 45,   "unit": "vials"},
]

def stock_status(qty):
    if qty >= 200: return "adequate"
    if qty >= 80:  return "moderate"
    if qty >= 30:  return "low"
    return "critical"

@app.get("/api/employee/medicine-stock")
async def get_medicine_stock(db: Session = Depends(get_db)):
    # Get latest record per medicine name
    from sqlalchemy import func
    subq = db.query(MedicineStock.medicine_name,
                    func.max(MedicineStock.updated_at).label("max_t")
                   ).group_by(MedicineStock.medicine_name).subquery()
    stocks = db.query(MedicineStock).join(
        subq, (MedicineStock.medicine_name == subq.c.medicine_name) &
              (MedicineStock.updated_at == subq.c.max_t)
    ).all()

    # Merge DB records with defaults so all medicines always appear
    db_map = {s.medicine_name: s for s in stocks}
    result = []
    for d in DEFAULT_STOCK:
        if d["medicine"] in db_map:
            s = db_map[d["medicine"]]
            result.append({"medicine": s.medicine_name, "quantity": s.quantity,
                          "status": stock_status(s.quantity), "unit": d["unit"]})
        else:
            result.append(dict(**d, status=stock_status(d["quantity"])))
    return result

@app.post("/api/employee/update-stock")
async def update_stock(request: Request, medicine: str = Form(...), quantity: int = Form(...),
    action: str = Form("add"), db: Session = Depends(get_db)):
    token = request.cookies.get("access_token") or request.headers.get("Authorization","").replace("Bearer ","")
    user_id = 3  # fallback to demo employee
    phc_name = "PHC Hanamkonda"
    try:
        user = get_current_user(token, db)
        user_id = user.id
        phc_name = user.healthcare_center or phc_name
    except Exception:
        pass
    
    # Get current stock
    existing = db.query(MedicineStock).filter(
        MedicineStock.medicine_name == medicine,
        MedicineStock.phc_name == phc_name
    ).order_by(MedicineStock.updated_at.desc()).first()
    
    # Get current quantity from existing or default
    current_qty = 0
    if existing:
        current_qty = existing.quantity
    else:
        # Find default quantity for this medicine
        for d in DEFAULT_STOCK:
            if d["medicine"] == medicine:
                current_qty = d["quantity"]
                break
    
    # Calculate new quantity based on action
    if action == "add":
        new_qty = current_qty + quantity
    else:  # "set"
        new_qty = quantity
    
    # Upsert
    if existing:
        existing.quantity = new_qty
        existing.updated_at = datetime.utcnow()
    else:
        stock = MedicineStock(medicine_name=medicine, quantity=new_qty,
                              phc_name=phc_name, updated_by=user_id)
        db.add(stock)
    db.commit()
    
    action_text = "added to" if action == "add" else "set to"
    return {"message": f"✅ {medicine} {action_text} {new_qty} units", "medicine": medicine,
            "quantity": new_qty, "status": stock_status(new_qty)}


# Patient endpoints
@app.get("/api/employee/patients")
async def get_patients(request: Request, db: Session = Depends(get_db)):
    patients = db.query(Patient).order_by(Patient.created_at.desc()).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "age": p.age,
            "gender": p.gender,
            "phone": p.phone,
            "disease": p.disease,
            "medicines": json.loads(p.medicines) if p.medicines else [],
            "phc_name": p.phc_name,
            "village": p.village,
            "district": p.district,
            "state": p.state,
            "prescription_photo": p.prescription_photo,
            "created_at": p.created_at.strftime("%d %b %Y")
        }
        for p in patients
    ]


@app.post("/api/employee/patients")
async def create_patient(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    gender: str = Form(...),
    phone: str = Form(""),
    aadhaar: str = Form(""),
    disease: str = Form(""),
    medicines: str = Form("[]"),
    village: str = Form(""),
    district: str = Form(""),
    state: str = Form(""),
    phc_name: str = Form(""),
    prescription_photo: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    # Handle file upload
    photo_path = None
    if prescription_photo and prescription_photo.filename:
        # Create unique filename
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        ext = prescription_photo.filename.split(".")[-1]
        filename = f"prescription_{timestamp}.{ext}"
        file_path = os.path.join("uploads", filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await prescription_photo.read())
        photo_path = filename

    patient = Patient(
        name=name,
        age=age,
        gender=gender,
        phone=phone,
        aadhaar=aadhaar,
        disease=disease,
        medicines=medicines,
        village=village,
        district=district,
        state=state,
        phc_name=phc_name,
        prescription_photo=photo_path
    )
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return {"message": "✅ Patient created successfully!", "patient_id": patient.id}

@app.post("/api/employee/add-disease-report")
async def employee_add_disease(request: Request, disease: str = Form(...), cases: int = Form(...),
    village: str = Form(...), district: str = Form(...), state: str = Form(...),
    db: Session = Depends(get_db)):
    token = request.cookies.get("access_token") or request.headers.get("Authorization","").replace("Bearer ","")
    user = get_current_user(token, db)
    risk = "low"
    if cases >= 20: risk = "critical"
    elif cases >= 15: risk = "high"
    elif cases >= 8: risk = "medium"
    report = DiseaseReport(disease=disease, cases=cases, village=village,
                           district=district, state=state, risk_level=risk, reported_by=user.id)
    db.add(report); db.commit()
    return {"message": "Disease report submitted", "risk_level": risk}

# ── AI API ─────────────────────────────────────────────────────────────────────
@app.get("/api/ai/outbreak-prediction")
async def outbreak_prediction(db: Session = Depends(get_db)):
    reports = db.query(DiseaseReport).all()
    return predict_disease_outbreak(reports)

@app.get("/api/ai/demand-forecast")
async def demand_forecast():
    return forecast_demand()

@app.get("/api/ai/recommendations")
async def ai_recommendations():
    return get_ai_recommendations()

@app.post("/api/ai/simulate")
async def simulate(scenario: str = Form(...)):
    return simulate_scenario(scenario)

@app.get("/api/ai/digital-twin/{phc_id}")
async def digital_twin(phc_id: int, db: Session = Depends(get_db)):
    phc = db.query(PHC).filter(PHC.id == phc_id).first()
    if not phc: raise HTTPException(status_code=404, detail="PHC not found")
    return get_digital_twin_data(phc)

@app.get("/api/ai/chatbot")
async def chatbot(q: str = "", role: str = "citizen"):
    responses = {
        "diabetes": "Your next diabetes checkup is due. A free screening camp is available at PHC Hanamkonda on 15 July from 10AM-3PM. Book now!",
        "checkup": "Your next checkup: PHC Hanamkonda on 15 July 2024, 10:00 AM - 2:00 PM. Click Book Appointment.",
        "camp": "Upcoming camps: 1) Diabetes Screening - PHC Hanamkonda (15 Jul) | 2) Eye Checkup - Warangal (18 Jul) | 3) Women Health - PHC Kazipet (20 Jul)",
        "medicine": "Based on current trends, ORS and Malaria kits may run low in 3 days at PHC Kazipet. Restock recommended.",
        "outbreak": "🔴 High Risk: Malaria outbreak predicted in Kazipet (78% confidence). Dengue moderate risk in Narsampet. AI recommends deploying rapid response team.",
        "phc": "Nearest PHC: PHC Hanamkonda (2.3 km) | Available doctors: 3 | Beds: 12/30 available | Today: 8AM-6PM",
        "blood pressure": "Last BP reading: 120/80 (Normal ✅). Next BP check recommended within 3 months.",
        "appointment": "Book appointment at PHC Hanamkonda. Click Book Appointment button or call 9000-111-222.",
        "score": "Your Health Score: 78/100 (Good 🟢). Main factors: Diabetes managed, BP controlled. Next checkup needed.",
    }
    q_lower = q.lower()
    for key, response in responses.items():
        if key in q_lower:
            return {"response": response, "confidence": 0.92}
    if role == "admin":
        return {"response": "Top risk districts: Warangal (Malaria 78%), Nalgonda (Dengue 62%), Karimnagar (Cholera 45%). Recommend deploying 3 rapid response teams immediately.", "confidence": 0.88}
    if role == "employee":
        return {"response": "Medicine alert: ORS at 45% (reorder in 2 days), Malaria kits at 30% (critical). Patient load forecast: +18% tomorrow due to weather. AI recommends requesting transfer from PHC Hanamkonda.", "confidence": 0.91}
    return {"response": "👋 Hello! I'm your HealthPulse AI Assistant. Ask me about checkups, nearby health camps, medicine availability, disease outbreaks, or your health score!", "confidence": 1.0}

@app.get("/api/charts/disease-trend")
async def disease_trend():
    return {"labels": ["Jan","Feb","Mar","Apr","May","Jun","Jul"],
            "datasets": [
                {"label": "Malaria", "data": [12,19,15,28,35,42,38], "color": "#ef4444"},
                {"label": "Dengue", "data": [5,8,12,18,22,28,25], "color": "#f97316"},
                {"label": "Diarrhea", "data": [25,32,28,35,30,22,18], "color": "#3b82f6"},
                {"label": "Typhoid", "data": [8,12,10,14,11,9,7], "color": "#8b5cf6"},
            ]}

@app.get("/api/charts/resource-forecast")
async def resource_forecast():
    return {"labels": ["Day 1","Day 2","Day 3","Day 4","Day 5","Day 6","Day 7"],
            "predicted_patients": [145,168,192,178,205,188,215],
            "bed_demand": [28,32,38,35,42,39,45],
            "medicine_demand": [320,380,420,390,460,435,490]}

@app.get("/api/map/phc-locations")
async def phc_map_locations(db: Session = Depends(get_db)):
    # Merge DB PHCs with static India-wide PHC data
    db_phcs = db.query(PHC).all()
    db_names = {p.name for p in db_phcs}
    result = []
    for p in db_phcs:
        risk = "critical" if p.health_score < 30 else ("high" if p.health_score < 50 else ("medium" if p.health_score < 75 else "good"))
        result.append({"id": p.id, "name": p.name, "lat": p.lat, "lng": p.lng,
                       "health_score": p.health_score, "district": p.district,
                       "state": p.state, "doctors": p.doctors, "beds": p.beds,
                       "available_beds": p.available_beds, "medicine_stock": p.medicine_stock, "risk": risk})
    # Add static India-wide PHCs not already in DB
    for i, p in enumerate(INDIA_PHC_LOCATIONS):
        if p["name"] not in db_names:
            risk = "critical" if p["health_score"] < 30 else ("high" if p["health_score"] < 50 else ("medium" if p["health_score"] < 75 else "good"))
            result.append({"id": 1000+i, "name": p["name"], "lat": p["lat"], "lng": p["lng"],
                           "health_score": p["health_score"], "district": p["district"],
                           "state": p["state"], "doctors": p["doctors"], "beds": p["beds"],
                           "available_beds": p["available_beds"], "medicine_stock": p["medicine_stock"],
                           "risk": risk})
    return result

@app.get("/api/india/states")
async def get_states():
    return sorted(INDIA_STATES.keys())

@app.get("/api/india/cities/{state}")
async def get_cities(state: str):
    cities = INDIA_STATES.get(state, [])
    return sorted(cities)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
