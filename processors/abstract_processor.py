class AbstractProcessor:
    def __init__(self):
        pass

    def process(self, input_filepath, output_filepath):
        raise NotImplementedError("Must be implemented by child class")
