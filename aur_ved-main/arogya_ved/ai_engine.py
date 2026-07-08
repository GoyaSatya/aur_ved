"""
HealthPulse AI Engine
Mock AI models with realistic outputs — replaceable with real ML models.
"""
import random
from datetime import datetime, timedelta


def predict_disease_outbreak(reports):
    """Disease Ripple Prediction AI"""
    disease_map = {}
    for r in reports:
        d = r.disease
        if d not in disease_map:
            disease_map[d] = {"cases": 0, "villages": [], "districts": set()}
        disease_map[d]["cases"] += r.cases
        disease_map[d]["villages"].append(r.village)
        disease_map[d]["districts"].add(r.district)

    predictions = []
    for disease, data in disease_map.items():
        risk = "low"
        prob = 0.2
        if data["cases"] >= 20:
            risk = "critical"
            prob = 0.92
        elif data["cases"] >= 15:
            risk = "high"
            prob = 0.78
        elif data["cases"] >= 8:
            risk = "medium"
            prob = 0.55
        else:
            risk = "low"
            prob = 0.25

        predictions.append({
            "disease": disease,
            "total_cases": data["cases"],
            "affected_villages": data["villages"],
            "affected_districts": list(data["districts"]),
            "risk_level": risk,
            "outbreak_probability": round(prob, 2),
            "predicted_cases_7d": int(data["cases"] * 1.8),
            "estimated_medicine_demand": int(data["cases"] * 12),
            "estimated_beds": max(5, int(data["cases"] * 0.4)),
            "estimated_doctors": max(1, int(data["cases"] * 0.08)),
            "confidence": round(random.uniform(0.82, 0.96), 2),
            "explanation": _generate_explanation(disease, data["cases"], risk),
            "days_to_peak": random.randint(3, 8)
        })

    return {
        "predictions": predictions,
        "overall_risk": "high" if any(p["risk_level"] in ["high","critical"] for p in predictions) else "medium",
        "generated_at": datetime.now().isoformat(),
        "model": "HealthPulse Disease Ripple Predictor v2.1"
    }


def _generate_explanation(disease, cases, risk):
    reasons = {
        "Malaria": [
            "Rainfall increased by 42% — mosquito breeding conditions favorable",
            "Humidity above 85% — high vector activity",
            f"{cases} cases reported across multiple villages",
            "Historical July trend shows 35% increase",
            "3 nearby PHCs reported malaria cases"
        ],
        "Dengue": [
            "Stagnant water sources identified in affected areas",
            f"{cases} confirmed cases — spread pattern detected",
            "Temperature range optimal for Aedes mosquito activity",
            "Low vector control coverage in rural areas"
        ],
        "Diarrhea": [
            "Water quality testing shows contamination risk",
            f"{cases} cases clustered in 2-3 villages — possible common source",
            "Monsoon season increases waterborne disease risk",
            "Sanitation infrastructure gaps identified"
        ],
        "Typhoid": [
            f"{cases} cases reported — fecal-oral transmission suspected",
            "Water supply contamination possible",
            "Low vaccination coverage in affected villages"
        ]
    }
    default_reasons = [
        f"{cases} active cases detected",
        "Seasonal pattern matches historical outbreak data",
        "Geographic clustering suggests community spread",
        "Environmental conditions conducive to spread"
    ]
    r = reasons.get(disease, default_reasons)
    return r


def forecast_demand():
    """Human Behavior & Demand Forecast AI"""
    today = datetime.now()
    forecast = []
    base_patients = 145
    for i in range(7):
        day = today + timedelta(days=i)
        # Simulate rainfall effect
        rainfall_factor = random.uniform(0.9, 1.4)
        festival_factor = 1.0
        if day.weekday() in [5, 6]:  # Weekend
            festival_factor = 1.15

        patients = int(base_patients * rainfall_factor * festival_factor)
        forecast.append({
            "date": day.strftime("%d %b"),
            "day": day.strftime("%A"),
            "predicted_patients": patients,
            "bed_demand": int(patients * 0.22),
            "ors_demand": int(patients * 2.1),
            "malaria_kit_demand": int(patients * 0.08),
            "iv_fluid_demand": int(patients * 0.15),
            "doctor_requirement": max(3, int(patients * 0.025)),
            "ambulance_demand": max(1, int(patients * 0.008)),
            "confidence": round(random.uniform(0.80, 0.95), 2)
        })
        base_patients = int(base_patients * random.uniform(0.95, 1.12))

    return {
        "forecast": forecast,
        "inputs": {
            "weather": "Monsoon - Heavy Rain Expected",
            "festival": "No major festival next 7 days",
            "season": "Monsoon Season",
            "risk_factors": ["High humidity", "Stagnant water", "Low-lying areas"]
        },
        "top_alerts": [
            {"type": "warning", "message": "ORS stock may run out in 4 days at PHC Kazipet"},
            {"type": "info", "message": "Malaria kit demand expected to rise 35% due to rainfall"},
            {"type": "alert", "message": "Doctor shortage predicted at PHC Narsampet on Day 5"}
        ],
        "model": "HealthPulse Behavior Engine v1.8"
    }


