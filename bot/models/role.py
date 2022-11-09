from enum import Enum


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    Ban = 'ban'  # todo сделать отдельный фильтр для бана.
