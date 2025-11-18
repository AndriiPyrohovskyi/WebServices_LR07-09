import requests
from typing import Optional, List, Dict, Any
from src.external_api.models import (
    F1DataModel,
    F1ProcessedModel,
    DriverModel,
    RaceModel,
)
from src.external_api.config import f1_config as cfg


class F1Service:
    """Service to interact with F1 Ergast API."""

    def __init__(self):
        self.base_url = cfg.ergast_api_base_url
        self.timeout = cfg.default_timeout

    def get_current_season_drivers(self) -> F1DataModel:
        """
        Fetch current season drivers from F1 API.
        :return: F1DataModel with raw driver data.
        """
        url = f"{self.base_url}/current/drivers.json"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        drivers_data = data["MRData"]["DriverTable"]["Drivers"]
        season = data["MRData"]["DriverTable"].get("season", "current")

        return F1DataModel(
            data_type="drivers", season=season, items=drivers_data
        )

    def get_current_season_races(self) -> F1DataModel:
        """
        Fetch current season race schedule from F1 API.
        :return: F1DataModel with raw race data.
        """
        url = f"{self.base_url}/current.json"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        races_data = data["MRData"]["RaceTable"]["Races"]
        season = data["MRData"]["RaceTable"].get("season", "current")

        return F1DataModel(
            data_type="races", season=season, items=races_data
        )

    def get_driver_standings(self, season: Optional[str] = "current") -> F1DataModel:
        """
        Fetch driver standings for a specific season.
        :param season: Season year (default: current)
        :return: F1DataModel with raw standings data.
        """
        url = f"{self.base_url}/{season}/driverStandings.json"
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        standings_data = data["MRData"]["StandingsTable"]["StandingsLists"]
        actual_season = (
            standings_data[0]["season"] if standings_data else season
        )

        driver_standings = []
        if standings_data:
            driver_standings = standings_data[0]["DriverStandings"]

        return F1DataModel(
            data_type="driver_standings",
            season=actual_season,
            items=driver_standings,
        )

    def process_drivers_data(self, raw_data: F1DataModel) -> F1ProcessedModel:
        """
        Process raw driver data into a more readable format.
        :param raw_data: Raw F1DataModel with driver data
        :return: F1ProcessedModel with processed driver information
        """
        processed_items = []
        for driver in raw_data.items:
            processed_items.append(
                {
                    "full_name": f"{driver['givenName']} {driver['familyName']}",
                    "nationality": driver["nationality"],
                    "driver_number": driver.get("permanentNumber", "N/A"),
                    "code": driver.get("code", "N/A"),
                    "birth_date": driver["dateOfBirth"],
                    "wiki_url": driver["url"],
                }
            )

        summary = f"Current season has {len(processed_items)} registered drivers from various nations."

        return F1ProcessedModel(
            title=f"F1 {raw_data.season} Season - Drivers",
            description="List of all drivers competing in the current Formula 1 season",
            season=raw_data.season,
            total_items=len(processed_items),
            summary=summary,
            items=processed_items,
        )

    def process_races_data(self, raw_data: F1DataModel) -> F1ProcessedModel:
        """
        Process raw race data into a more readable format.
        :param raw_data: Raw F1DataModel with race data
        :return: F1ProcessedModel with processed race information
        """
        processed_items = []
        for race in raw_data.items:
            circuit = race["Circuit"]
            location = circuit["Location"]

            processed_items.append(
                {
                    "round": race["round"],
                    "race_name": race["raceName"],
                    "circuit_name": circuit["circuitName"],
                    "location": f"{location['locality']}, {location['country']}",
                    "date": race["date"],
                    "time": race.get("time", "TBA"),
                    "coordinates": {
                        "lat": location["lat"],
                        "long": location["long"],
                    },
                }
            )

        summary = f"The {raw_data.season} F1 season includes {len(processed_items)} races across different countries."

        return F1ProcessedModel(
            title=f"F1 {raw_data.season} Season - Race Calendar",
            description="Complete race schedule for the Formula 1 season",
            season=raw_data.season,
            total_items=len(processed_items),
            summary=summary,
            items=processed_items,
        )

    def process_standings_data(self, raw_data: F1DataModel) -> F1ProcessedModel:
        """
        Process raw standings data into a more readable format.
        :param raw_data: Raw F1DataModel with standings data
        :return: F1ProcessedModel with processed standings information
        """
        processed_items = []
        for standing in raw_data.items:
            driver = standing["Driver"]
            constructors = standing.get("Constructors", [])
            team_name = constructors[0]["name"] if constructors else "N/A"

            processed_items.append(
                {
                    "position": int(standing["position"]),
                    "driver_name": f"{driver['givenName']} {driver['familyName']}",
                    "driver_code": driver.get("code", "N/A"),
                    "nationality": driver["nationality"],
                    "team": team_name,
                    "points": float(standing["points"]),
                    "wins": int(standing["wins"]),
                }
            )

        # Sort by position
        processed_items.sort(key=lambda x: x["position"])

        leader = processed_items[0] if processed_items else None
        summary = (
            f"Championship leader: {leader['driver_name']} with {leader['points']} points and {leader['wins']} wins."
            if leader
            else "No standings data available."
        )

        return F1ProcessedModel(
            title=f"F1 {raw_data.season} Season - Driver Standings",
            description="Current driver championship standings",
            season=raw_data.season,
            total_items=len(processed_items),
            summary=summary,
            items=processed_items,
        )


service = F1Service()