def get_health_score(phc):
    """Calculate AI Health Readiness Score"""
    score = 0
    factors = {}

    # Medicine availability (25 pts)
    med_score = min(25, int(phc.medicine_stock * 0.25))
    factors["medicine_availability"] = med_score
    score += med_score

    # Doctor availability (20 pts)
    doc_score = min(20, phc.doctors * 5)
    factors["doctor_availability"] = doc_score
    score += doc_score

    # Bed occupancy (20 pts)
    if phc.beds > 0:
        occupancy_rate = (phc.beds - phc.available_beds) / phc.beds
        bed_score = int(20 * (1 - occupancy_rate))
    else:
        bed_score = 10
    factors["bed_availability"] = bed_score
    score += bed_score

    # Emergency preparedness (20 pts)
    emergency_score = min(20, phc.ambulances * 8 + phc.oxygen_cylinders // 2)
    factors["emergency_preparedness"] = emergency_score
    score += emergency_score

    # Nurse coverage (15 pts)
    nurse_score = min(15, phc.nurses * 2)
    factors["nurse_coverage"] = nurse_score
    score += nurse_score

    score = min(100, score)

    if score >= 90:
        category = "Excellent"
        color = "green"
        emoji = "🟢"
    elif score >= 75:
        category = "Good"
        color = "green"
        emoji = "🟢"
    elif score >= 50:
        category = "Moderate Risk"
        color = "yellow"
        emoji = "🟡"
    elif score >= 30:
        category = "High Risk"
        color = "orange"
        emoji = "🟠"
    else:
        category = "Critical"
        color = "red"
        emoji = "🔴"

    return {
        "phc_name": phc.name,
        "score": score,
        "category": category,
        "color": color,
        "emoji": emoji,
        "factors": factors,
        "recommendations": _get_score_recommendations(factors, score)
    }


def _get_score_recommendations(factors, score):
    recs = []
    if factors.get("medicine_availability", 0) < 15:
        recs.append("🔴 Restock medicine supply — currently below 60%")
    if factors.get("doctor_availability", 0) < 10:
        recs.append("🟠 Request additional doctors from CHC")
    if factors.get("bed_availability", 0) < 10:
        recs.append("🟡 Arrange temporary bed expansion")
    if factors.get("emergency_preparedness", 0) < 10:
        recs.append("🔴 Oxygen cylinders critically low — immediate refill needed")
    if score < 50:
        recs.append("🔴 URGENT: Health Readiness Score critical — district officer notified")
    return recs if recs else ["✅ All systems performing well. Maintain current standards."]


def get_ai_recommendations():
    """Resource redistribution recommendations"""
    return {
        "recommendations": [
            {
                "id": 1,
                "type": "transfer",
                "priority": "critical",
                "title": "Transfer ORS Packets",
                "description": "PHC Hanamkonda has surplus 600 ORS. PHC Kazipet is critically low.",
                "from": "PHC Hanamkonda",
                "to": "PHC Kazipet",
                "items": "600 ORS packets",
                "estimated_time": "45 minutes",
                "confidence": 0.94,
                "impact": "Prevents shortage for ~300 patients",
                "lives_benefited": 300,
                "estimated_cost": 1200
            },
            {
                "id": 2,
                "type": "staff",
                "priority": "high",
                "title": "Deploy Additional Doctor",
                "description": "High patient load expected at PHC Narsampet due to weather forecast.",
                "from": "CHC Warangal",
                "to": "PHC Narsampet",
                "items": "2 Doctors + 1 Nurse",
                "estimated_time": "2 hours",
                "confidence": 0.87,
                "impact": "Reduces patient wait time by 60%",
                "lives_benefited": 150,
                "estimated_cost": 0
            },
            {
                "id": 3,
                "type": "camp",
                "priority": "medium",
                "title": "Organize Malaria Camp",
                "description": "AI predicts malaria surge in next 5 days in Kazipet area.",
                "location": "PHC Kazipet & nearby villages",
                "items": "50 Malaria Kits + 200 Nets + 2 Doctors",
                "estimated_time": "Schedule within 48 hours",
                "confidence": 0.91,
                "impact": "Early detection — prevents 85% spread",
                "lives_benefited": 500,
                "estimated_cost": 8500
            }
        ],
        "generated_at": datetime.now().isoformat()
    }


def simulate_scenario(scenario: str):
    """AI Scenario Simulation"""
    scenarios = {
        "rainfall": {
            "scenario": "Heavy Rainfall (7 Days)",
            "predictions": {
                "malaria_increase": "↑ 68%",
                "dengue_increase": "↑ 42%",
                "diarrhea_increase": "↑ 35%",
                "patient_surge": "↑ 85 additional patients/day",
                "ors_demand": "↑ 320 packets extra",
                "malaria_kit_demand": "↑ 45 kits",
                "bed_demand": "↑ 18 extra beds",
                "doctor_requirement": "↑ 3 additional doctors",
                "ambulance_demand": "↑ 2 additional"
            },
            "confidence": 0.89,
            "alert_level": "High",
            "recommended_actions": [
                "Pre-position 500 ORS packets at PHC Kazipet",
                "Distribute 200 mosquito nets to high-risk villages",
                "Arrange 2 extra doctors from CHC Warangal",
                "Activate vector control spraying in affected areas",
                "Alert district medical officer"
            ]
        },
        "heatwave": {
            "scenario": "Heatwave Alert (5 Days)",
            "predictions": {
                "dehydration_cases": "↑ 120%",
                "heat_stroke": "↑ 85 cases expected",
                "ors_demand": "↑ 450 packets",
                "iv_fluid_demand": "↑ 60 bottles",
                "emergency_beds": "↑ 25 extra needed",
                "patient_surge": "↑ 120 additional patients/day"
            },
            "confidence": 0.93,
            "alert_level": "Critical",
            "recommended_actions": [
                "Pre-stock 500 ORS packets at all PHCs",
                "Arrange 60 IV fluid bottles across 3 PHCs",
                "Set up cooling centers at PHCs",
                "Deploy mobile health vans",
                "Issue public heat advisory"
            ]
        },
        "festival": {
            "scenario": "Major Festival/Event",
            "predictions": {
                "road_accidents": "↑ 45%",
                "trauma_cases": "↑ 30 cases",
                "blood_demand": "↑ 15 units",
                "emergency_beds": "↑ 20 extra",
                "ambulance_demand": "↑ 4 additional"
            },
            "confidence": 0.85,
            "alert_level": "High",
            "recommended_actions": [
                "Deploy 4 ambulances on festival routes",
                "Stock trauma kits at roadside PHCs",
                "Coordinate blood bank reserves",
                "Activate emergency response teams",
                "Coordinate with traffic police"
            ]
        },
        "outbreak": {
            "scenario": "Disease Outbreak Response",
            "predictions": {
                "spread_villages": "12 villages at risk",
                "expected_patients": "340 cases in 7 days",
                "isolation_beds_needed": 45,
                "medicine_requirement": "Antibiotics x2000, ORS x800",
                "staff_requirement": "8 additional health workers"
            },
            "confidence": 0.91,
            "alert_level": "Critical",
            "recommended_actions": [
                "Declare local health emergency",
                "Deploy rapid response team immediately",
                "Set up isolation ward at CHC",
                "Initiate contact tracing",
                "Stock targeted medicines at all PHCs"
            ]
        }
    }
    result = scenarios.get(scenario.lower(), scenarios["rainfall"])
    result["simulated_at"] = datetime.now().isoformat()
    return result


def get_digital_twin_data(phc):
    """Digital Twin - Live Virtual Representation"""
    current_patients = random.randint(25, 65)
    waiting = random.randint(5, 20)

    return {
        "phc": {
            "id": phc.id,
            "name": phc.name,
            "district": phc.district,
            "health_score": phc.health_score
        },
        "current_status": {
            "patients_today": current_patients,
            "patients_waiting": waiting,
            "avg_wait_time": f"{random.randint(12, 35)} min",
            "doctors_available": phc.doctors,
            "nurses_available": phc.nurses,
            "beds_total": phc.beds,
            "beds_available": phc.available_beds,
            "icu_beds": phc.icu_beds or 0,
            "oxygen_cylinders": phc.oxygen_cylinders or 10,
            "ambulances": phc.ambulances or 1,
            "medicine_stock_pct": phc.medicine_stock,
            "lab_capacity_used": random.randint(40, 80),
        },
        "predictions": {
            "next_24h": {
                "expected_patients": int(current_patients * 1.15),
                "medicine_shortage_risk": "Low",
                "bed_shortage_risk": "Medium" if phc.available_beds < 8 else "Low",
                "confidence": 0.91
            },
            "next_3d": {
                "expected_patients": int(current_patients * 1.35),
                "medicine_shortage_risk": "Medium",
                "bed_shortage_risk": "High" if phc.available_beds < 8 else "Medium",
                "confidence": 0.85
            },
            "next_7d": {
                "expected_patients": int(current_patients * 1.65),
                "medicine_shortage_risk": "High",
                "bed_shortage_risk": "High",
                "confidence": 0.78
            }
        },
        "alerts": [
            {"level": "warning", "message": "Malaria kit stock below 30%"},
            {"level": "info", "message": "Doctor attendance 100% today"},
            {"level": "critical", "message": "Oxygen cylinder restock needed within 48h"}
            if (phc.oxygen_cylinders or 10) < 8 else
            {"level": "info", "message": "All resources adequate for next 24h"}
        ],
        "updated_at": datetime.now().isoformat()
    }
