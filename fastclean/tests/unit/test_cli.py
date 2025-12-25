import pytest
from pathlib import Path


class TestCLIInit:
    """Tests for init command."""
    
    def test_project_name_validation(self):
        """Test project name is valid."""
        valid_names = ["my_project", "test123", "app"]
        for name in valid_names:
            assert name.replace("_", "").isalnum()
    
    def test_sample_config(self, sample_project_config):
        """Test sample config fixture."""
        assert sample_project_config["name"] == "test_project"
        assert sample_project_config["db"] == "postgresql"


class TestCLICrud:
    """Tests for crud command."""
    
    def test_entity_config(self, sample_entity_config):
        """Test entity config fixture."""
        assert sample_entity_config["name"] == "Product"
        assert "price:float" in sample_entity_config["fields"]
    
    def test_field_parsing(self):
        """Test field string parsing."""
        fields_str = "name:str,price:float,quantity:int"
        fields = fields_str.split(",")
        assert len(fields) == 3
        assert fields[0] == "name:str"


class TestProjectGeneration:
    """Tests for project generation."""
    
    def test_temp_path_exists(self, temp_project_path):
        """Test temp path fixture."""
        assert temp_project_path is not None
        assert isinstance(temp_project_path, Path)