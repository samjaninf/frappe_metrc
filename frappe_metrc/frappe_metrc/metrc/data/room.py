from ..request import METRC

class Room(METRC):
    def _endpoint(self):
        return "/rooms/v1/"

    def get(self, id=None):
        self._get(self._endpoint(), {"id" : id})