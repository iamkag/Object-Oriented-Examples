import pytest

from app.models import inventory

@pytest.fixture
def hdd_values():
    return {
        'name': 'Seagate Barracuda',
        'manufacturer': 'Seagate',
        'total': 10,
        'allocated': 3,
        'capacity_gb': 512,
        'size': '3.5"',
        'rpm': 7200
    }

@pytest.fixture
def hdd(hdd_values):
    return inventory.HDD(**hdd_values)

def test_create_hdd(hdd, hdd_values):
    """Test creating a HDD"""
    for attr_name in hdd_values:
        assert getattr(hdd, attr_name) == hdd_values[attr_name]

@pytest.mark.parametrize('size, exception', [('1.8"', ValueError), ('2.5"', None), ('3.5"', None), ('4.0"', ValueError)])
def test_create_invalid_size(size, exception, hdd_values):
    """Test creating a HDD with invalid size"""
    hdd_values['size'] = size
    if exception:
        with pytest.raises(exception):
            inventory.HDD(**hdd_values)
    else:
        inventory.HDD(**hdd_values)
    
@pytest.mark.parametrize('rpm, exception', [(10, ValueError), (1_000, None), (50_000, None), (60_000, ValueError)])
def test_create_invalid_rpm(rpm, exception, hdd_values):
    """Test creating a HDD with invalid RPM"""
    hdd_values['rpm'] = rpm
    if exception:
        with pytest.raises(exception):
            inventory.HDD(**hdd_values)
    else:
        inventory.HDD(**hdd_values)

def test_repr(hdd):
    assert hdd.category in repr(hdd)
    assert str(hdd.capacity_gb) in repr(hdd)
    assert hdd.size in repr(hdd)
    assert str(hdd.rpm) in repr(hdd)