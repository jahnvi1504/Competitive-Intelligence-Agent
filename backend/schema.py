from typing import Generic, TypeVar, Optional, List, Any, Dict
from pydantic import BaseModel, Field

T = TypeVar('T')

class SchemaField(BaseModel, Generic[T]):
    value: Optional[T] = None
    confidence: str = "unverified"  # "high" | "medium" | "low" | "unverified"
    source_url: Optional[str] = None
    access_date: Optional[str] = None
    conflict: bool = False
    conflicting_value: Optional[Any] = None
    conflicting_source_url: Optional[str] = None

class ProgramSchema(BaseModel):
    # Category 1: Program Basics
    program_name: SchemaField[str] = Field(default_factory=SchemaField)
    brand_name: SchemaField[str] = Field(default_factory=SchemaField)
    industry: SchemaField[str] = Field(default_factory=SchemaField)
    program_type: SchemaField[str] = Field(default_factory=SchemaField)
    geography: SchemaField[str] = Field(default_factory=SchemaField)
    membership_count: SchemaField[str] = Field(default_factory=SchemaField)
    program_launch_year: SchemaField[int] = Field(default_factory=SchemaField)
    membership_cost: SchemaField[str] = Field(default_factory=SchemaField)

    # Category 2: Earn Mechanics
    base_earn_rate: SchemaField[str] = Field(default_factory=SchemaField)
    bonus_earn_categories: SchemaField[List[str]] = Field(default_factory=SchemaField)
    bonus_earn_rates: SchemaField[Dict[str, str]] = Field(default_factory=SchemaField)
    non_transactional_earn: SchemaField[List[str]] = Field(default_factory=SchemaField)
    earn_cap: SchemaField[str] = Field(default_factory=SchemaField)
    earn_expiry_activity: SchemaField[str] = Field(default_factory=SchemaField)

    # Category 3: Burn Mechanics
    redemption_options: SchemaField[List[str]] = Field(default_factory=SchemaField)
    minimum_redemption_threshold: SchemaField[str] = Field(default_factory=SchemaField)
    point_value_cpp: SchemaField[float] = Field(default_factory=SchemaField)
    points_expiry_policy: SchemaField[str] = Field(default_factory=SchemaField)
    cashback_rate: SchemaField[str] = Field(default_factory=SchemaField)

    # Category 4: Tier System
    tier_count: SchemaField[int] = Field(default_factory=SchemaField)
    tier_names: SchemaField[List[str]] = Field(default_factory=SchemaField)
    tier_qualification_criteria: SchemaField[List[str]] = Field(default_factory=SchemaField)
    tier_qualification_period: SchemaField[str] = Field(default_factory=SchemaField)
    tier_benefits: SchemaField[Dict[str, List[str]]] = Field(default_factory=SchemaField)
    tier_status_expiry: SchemaField[str] = Field(default_factory=SchemaField)

    # Category 5: Partnerships
    partner_names: SchemaField[List[str]] = Field(default_factory=SchemaField)
    partnership_type_per_partner: SchemaField[Dict[str, str]] = Field(default_factory=SchemaField)
    partnership_details: SchemaField[List[str]] = Field(default_factory=SchemaField)
    co_brand_card: SchemaField[str] = Field(default_factory=SchemaField)

    # Category 6: Digital Experience
    mobile_app_available: SchemaField[str] = Field(default_factory=SchemaField)
    app_rating_ios: SchemaField[float] = Field(default_factory=SchemaField)
    app_rating_android: SchemaField[float] = Field(default_factory=SchemaField)
    app_review_count: SchemaField[str] = Field(default_factory=SchemaField)
    personalization_features: SchemaField[List[str]] = Field(default_factory=SchemaField)
    gamification_features: SchemaField[List[str]] = Field(default_factory=SchemaField)
    digital_only_benefits: SchemaField[List[str]] = Field(default_factory=SchemaField)

    # Category 7: Member Sentiment
    overall_sentiment: SchemaField[str] = Field(default_factory=SchemaField)
    common_praise: SchemaField[List[str]] = Field(default_factory=SchemaField)
    common_complaints: SchemaField[List[str]] = Field(default_factory=SchemaField)
    sentiment_sources_checked: SchemaField[List[str]] = Field(default_factory=SchemaField)
    nps_score: SchemaField[Optional[int]] = Field(default_factory=SchemaField)

    # Category 8: Competitive Position
    key_differentiators: SchemaField[List[str]] = Field(default_factory=SchemaField)
    known_weaknesses: SchemaField[List[str]] = Field(default_factory=SchemaField)
    closest_competitors: SchemaField[List[str]] = Field(default_factory=SchemaField)
    recent_changes: SchemaField[List[str]] = Field(default_factory=SchemaField)

class SourceMetadata(BaseModel):
    url: str
    domain: str
    page_type: str  # FAQ, Terms, Forum, News, etc.
    access_date: str
    tier: str  # Official, Press Release, News, Forum, etc.
    confidence_contribution: float
    status: str  # Accepted, Rejected (fingerprint mismatch), Rejected (other)
    rejection_reason: Optional[str] = None

class ResearchResult(BaseModel):
    schema_data: ProgramSchema
    narrative: str
    sources: List[SourceMetadata]
    completeness: int
    confidence_summary: Dict[str, int]  # count of high, medium, low, unverified, conflicts

class ComparisonResult(BaseModel):
    program_a_name: str
    program_b_name: str
    schema_a: ProgramSchema
    schema_b: ProgramSchema
    narrative_a: str
    narrative_b: str
    strategic_analysis: str
    comparison_table: List[Dict[str, Any]]
