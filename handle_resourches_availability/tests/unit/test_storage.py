import pytest

from app.models import inventory

@pytest.fixture
def storage_values():
    return {
        'name': 'Thumbdrive',
        'manufacturer': 'Sandisk',
        'total': 10,
        'allocated': 3,
        'capacity_gb': 512
    }

@pytest.fixture
def storage(storage_values):
    return inventory.Storage(**storage_values)

def test_create_storage(storage_values, storage):
    """Test creating a storage device"""
    for attr_name in storage_values:
        assert getattr(storage, attr_name) == storage_values[attr_name]

def test_repr(storage):
    assert storage.category in repr(storage)
    assert str(storage.capacity_gb) in repr(storage)