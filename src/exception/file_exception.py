class FileOpenError(Exception):
    def __init__(self,file_name):
        message = f'{file_name} is opened.\nPlease close {file_name} and start again!!!'
        super().__init__(message)