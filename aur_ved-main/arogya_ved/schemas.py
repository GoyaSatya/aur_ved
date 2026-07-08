from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class UserCreate(BaseModel):
    name: str
    email: str
    phone: str
    password: str
    role: str = "citizen"
    age: Optional[int] = None
    gender: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    village: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class DiseaseReportCreate(BaseModel):
    disease: str
    cases: int
    village: str
    district: str
    state: str
    notes: Optional[str] = None


class MedicineStockUpdate(BaseModel):
    medicine_name: str
    quantity: int
    phc_name: str
