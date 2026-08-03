import uuid

from sqlalchemy.orm import Session

from app.models.role import Role


DEFAULT_ROLES = [
    {
        "name": "Administrator",
        "description": "Full system access",
        "permissions": {
            "users": ["create", "read", "update", "delete"],
            "roles": ["create", "read", "update", "delete"],
            "alerts": ["read", "update"],
            "dashboard": ["view"],
            "settings": ["update"],
        },
    },
    {
        "name": "SOC Analyst",
        "description": "Security Operations Center Analyst",
        "permissions": {
            "dashboard": ["view"],
            "alerts": ["read", "update"],
            "logs": ["read"],
        },
    },
    {
        "name": "Incident Responder",
        "description": "Incident Response Team",
        "permissions": {
            "alerts": ["read", "update"],
            "incidents": ["create", "update"],
        },
    },
    {
        "name": "Threat Hunter",
        "description": "Threat Hunting Team",
        "permissions": {
            "threats": ["read"],
            "logs": ["read"],
        },
    },
    {
        "name": "Digital Forensics Analyst",
        "description": "Digital Forensics Team",
        "permissions": {
            "forensics": ["read", "create"],
        },
    },
    {
        "name": "Viewer",
        "description": "Read-only user",
        "permissions": {
            "dashboard": ["view"],
            "alerts": ["read"],
        },
    },
]


def seed_roles(db: Session):
    for role_data in DEFAULT_ROLES:

        existing = db.query(Role).filter(
            Role.name == role_data["name"]
        ).first()

        if existing:
            continue

        db.add(
            Role(
                id=uuid.uuid4(),
                **role_data,
            )
        )

    db.commit()