from pydantic import BaseModel, Field, HttpUrl, ConfigDict
from typing import Optional, List
from src.external_api.config import f1_config as cfg


class DriverModel(BaseModel):
    """Model for F1 Driver information."""

    driverId: str = Field(
        ...,
        description="Driver unique identifier",
        min_length=cfg.min_name_length,
        max_length=cfg.max_name_length,
    )
    givenName: str = Field(
        ...,
        description="Driver's first name",
        min_length=cfg.min_name_length,
        max_length=cfg.max_name_length,
    )
    familyName: str = Field(
        ...,
        description="Driver's last name",
        min_length=cfg.min_name_length,
        max_length=cfg.max_name_length,
    )
    dateOfBirth: str = Field(..., description="Driver's date of birth (YYYY-MM-DD)")
    nationality: str = Field(
        ...,
        description="Driver's nationality",
        min_length=cfg.min_nationality_length,
        max_length=cfg.max_nationality_length,
    )
    url: str = Field(..., description="Wikipedia URL of the driver")

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class ConstructorModel(BaseModel):
    """Model for F1 Constructor (team) information."""

    constructorId: str = Field(
        ...,
        description="Constructor unique identifier",
        min_length=cfg.min_name_length,
        max_length=cfg.max_name_length,
    )
    name: str = Field(
        ...,
        description="Constructor name",
        min_length=cfg.min_name_length,
        max_length=cfg.max_name_length,
    )
    nationality: str = Field(
        ...,
        description="Constructor's nationality",
        min_length=cfg.min_nationality_length,
        max_length=cfg.max_nationality_length,
    )
    url: str = Field(..., description="Wikipedia URL of the constructor")

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class CircuitLocationModel(BaseModel):
    """Model for Circuit Location."""

    lat: str = Field(..., description="Latitude of the circuit")
    long: str = Field(..., description="Longitude of the circuit")
    locality: str = Field(
        ...,
        description="City/locality where circuit is located",
        min_length=cfg.min_name_length,
        max_length=cfg.max_circuit_name_length,
    )
    country: str = Field(
        ...,
        description="Country where circuit is located",
        min_length=cfg.min_country_length,
        max_length=cfg.max_country_length,
    )

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class CircuitModel(BaseModel):
    """Model for F1 Circuit information."""

    circuitId: str = Field(
        ...,
        description="Circuit unique identifier",
        min_length=cfg.min_name_length,
        max_length=cfg.max_name_length,
    )
    circuitName: str = Field(
        ...,
        description="Official circuit name",
        min_length=cfg.min_circuit_name_length,
        max_length=cfg.max_circuit_name_length,
    )
    url: str = Field(..., description="Wikipedia URL of the circuit")
    Location: CircuitLocationModel = Field(..., description="Circuit location details")

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class RaceModel(BaseModel):
    """Model for F1 Race information."""

    season: str = Field(..., description="Season year")
    round: str = Field(..., description="Round number in the season")
    raceName: str = Field(
        ...,
        description="Official race name",
        min_length=cfg.min_name_length,
        max_length=cfg.max_circuit_name_length,
    )
    date: str = Field(..., description="Race date (YYYY-MM-DD)")
    time: Optional[str] = Field(None, description="Race time (HH:MM:SSZ)")
    url: str = Field(..., description="Wikipedia URL of the race")
    Circuit: CircuitModel = Field(..., description="Circuit where race takes place")

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class StandingModel(BaseModel):
    """Model for Driver or Constructor standings."""

    position: str = Field(..., description="Current position in standings")
    points: str = Field(..., description="Total points")
    wins: str = Field(..., description="Number of wins")
    Driver: Optional[DriverModel] = Field(None, description="Driver information")
    Constructor: Optional[ConstructorModel] = Field(
        None, description="Constructor information"
    )

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class F1DataModel(BaseModel):
    """Raw model for F1 API response data."""

    data_type: str = Field(..., description="Type of F1 data (drivers, races, etc)")
    season: Optional[str] = Field(None, description="Season year if applicable")
    items: List[dict] = Field(..., description="Raw data items from F1 API")

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class F1ProcessedModel(BaseModel):
    """Processed model for F1 data with custom formatting."""

    title: str = Field(..., description="Processed data title")
    description: str = Field(..., description="Description of the data")
    season: Optional[str] = Field(None, description="Season year if applicable")
    total_items: int = Field(..., description="Total number of items", ge=0)
    summary: str = Field(..., description="Summary of the processed data")
    items: List[dict] = Field(..., description="Processed data items")

    model_config: ConfigDict = ConfigDict(from_attributes=True)
