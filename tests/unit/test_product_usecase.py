import pytest
from unittest.mock import Mock, MagicMock
from src.domain.entities.product import Product
from src.application.usecases.product.create_product import CreateProductUseCase
from src.application.usecases.product.get_product import GetProductUseCase


class TestCreateProductUseCase:
    def setup_method(self):
        self.repository = Mock()
        self.usecase = CreateProductUseCase(self.repository)

    def test_create_product_success(self):
        # Arrange
        self.repository.create.return_value = Product(
            id=1,
            name=str(),
            price=float(),
            quantity=int(),
        )

        # Act
        result = self.usecase.execute(
            {
                "name": str(),
                "price": float(),
                "quantity": int(),
            }
        )

        # Assert
        assert result is not None
        self.repository.create.assert_called_once()


class TestGetProductUseCase:
    def setup_method(self):
        self.repository = Mock()
        self.usecase = GetProductUseCase(self.repository)

    def test_get_product_success(self):
        # Arrange
        self.repository.get_by_id.return_value = Product(
            id=1,
            name=str(),
            price=float(),
            quantity=int(),
        )

        # Act
        result = self.usecase.execute(1)

        # Assert
        assert result is not None
        self.repository.get_by_id.assert_called_once_with(1)

    def test_get_product_not_found(self):
        # Arrange
        self.repository.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(Exception):
            self.usecase.execute(999)
