from enum import Enum


class UserType(Enum):
    STUDENT = "student"
    ASSO = "asso"  # Shared account between association members
    TEACHER = "teacher"
    ADMIN = "admin"


class UserLevel(Enum):
    _1A = "1A"
    _2A = "2A"
    _3A = "3A"
    NA = "N/A"  # Not applicable, for teachers, assos and admins
