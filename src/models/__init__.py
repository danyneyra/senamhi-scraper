"""
Modelos de datos para el SENAMHI Scraper.
"""

from .station import (
    Station,
    StationCategory,
    StationType,
    StationStatus
)

from .data_schema import (
    get_headers_for_station_type,
    get_expected_columns_count,
    validate_csv_row,
    METEOROLOGICAL_CONVENTIONAL_HEADERS,
    METEOROLOGICAL_AUTOMATIC_HEADERS,
    HYDROLOGICAL_CONVENTIONAL_HEADERS,
    HYDROLOGICAL_AUTOMATIC_HEADERS
)

from .query import (
    QueryMode,
    OutputFormat,
    DateRange,
    QueryRequest,
    ScrapingResult
)

__all__ = [
    # Station models
    "Station",
    "StationCategory", 
    "StationType",
    "StationStatus",
    
    # Query models
    "QueryMode",
    "OutputFormat", 
    "DateRange",
    "QueryRequest",
    "ScrapingResult",
    
    # Data schema functions
    "get_headers_for_station_type",
    "get_expected_columns_count", 
    "validate_csv_row",
    
    # Headers constants
    "METEOROLOGICAL_CONVENTIONAL_HEADERS",
    "METEOROLOGICAL_AUTOMATIC_HEADERS",
    "HYDROLOGICAL_CONVENTIONAL_HEADERS", 
    "HYDROLOGICAL_AUTOMATIC_HEADERS"
]