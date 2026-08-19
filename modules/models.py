from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class UserProfile(BaseModel):
    """Pydantic V2 Data Contract for User Profiles."""
    id: str = Field(default="default_user", description="Unique user identifier")
    name: str = Field(default="Pengguna Utama", description="Full name of applicant")
    gpa: float = Field(default=3.50, ge=0.0, le=4.0, description="Current GPA")
    ielts_score: float = Field(default=6.5, ge=0.0, le=9.0, description="Current IELTS score")
    toefl_ibt_score: float = Field(default=80.0, ge=0.0, le=120.0, description="Current TOEFL iBT score")
    age: int = Field(default=24, ge=15, le=100, description="Applicant age in years")
    target_degree: str = Field(default="S2", description="Target academic degree: S1, S2, or S3")
    major_field: str = Field(default="Ilmu Komputer", description="Target field of study")
    work_exp_years: int = Field(default=2, ge=0, description="Years of work experience")
    publications_count: int = Field(default=0, ge=0, description="Number of research publications")
    target_countries: List[str] = Field(default_factory=lambda: ["UK", "Europe"], description="List of target countries")
    created_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


class Scholarship(BaseModel):
    """Pydantic V2 Data Contract for Master Scholarship Repository."""
    id: str = Field(description="Unique scholarship slug/identifier")
    name: str = Field(description="Official scholarship name")
    provider: str = Field(description="Organizing foundation / government ministry")
    funding_type: str = Field(default="Fully Funded", description="Fully Funded or Partial Funded")
    target_degrees: List[str] = Field(default_factory=list, description="Supported degrees e.g. ['S1', 'S2']")
    target_countries: List[str] = Field(default_factory=list, description="Eligible target countries")
    min_gpa: float = Field(default=3.0, description="Minimum GPA requirement")
    min_ielts: float = Field(default=6.0, description="Minimum IELTS requirement")
    min_toefl_ibt: float = Field(default=75.0, description="Minimum TOEFL iBT requirement")
    max_age: int = Field(default=35, description="Maximum age limit")
    min_work_exp_years: int = Field(default=0, description="Minimum work experience required")
    required_documents: List[str] = Field(default_factory=list, description="List of required application documents")
    deadline_date: str = Field(default="2026-12-31", description="Application deadline ISO date")
    source_url: str = Field(default="", description="Official portal URL")
    description: str = Field(default="", description="Scholarship summary description")


class UserScholarshipFlag(BaseModel):
    """Pydantic V2 Data Contract for Isolated User Interaction Flags (Bookmarks, Status & Notes)."""
    user_id: str = Field(description="Foreign key to user_profiles.id")
    scholarship_id: str = Field(description="Foreign key to scholarships.id")
    is_bookmarked: bool = Field(default=False, description="User star/bookmark flag")
    priority: str = Field(default="NONE", description="Priority level: HIGH, MED, LOW, NONE")
    status: str = Field(default="SAVED", description="Application status: SAVED, DRAFTING, APPLIED, ACCEPTED, REJECTED")
    user_notes: str = Field(default="", description="Personal user notes and reminders")
    updated_at: Optional[str] = Field(default_factory=lambda: datetime.now().isoformat())


class MatchResult(BaseModel):
    """Pydantic V2 Data Contract for Fit Score Calculations."""
    scholarship_id: str
    scholarship_name: str
    provider: str
    funding_type: str
    fit_score: float
    category: str  # Safety, Target, Reach
    badge: str
    quadrant: str
    is_qualified: bool
    status_label: str
    missing_requirements: List[str] = Field(default_factory=list)
    flag_status: Optional[UserScholarshipFlag] = None
