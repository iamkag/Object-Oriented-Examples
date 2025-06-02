"""Various Validators"""

def validate_integer(arg_name, arg_value, min_value=None,max_value=None, custom_min_message=None, custom_max_message=None):
    """"
    validates taht 'arg_value' is an integer and is within the range of 'min_value' and 'max_value'
    Args:
        arg_name: str: Name of the argument
        arg_value: obj: Value of the argument
        min_value: int: Minimum value of the argument
        max_value: int: Maximum value of the argument
        custom_min_message: str: Custom message for minimum value
        custom_max_message: str: Custom message for maximum
        
        Returns:
            None: no exceptions are raised if validation is successful

        Raises:
            TypeError: If arg_value does not have type int
            ValueError: If arg_value is less than min_value or greater than max_value
        """
    
    if not isinstance(arg_value, int):
        raise TypeError(f"{arg_name} must be an integer")
    
    if min_value is not None and arg_value < min_value:
        if custom_min_message is not None:
            raise ValueError(custom_min_message)
        raise ValueError(f"{arg_name} must be greater than {min_value}")
    
    if max_value is not None and arg_value > max_value:
        if custom_max_message is not None:
            raise ValueError(custom_max_message)
        raise ValueError(f"{arg_name} must be less than {max_value}")
    