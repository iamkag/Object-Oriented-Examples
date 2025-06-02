""" Inventory model """

from app.utils.validators import validate_integer

class Resource:
    """Base class for resources"""
    
    def __init__(self, name, manufacturer, total, allocated):
        """
        Args:
            name: str: Name of the resource
            manufacturer: str: Manufacturer of the resource
            total: int: Total number of resources
            allocated: int: Number of resources allocated

        Note:
            allocated cannot exceed total
        """
        self._name = name
        self._manufacturer = manufacturer
        validate_integer('total', total, min_value = 0)
        self._total = total
        validate_integer('allocated', allocated, min_value = 0, max_value = total, custom_max_message = 'Allocated inventory cannot exceed totalinventory')
        self._allocated = allocated

    @property
    def name(self):
        return self._name
    
    @property
    def manufacturer(self):
        return self._manufacturer
    
    @property
    def total(self):
        return self._total
    
    @property
    def allocated(self):
        return self._allocated
    
    @property
    def category(self):
        return type(self).__name__.lower()

    @property
    def available(self):
        return self.total - self.allocated
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"{self.category}({self.name}, {self.manufacturer}, {self.total}, {self.allocated})"
    
    def claim(self, num):
        """ Claim num inventory items (if available)
        Args:
            num: int: Number of items to claim
        """
        validate_integer('num', num, min_value = 1, max_value = self.available, custom_max_message = 'Cannot claim more inventory than available')
        self._allocated += num

    def freeup(self, num):
        """ Free up num inventory items
        Args:
            num: int: Number of items to free up
        """
        validate_integer('num', num, min_value = 1, max_value = self.allocated, custom_max_message = 'Cannot free up more inventory than allocated')
        self._allocated -= num

    def died(self, num):
        """ Number of items to deallocate and remove from inventory pool altogether """
        validate_integer('num', num, min_value = 1, max_value = self.allocated, custom_max_message = 'Cannot retire more than allocated')
        self._total -= num
        self._allocated -= num
    
    def purchase(self, num):
        """ Number of items to add to inventory pool """
        validate_integer('num', num, min_value = 1)
        self._total += num


class CPU(Resource):
    """CPU Resource used to track specific CPU inventory pools"""
    def __init__(self, name, manufacturer, total, allocated, cores, socket, power_watts):
        """
        Args:
            name: str: Name of the CPU
            manufacturer: str: Manufacturer of the CPU
            total: int: Total number of CPUs
            allocated: int: Number of CPUs allocated
            cores: int: Number of cores
            socket: str: CPU socket type
            power_watts: int: Power consumption in watts

        """
        super().__init__(name, manufacturer, total, allocated)
        validate_integer('cores', cores, min_value = 1)
        validate_integer('power_watts', power_watts, min_value = 1)
        self._cores = cores
        self._socket = socket
        self._power_watts = power_watts

    @property
    def cores(self):
        return self._cores
    
    @property
    def socket(self):
        return self._socket
    
    @property
    def power_watts(self):
        return self._power_watts
    
    def __repr__(self):
        return f"{self.category}: {self.name} ({self.socket} - x{self.cores})"
    
class Storage(Resource):
    """
    A base class for storage devices - probably not used directly
    """

    def __init__(self, name, manufacturer, total, allocated, capacity_gb):
        """
        Args:
            name: str: Name of the storage device
            manufacturer: str: Manufacturer of the storage device
            total: int: Total number of storage devices
            allocated: int: Number of storage devices allocated
            capacity_gb: int: Capacity in gigabytes
        """
        super().__init__(name, manufacturer, total, allocated)
        validate_integer('capacity_gb', capacity_gb, min_value = 1)
        self._capacity_gb = capacity_gb
        
    @property
    def capacity_gb(self):
        return self._capacity_gb
    
    def __repr__(self):
        return f"{self.category}: {self.capacity_gb} GB"
    
class HDD(Storage):
    """"
    Class used for HDD type resources
    """

    def __init__(self, name, manufacturer, total, allocated, capacity_gb, size, rpm):
        """
        Args:
            name: str: Name of the HDD
            manufacturer: str: Manufacturer of the HDD
            total: int: Total number of HDDs
            allocated: int: Number of HDDs allocated
            capacity_gb: int: Capacity in gigabytes
            size: float: Size in inches
            rpm: int: Rotations per minute
        """
        super().__init__(name, manufacturer, total, allocated, capacity_gb)
        allowed_sizes = ['2.5"', '3.5"']
        if size not in allowed_sizes:
            raise ValueError(f"Invalid HDD size.\nSize must be one of {allowed_sizes}")
        validate_integer('rpm', rpm, min_value = 1_000, max_value = 50_000)

        self._size = size
        self._rpm = rpm

    @property
    def size(self):
        return self._size
    
    @property
    def rpm(self):
        return self._rpm
    
    def __repr__(self):
        s = super().__repr__()
        return f"{s}: {self.size} - {self.rpm} RPM"

class SSD(Storage):
    """
    Class used for SSD type resources
    """

    def __init__(self, name, manufacturer, total, allocated, capacity_gb, interface):
        """
        Args:
            name: str: Name of the SSD
            manufacturer: str: Manufacturer of the SSD
            total: int: Total number of SSDs
            allocated: int: Number of SSDs allocated
            capacity_gb: int: Capacity in gigabytes
            interface: str: Interface type
        """
        super().__init__(name, manufacturer, total, allocated, capacity_gb)
        allowed_interfaces = ['SATA', 'SAS', 'NVMe']
        if interface not in allowed_interfaces:
            raise ValueError(f"Invalid interface.\nInterface must be one of {allowed_interfaces}")
        
        self._interface = interface

    @property
    def interface(self):
        return self._interface
    
    def __repr__(self):
        s = super().__repr__()
        return f"{s}: {self.interface}"