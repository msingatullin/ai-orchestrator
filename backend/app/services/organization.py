from uuid import uuid4
from sqlalchemy.orm import Session
from ..models import Organization
from ..schemas import OrganizationCreate

class OrganizationService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, org_in: OrganizationCreate) -> Organization:
        org = Organization(id=str(uuid4()), name=org_in.name)
        self.db.add(org)
        self.db.commit()
        self.db.refresh(org)
        return org

    def get(self, org_id: str) -> Organization | None:
        return self.db.query(Organization).filter(Organization.id == org_id).first()
