import datetime as dt
from dataclasses import dataclass


@dataclass
class User:
    user_id: str
    first_name: str
    email: str


@dataclass
class Goal:
    user: User
    goal_type: str
    target_amount: float
    target_date: dt.date
