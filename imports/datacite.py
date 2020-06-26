from rdmo.projects.imports import Import


class DataCiteImport(Import):

    def check(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError
