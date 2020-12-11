class FeatureCodeException(Exception):
    def __init__(self, message):
        # Call Exception.__init__(message)
        # to use the same Message header as the parent class
        super().__init__(message)


class DuplicateRegionCode(Exception):
    def __init__(self, message):
        super().__init__(message)


# class MissingFeatureCode(Exception):
#     def __init__(self, message):
#         super().__init__(message)