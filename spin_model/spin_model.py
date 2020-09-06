from .spin_site import IsingSpinSite

class SpinModel(object):
    ''' Abstract base class for spin model that used to store the
    parameters of the system'''
    pass

class IsingModel(SpinModel):
    ''' '''
    def __init__(self, interaction_strength=1.0):
        self.interaction_strength = interaction_strength

    def get_site(self, config=0, index=1):
        return IsingSpinSite(
            interaction_strength=self.interaction_strength,
            config=config, index=index)

class XYModel(SpinModel):
    def __init__(self):
        pass

    def get_site(self):
        pass

class HubbardModel(SpinModel):
    def __init__(self):
        pass

    def get_site(self):
        pass