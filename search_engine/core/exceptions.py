class EmptyCorpusException(Exception):
    """
    Represent exeption which occurs when we get path to an empty folder.
    """
    def __init__(self, path:str)->None:
        super().__init__(f"Empty corpus at {path}")
