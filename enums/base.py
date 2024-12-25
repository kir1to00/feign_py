from enum import Enum
from typing import Union


class BaseEnum(Enum):
    """Base class for enums with a parse method to convert string to enum value."""

    @classmethod
    def parse(cls, name: str) -> Union[str, None]:
        """Parse the given string into an enum value or return None if not found."""
        if not name:
            return None
        name = name.upper()
        try:
            return cls._member_map_[name].value
        except KeyError:
            return None  # Return None if the name does not match any enum member
