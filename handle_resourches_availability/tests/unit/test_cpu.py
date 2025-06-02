"""
(env) (base) ➜  handle_resourches_availability python -m pytest tests/unit/test_cpu.py
"""
import pytest

from app.models import inventory

@pytest.fixture
def cpu_values():
    return {
        'name': 'RYZEN Threadripper 2990WX',
        'manufacturer': 'AMD',
        'total': 10,
        'allocated': 3,
        'cores': 32,
        'socket': 'sTR4',
        'power_watts': 250
    }

@pytest.fixture
def cpu(cpu_values):
    return inventory.CPU(**cpu_values)

def test_create_cpu(cpu_values, cpu):
    """Test creating a CPU"""
    for attr_name in cpu_values:
        assert getattr(cpu, attr_name) == cpu_values[attr_name]

@pytest.mark.parametrize('cores, exception', [(10.5, TypeError), (-1, ValueError), (0, ValueError)])
def test_create_invalid_cores(cores, exception, cpu_values):
    """Test creating a CPU with invalid cores"""
    cpu_values['cores'] = cores
    with pytest.raises(exception):
        inventory.CPU(**cpu_values)

def test_repr(cpu):
    assert cpu.category in repr(cpu)
    assert cpu.name in repr(cpu)
    assert cpu.socket in repr(cpu)
    assert str(cpu.cores) in repr(cpu)
   