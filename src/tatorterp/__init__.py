
class Episode(object):
    def __init__(self, episode_index, title, location, broadcaster, **kwargs):
        self.episode_index = episode_index
        self.title = title
        self.location = location
        self.broadcaster = broadcaster
        self._attribs = ["episode_index","title","location","broadcaster"]
        for key, val in kwargs.items():
            setattr(self, key, val)
            self._attribs.append(key)
        
        
        