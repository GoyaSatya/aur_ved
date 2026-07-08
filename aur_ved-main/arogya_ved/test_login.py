import requests

print("=" * 55)
print("  HealthPulse AI - Full System Test")
print("=" * 55)

base = "http://localhost:8000"

# Test pages
pages = [
    ("Landing Page",          "/"),
    ("Login Page",            "/login"),
    ("Register Page",         "/register"),
    ("Employee Register",     "/register/employee"),
    ("Citizen Dashboard",     "/citizen/dashboard"),
    ("Admin Dashboard",       "/admin/dashboard"),
    ("Employee Dashboard",    "/employee/dashboard"),
]
print("\n[PAGES]")
for name, path in pages:
    r = requests.get(base + path, timeout=5)
    icon = "OK " if r.status_code == 200 else "ERR"
    print(f"  {icon}  [{r.status_code}]  {name}")

# Test login
print("\n[LOGIN]")
accounts = [
    ("admin@healthpulse.gov.in", "Admin@123",    "admin"),
    ("satya@example.com",        "Citizen@123",  "citizen"),
    ("priya@phc.gov.in",         "Employee@123", "employee"),
]
for email, pwd, role in accounts:
    r = requests.post(base + "/api/auth/login", data={"email": email, "password": pwd}, timeout=5)
    d = r.json()
    if r.status_code == 200:
        print(f"  OK   {role:10s}  {d['name']:20s}  -> {d['redirect']}")
    else:
        print(f"  FAIL {role}: {d.get('detail')}")

# Test APIs
print("\n[APIs]")
apis = [
    ("Admin Stats",        "/api/admin/stats"),
    ("PHC List",           "/api/admin/phcs"),
    ("Health Camps",       "/api/citizen/camps"),
    ("Disease Reports",    "/api/admin/disease-reports"),
    ("Outbreak AI",        "/api/ai/outbreak-prediction"),
    ("Demand Forecast AI", "/api/ai/demand-forecast"),
    ("AI Recommendations", "/api/ai/recommendations"),
    ("AI Chatbot",         "/api/ai/chatbot?q=diabetes&role=citizen"),
    ("Digital Twin",       "/api/ai/digital-twin/1"),
    ("PHC Map Data",       "/api/map/phc-locations"),
    ("Disease Chart",      "/api/charts/disease-trend"),
    ("Resource Chart",     "/api/charts/resource-forecast"),
]
for name, path in apis:
    r = requests.get(base + path, timeout=5)
    icon = "OK " if r.status_code == 200 else "ERR"
    print(f"  {icon}  [{r.status_code}]  {name}")

print("\n" + "=" * 55)
print("  Server running at: http://localhost:8000")
print("=" * 55)
