from dataclasses import dataclass


@dataclass
class F1Config:
    """Configuration limits for F1 API models."""

    # URL lengths
    min_url_length: int = 10
    max_url_length: int = 500

    # String field limits
    min_name_length: int = 2
    max_name_length: int = 100

    min_nationality_length: int = 2
    max_nationality_length: int = 50

    min_circuit_name_length: int = 3
    max_circuit_name_length: int = 100

    min_country_length: int = 2
    max_country_length: int = 100

    # Numeric limits
    min_position: int = 1
    max_position: int = 30

    min_points: float = 0.0
    max_points: float = 1000.0

    min_year: int = 1950
    max_year: int = 2100

    # API Configuration
    ergast_api_base_url: str = "https://ergast.com/api/f1"
    default_timeout: int = 10


f1_config = F1Config()
