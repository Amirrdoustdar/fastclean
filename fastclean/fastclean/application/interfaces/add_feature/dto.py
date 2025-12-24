from dataclasses import dataclass
from pathlib import Path


@dataclass
class AddFeatureRequest:
    """Base request for adding features"""

    project_path: Path


@dataclass
class AddAuthenticationRequest(AddFeatureRequest):
    """Request for adding authentication"""

    auth_type: str  # jwt, oauth2, api_key
    secret_key: str | None = None


@dataclass
class AddCachingRequest(AddFeatureRequest):
    """Request for adding caching"""

    cache_type: str  # redis, memcached, in_memory
    connection_string: str | None = None


@dataclass
class AddMonitoringRequest(AddFeatureRequest):
    """Request for adding monitoring"""

    monitoring_type: str  # prometheus, elk
    port: int | None = None


@dataclass
class AddFeatureResponse:
    """Response for feature addition"""

    feature_name: str
    files_modified: list[Path]
    files_created: list[Path]
    success: bool
    message: str
