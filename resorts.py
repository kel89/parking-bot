from enum import Enum
import dataclasses
from enum import Enum
import dataclasses


@dataclasses.dataclass
class Resort:
    base_url: str
    main_screen_string: str
    passholder_string: str
    carpool_string: str


class Resorts(Enum):
    BRIGHTON = Resort(
        base_url="https://reservenski.parkbrightonresort.com",
        main_screen_string="Reserve Parking Before Arriving at Brighton",
        passholder_string="Season\'s Pass",
        carpool_string="3+ Carpool"
    )

    SOLITUDE = Resort(
        base_url="https://reservenski.parksolitude.com",
        main_screen_string="Reserve Parking Before Arriving at Solitude",
        passholder_string="Season Pass Holders",
        carpool_string="Carpool 4+ occupancy or ADA "
    )
