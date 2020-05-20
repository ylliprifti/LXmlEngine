from interface import Interface


class Engine(Interface):

    def process(self, process_tree: dict) -> dict:
        pass

