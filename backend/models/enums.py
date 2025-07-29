from enum import Enum

class UserRole(str, Enum):
    admin = "Admin"
    user = "User"
