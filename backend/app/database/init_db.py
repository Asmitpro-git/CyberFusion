from sqlalchemy.orm import Session

from app.database.seed_roles import seed_roles


def initialize_database(db: Session):
    seed_roles(db)