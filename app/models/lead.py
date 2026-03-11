from enum import Enum
from datetime import datetime
from typing import Optional, List


class LeadStatus(str, Enum):
    PENDING = "pending"
    RESEARCHING = "researching"
    DRAFT_READY = "draft_ready"
    APPROVED = "approved"
    SENT = "sent"
    REJECTED = "rejected"


class ResearchData:
    def __init__(
        self,
        company_description: Optional[str] = None,
        recent_news: Optional[List[str]] = None,
        pain_points: Optional[List[str]] = None,
        key_insights: Optional[str] = None,
        scraped_at: Optional[datetime] = None
    ):
        self.company_description = company_description
        self.recent_news = recent_news or []
        self.pain_points = pain_points or []
        self.key_insights = key_insights
        self.scraped_at = scraped_at
    
    def to_dict(self):
        return {
            "company_description": self.company_description,
            "recent_news": self.recent_news,
            "pain_points": self.pain_points,
            "key_insights": self.key_insights,
            "scraped_at": self.scraped_at
        }


class EmailDraft:
    def __init__(
        self,
        subject: str,
        body: str,
        version: int = 1,
        generated_at: Optional[datetime] = None
    ):
        self.subject = subject
        self.body = body
        self.version = version
        self.generated_at = generated_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            "subject": self.subject,
            "body": self.body,
            "version": self.version,
            "generated_at": self.generated_at
        }


class Lead:
    """Lead model for MongoDB"""
    
    def __init__(
        self,
        company_name: str,
        user_id: str,
        website: Optional[str] = None,
        industry: Optional[str] = None,
        contact_person: Optional[str] = None,
        contact_email: Optional[str] = None,
        phone: Optional[str] = None,
        status: LeadStatus = LeadStatus.PENDING,
        research_data: Optional[ResearchData] = None,
        email_drafts: Optional[List[EmailDraft]] = None,
        approved_draft: Optional[EmailDraft] = None,
        notes: Optional[str] = None,
        _id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self._id = _id
        self.company_name = company_name
        self.user_id = user_id
        self.website = website
        self.industry = industry
        self.contact_person = contact_person
        self.contact_email = contact_email
        self.phone = phone
        self.status = status
        self.research_data = research_data
        self.email_drafts = email_drafts or []
        self.approved_draft = approved_draft
        self.notes = notes
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            "_id": self._id,
            "company_name": self.company_name,
            "user_id": self.user_id,
            "website": self.website,
            "industry": self.industry,
            "contact_person": self.contact_person,
            "contact_email": self.contact_email,
            "phone": self.phone,
            "status": self.status,
            "research_data": self.research_data.to_dict() if self.research_data else None,
            "email_drafts": [draft.to_dict() for draft in self.email_drafts],
            "approved_draft": self.approved_draft.to_dict() if self.approved_draft else None,
            "notes": self.notes,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @staticmethod
    def from_dict(data: dict):
        research_data = None
        if data.get("research_data"):
            rd = data["research_data"]
            research_data = ResearchData(
                company_description=rd.get("company_description"),
                recent_news=rd.get("recent_news", []),
                pain_points=rd.get("pain_points", []),
                key_insights=rd.get("key_insights"),
                scraped_at=rd.get("scraped_at")
            )
        
        email_drafts = []
        for draft in data.get("email_drafts", []):
            email_drafts.append(EmailDraft(
                subject=draft["subject"],
                body=draft["body"],
                version=draft.get("version", 1),
                generated_at=draft.get("generated_at")
            ))
        
        approved_draft = None
        if data.get("approved_draft"):
            ad = data["approved_draft"]
            approved_draft = EmailDraft(
                subject=ad["subject"],
                body=ad["body"],
                version=ad.get("version", 1),
                generated_at=ad.get("generated_at")
            )
        
        return Lead(
            _id=str(data.get("_id")),
            company_name=data["company_name"],
            user_id=data["user_id"],
            website=data.get("website"),
            industry=data.get("industry"),
            contact_person=data.get("contact_person"),
            contact_email=data.get("contact_email"),
            phone=data.get("phone"),
            status=data.get("status", LeadStatus.PENDING),
            research_data=research_data,
            email_drafts=email_drafts,
            approved_draft=approved_draft,
            notes=data.get("notes"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )
