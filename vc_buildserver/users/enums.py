from enum import Enum
from enum import unique


@unique
class UserGender(Enum):
    women = 'women'
    male = 'male'
    none = 'none'
