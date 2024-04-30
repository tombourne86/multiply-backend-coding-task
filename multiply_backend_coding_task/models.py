import datetime as dt
from dataclasses import dataclass
from enum import Enum
from typing import Optional


@dataclass
class User:
    user_id: str
    first_name: str
    email: str


@dataclass
class Goal:
    user: Optional[User] = None
    goal_type: Optional["GoalType"] = None
    target_amount: Optional[float] = None
    target_date: Optional[dt.date] = None


# GoalType is a subclass of string to make serialising an Enum to json simpler
class GoalType(str, Enum):
    WEDDING = "WEDDING"
    HOMEBUYING = "HOMEBUYING"
    NEW_CAR = "NEW_CAR"
    CUSTOM = "CUSTOM"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_
