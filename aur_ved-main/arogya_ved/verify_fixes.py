import requests

B = "http://localhost:8000"
print("=" * 52)
print("  Verifying: Name change + Booking fix")
print("=" * 52)

# 1. Employee name
r = requests.post(f"{B}/api/auth/login",
    data={"email": "priya@phc.gov.in", "password": "Employee@123"})
d = r.json()
name = d.get("name", "unknown")
ok = "OK " if "Goyanshi" in name else "FAIL"
print(f"\n[NAME CHANGE]")
print(f"  {ok}  Employee login name: '{name}'")

# 2. Booking a camp
camps = requests.get(f"{B}/api/citizen/camps").json()
cid = camps[0]["id"]
cname = camps[0]["name"]
print(f"\n[BOOKING]")
print(f"  Camp: '{cname}' (id={cid})")

r1 = requests.post(f"{B}/api/citizen/book-appointment", data={"camp_id": cid})
d1 = r1.json()
ok1 = "OK " if r1.status_code == 200 else "FAIL"
print(f"  {ok1}  First booking  -> status='{d1.get('status')}' | {d1.get('message')}")
print(f"       Date: {d1.get('date')}  |  Time: {d1.get('time')}")

# 3. Duplicate booking guard
r2 = requests.post(f"{B}/api/citizen/book-appointment", data={"camp_id": cid})
d2 = r2.json()
ok2 = "OK " if d2.get("status") == "already_booked" else "FAIL"
print(f"  {ok2}  Duplicate guard -> status='{d2.get('status')}'")

print("\n" + "=" * 52)
print(f"  Open: http://localhost:8000/login")
print(f"  Employee: priya@phc.gov.in / Employee@123")
print("=" * 52)
