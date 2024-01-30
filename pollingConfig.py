"""
Example config file:
{
    "resort": "solitude",
    "username": "johndeervalley@gmail.com",
    "password": "snowboarderssuck",
    "dates": [
        "2024-01-05",
    ],
    "reservation_type": "passholder"
}
"""

import dataclasses
import datetime
from enum import Enum
import json
from resorts import Resort, Resorts


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
    alertNumber: str
    alertCarrier: str
    smsEmail: str
    smsEmailPassword: str


def load_json_config(path: str) -> ParkingConfig:
    with open(path) as f:
        config = json.load(f)

    try:
        if config["resort"] == "brighton":
            resort = Resorts.BRIGHTON

        elif config["resort"] == "solitude":
            resort = Resorts.SOLITUDE

        else:
            raise Exception(
                "Invalid resort specified in config, must be 'brighton' or 'solitude'")

        return ParkingConfig(
            username=config["username"],
            password=config["password"],
            resort=resort,
            reservation_type=ReservationType(config["reservation_type"]),
            dates=[datetime.datetime.strptime(
                date, "%Y-%m-%d").date() for date in config["dates"]
            ],
            alertNumber=config["alertNumber"] if "alertNumber" in config else None,
            alertCarrier=config["alertCarrier"] if "alertCarrier" in config else None,
            smsEmail=config["smsEmail"] if "smsEmail" in config else None,
            smsEmailPassword=config["smsEmailPassword"] if "smsEmailPassword" in config else None
        )

    except Exception as e:
        print("Invalid config file: ", e)
