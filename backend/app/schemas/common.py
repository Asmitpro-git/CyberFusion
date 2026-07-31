from __future__ import annotations

from pydantic import BaseModel


class ProjectStatusResponse(BaseModel):
    project: str
    version: str
    status: str


class HealthResponse(BaseModel):
    status: str


class VersionResponse(BaseModel):
    version: str
