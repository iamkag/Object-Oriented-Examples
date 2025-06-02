"""
Test the resource module
"""

import pytest
from app.models import inventory

@pytest.fixture
def resource_values():
    return {
        'name': 'Parrot',
        'manufacturer': 'Pirates A-Hoy',
        'total': 100,
        'allocated': 50
    }

@pytest.fixture
def resource(resource_values):
    return inventory.Resource(**resource_values)

def test_create_resource(resource_values, resource):
    """Test creating a resource"""
    for attr_name in resource_values:
        assert getattr(resource, attr_name) == resource_values[attr_name]
    # assert resource.name == resource_values['name']
    # assert resource.manufacturer == resource_values['manufacturer']
    # assert resource.total == resource_values['total']
    # assert resource.allocated == resource_values['allocated']

def test_create_invalid_total_type():
    """Test creating a resource with an invalid total type"""
    with pytest.raises(TypeError) as e:
        inventory.Resource('Parrot', 'Pirates A-Hoy', 10.5, 5)

def test_create_invalid_allocated_type():
    """Test creating a resource with an invalid allocated type"""
    with pytest.raises(TypeError) as e:
        inventory.Resource('name', 'manu', 10, 2.5)

def test_create_invalid_total_value():
    """Test creating a resource with an invalid total value"""
    with pytest.raises(ValueError) as e:
        inventory.Resource('Parrot', 'Pirates A-Hoy', -10, 0)    

####################

@pytest.mark.parametrize('total, allocated', [(10, -5), (10, 20)])
def test_create_invalid_allocated_value(total, allocated):
    """Test creating a resource with an invalid allocated value"""
    with pytest.raises(ValueError) as e:
        inventory.Resource('Parrot', 'Pirates A-Hoy', total, allocated)

def test_total(resource):
    assert resource.total == resource._total

def test_allocated(resource):
    assert resource.allocated == resource._allocated

def test_available(resource):
    assert resource.available == resource.total - resource.allocated

def test_category(resource):
    assert resource.category == 'resource'

def test_str_repr(resource):
    assert str(resource) == resource.name
    
def test_repr_repr(resource):
    assert repr(resource) == f"{resource.category}({resource.name}, {resource.manufacturer}, {resource.total}, {resource.allocated})"

def test_claim(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.claim(n)
    assert resource.allocated == original_allocated + n
    assert resource.total == original_total

@pytest.mark.parametrize('value', [0, -1, 1_000])
def test_claim_invalid(value, resource):
    with pytest.raises(ValueError) as e:
        resource.claim(value)
 
def test_freeup(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.freeup(n)
    assert resource.allocated == original_allocated - n
    assert resource.total == original_total

@pytest.mark.parametrize('value', [0, -1, 1_000])
def test_freeup_invalid(value, resource):
    with pytest.raises(ValueError) as e:
        resource.freeup(value)

def test_died(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.died(n)
    assert resource.total == original_total - n
    assert resource.allocated == original_allocated - n
    

@pytest.mark.parametrize('value', [-1, 0, 1_000])
def test_died_invalid(resource, value):
    print(f"Testing died with value={value}")
    with pytest.raises(ValueError):
        resource.died(value)

def test_purchase(resource):
    n = 2
    original_total = resource.total
    original_allocated = resource.allocated
    resource.purchase(n)
    assert resource.total == original_total + n
    assert resource.allocated == original_allocated

@pytest.mark.parametrize('value', [-1, 0])
def test_purchase_invalid(value, resource):
    with pytest.raises(ValueError) as e:
        resource.purchase(value)
