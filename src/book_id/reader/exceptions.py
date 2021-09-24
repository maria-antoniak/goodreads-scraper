class ReaderException(Exception):
    pass


class InputFileIsEmpty(ReaderException):
    def __init__(self, path_to_input_file: str):
        self.path_to_input_file = path_to_input_file
        super().__init__(
            f"File appears to be empty. Please check '{self.path_to_input_file}' contains queries."
        )
