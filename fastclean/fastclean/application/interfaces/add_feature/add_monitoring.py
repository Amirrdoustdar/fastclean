from fastclean.application.interfaces.file_system import IFileSystemService

from ..base import BaseUseCase
from .dto import AddFeatureResponse, AddMonitoringRequest


class AddMonitoringUseCase(BaseUseCase[AddMonitoringRequest, AddFeatureResponse]):
    """Use case for adding monitoring"""

    def __init__(self, file_system: IFileSystemService):
        self._file_system = file_system

    def execute(self, request: AddMonitoringRequest) -> AddFeatureResponse:
        """Execute monitoring addition"""
        # TODO: Implement monitoring
        return AddFeatureResponse(
            feature_name="monitoring",
            files_created=[],
            files_modified=[],
            success=True,
            message="Monitoring feature coming soon!",
        )
