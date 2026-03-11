from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from bson import ObjectId
from datetime import datetime
from app.schemas.lead import LeadCreate, LeadResponse, LeadUpdate
from app.schemas.user import UserResponse
from app.utils.dependencies import get_current_active_user
from app.database import get_database

router = APIRouter(prefix="/api/leads", tags=["Leads"])


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    lead_data: LeadCreate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Create a new lead"""
    db = get_database()
    
    lead_doc = {
        "_id": ObjectId(),
        **lead_data.model_dump(),
        "user_id": current_user.id,
        "status": "pending",
        "research_data": None,
        "email_drafts": [],
        "approved_draft": None,
        "notes": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    await db.leads.insert_one(lead_doc)
    
    return LeadResponse(
        id=str(lead_doc["_id"]),
        user_id=lead_doc["user_id"],
        **lead_data.model_dump(),
        status=lead_doc["status"],
        created_at=lead_doc["created_at"],
        updated_at=lead_doc["updated_at"]
    )


@router.get("/", response_model=List[LeadResponse])
async def get_leads(
    skip: int = 0,
    limit: int = 50,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get all leads for current user"""
    db = get_database()
    
    cursor = db.leads.find({"user_id": current_user.id}).skip(skip).limit(limit)
    leads = await cursor.to_list(length=limit)
    
    return [
        LeadResponse(
            id=str(lead["_id"]),
            user_id=lead["user_id"],
            company_name=lead["company_name"],
            website=lead.get("website"),
            industry=lead.get("industry"),
            contact_person=lead.get("contact_person"),
            contact_email=lead.get("contact_email"),
            phone=lead.get("phone"),
            status=lead["status"],
            research_data=lead.get("research_data"),
            email_drafts=lead.get("email_drafts", []),
            approved_draft=lead.get("approved_draft"),
            created_at=lead["created_at"],
            updated_at=lead["updated_at"],
            notes=lead.get("notes")
        )
        for lead in leads
    ]


@router.get("/{lead_id}", response_model=LeadResponse)
async def get_lead(
    lead_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Get a specific lead"""
    db = get_database()
    
    lead = await db.leads.find_one({"_id": ObjectId(lead_id), "user_id": current_user.id})
    
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return LeadResponse(
        id=str(lead["_id"]),
        user_id=lead["user_id"],
        company_name=lead["company_name"],
        website=lead.get("website"),
        industry=lead.get("industry"),
        contact_person=lead.get("contact_person"),
        contact_email=lead.get("contact_email"),
        phone=lead.get("phone"),
        status=lead["status"],
        research_data=lead.get("research_data"),
        email_drafts=lead.get("email_drafts", []),
        approved_draft=lead.get("approved_draft"),
        created_at=lead["created_at"],
        updated_at=lead["updated_at"],
        notes=lead.get("notes")
    )


@router.patch("/{lead_id}", response_model=LeadResponse)
async def update_lead(
    lead_id: str,
    lead_update: LeadUpdate,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Update a lead"""
    db = get_database()
    
    update_data = {k: v for k, v in lead_update.model_dump(exclude_unset=True).items() if v is not None}
    update_data["updated_at"] = datetime.utcnow()
    
    result = await db.leads.update_one(
        {"_id": ObjectId(lead_id), "user_id": current_user.id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    updated_lead = await db.leads.find_one({"_id": ObjectId(lead_id)})
    
    return LeadResponse(
        id=str(updated_lead["_id"]),
        user_id=updated_lead["user_id"],
        company_name=updated_lead["company_name"],
        website=updated_lead.get("website"),
        industry=updated_lead.get("industry"),
        contact_person=updated_lead.get("contact_person"),
        contact_email=updated_lead.get("contact_email"),
        phone=updated_lead.get("phone"),
        status=updated_lead["status"],
        research_data=updated_lead.get("research_data"),
        email_drafts=updated_lead.get("email_drafts", []),
        approved_draft=updated_lead.get("approved_draft"),
        created_at=updated_lead["created_at"],
        updated_at=updated_lead["updated_at"],
        notes=updated_lead.get("notes")
    )


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lead(
    lead_id: str,
    current_user: UserResponse = Depends(get_current_active_user)
):
    """Delete a lead"""
    db = get_database()
    
    result = await db.leads.delete_one({"_id": ObjectId(lead_id), "user_id": current_user.id})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    return None