from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.models.lead import LeadStatus


class ResearchDataSchema(BaseModel):
    company_description: Optional[str] = None
    recent_news: Optional[List[str]] = None
    pain_points: Optional[List[str]] = None
    key_insights: Optional[str] = None
    scraped_at: Optional[datetime] = None


class EmailDraftSchema(BaseModel):
    subject: str
    body: str
    version: int = 1
    generated_at: datetime


class LeadBase(BaseModel):
    company_name: str
    website: Optional[str] = None
    industry: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone: Optional[str] = None


class LeadCreate(LeadBase):
    pass


class LeadUpdate(BaseModel):
    company_name: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[LeadStatus] = None
    notes: Optional[str] = None


class LeadResponse(LeadBase):
    id: str
    user_id: str
    status: LeadStatus
    research_data: Optional[ResearchDataSchema] = None
    email_drafts: List[EmailDraftSchema] = []
    approved_draft: Optional[EmailDraftSchema] = None
    created_at: datetime
    updated_at: datetime
    notes: Optional[str] = None

    class Config:
        from_attributes = True
