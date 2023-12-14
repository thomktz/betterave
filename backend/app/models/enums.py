"""
Enums for user types and levels.

UserType:
- STUDENT: a student
- ASSO: a shared account between association members
- TEACHER: a teacher
- ADMIN: an administrator

UserLevel:
- _1A: first year student
- _2A: second year student
- _3A: third year student
"""

from enum import Enum


class UserType(Enum):
    """User types."""

    STUDENT = "student"
    ASSO = "asso"  # Shared account between association members
    TEACHER = "teacher"
    ADMIN = "admin"


class UserLevel(Enum):
    """User levels."""

    _1A = "1A"
    _2A = "2A"
    _3A = "3A"
    NA = "N/A"  # Not applicable, for teachers, assos and admins
