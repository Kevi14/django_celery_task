from enum import Enum

class ActionEnum(Enum):
    VIEW = "view"
    EDIT = "edit"
    DELETE = "delete"
    CREATE = "create"

    @classmethod
    def choices(cls):
        return [(action.value, action.name.capitalize()) for action in cls]
