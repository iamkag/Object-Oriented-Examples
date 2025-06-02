import pytest
from app.models import inventory

@pytest.fixture
def ssd_values():
    return {
        'name': 'Samsung 970 EVO',
        'manufacturer': 'Samsung',
        'total': 10,
        'allocated': 3,
        'capacity_gb': 512,
        'interface': 'NVMe',
    }

@pytest.fixture
def ssd(ssd_values):
    return inventory.SSD(**ssd_values)

def test_create_ssd(ssd, ssd_values):
    """Test creating a SSD"""
    for attr_name in ssd_values:
        assert getattr(ssd, attr_name) == ssd_values[attr_name]

def test_repr(ssd):
    assert ssd.category in repr(ssd)
    assert str(ssd.capacity_gb) in repr(ssd)
    assert ssd.interface in repr(ssd)