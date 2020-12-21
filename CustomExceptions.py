class FeatureCodeException(Exception):
    """Used when FIPS code of a location is missing. Malformed GeoNames data."""
    def __init__(self, message):
        super().__init__(message)


class DuplicateRegionCode(Exception):
    """Used when a location has multiple child location of the same name or code."""
    def __init__(self, message):
        super().__init__(message)


class MissingFeatureCode(Exception):
    """Used when a location is missing some key attributes."""
    def __init__(self, message):
        super().__init__(message)


class UnknownCodeSystemConceptType(Exception):
    """Used when a Region class contains unknown value incompatible with FHIR CodeSystem structure."""
    def __init__(self, message):
        super().__init__(message)

class DataFileInWrongFormat(Exception):
    """Used when the input txt file data is in the wrong format or is malformed."""
    def __init__(self, message):
        super().__init__(message)