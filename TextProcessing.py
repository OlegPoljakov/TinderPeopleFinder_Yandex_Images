class TextParse:
    def __init__(self):
        """Constructor"""
        pass

    @staticmethod
    def ParseImageLocation(location):
        actuallocation = location.replace(' \ ',' / ')
        return actuallocation