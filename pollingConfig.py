import dataclasses
import datetime
from enum import Enum
import json


class Resort(Enum):
    BRIGHTON = "brighton"
    SOLITUDE = "solitude"


class ReservationType(Enum):
    PASSHOLDER = "passholder"
    CARPOOL = "carpool"


@dataclasses.dataclass
class ParkingConfig:
    username: str
    password: str
    resort: Resort
    dates: list[datetime.date]
    reservation_type: ReservationType


def load_json_config(path: str) -> ParkingConfig:
    with open(path) as f:
        config = json.load(f)

    try:
        return ParkingConfig(
            username=config["username"],
            password=config["password"],
            resort=Resort(config["resort"]),
            reservation_type=ReservationType(config["reservation_type"]),
            dates=[datetime.datetime.strptime(
                date, "%Y-%m-%d").date() for date in config["dates"]
            ]
        )

    except Exception as e:
        print("Invalid config file: ", e)
