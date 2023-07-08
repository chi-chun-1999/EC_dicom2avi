class DataNotMatchError(Exception):
    def __init__(self, message):
        super().__init__(message)

class RedExtractError(DataNotMatchError):
    def __init__(self, message, file_name):
        message = f'{file_name} cannot find Red Feature'
        super().__init__(message)

class OCRExtractError(DataNotMatchError):
    def __init__(self, message, file_name):
        message = f'{file_name} cannot find Heart Rate on Dicom File'
        super().__init__(message)

class CycleExtractError(DataNotMatchError):
    def __init__(self, message, file_name):
        message = f'{file_name} cannot find Heart Rate on Dicom File'
        super().__init__(message)

class RWaveExtractError(DataNotMatchError):
    def __init__(self, message, file_name):
        message = f'{file_name} R Wave extract Error'
        super().__init__(message)

class MultiCycleExtractError(DataNotMatchError):
    def __init__(self, message, file_name):
        message = f'{file_name} Multi Cycle extract Error'
        super().__init__(message)