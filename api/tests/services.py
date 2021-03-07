class BuzzClient:
    """
    A client for connecting to the buzz API.
    """
    def __init__(self, app, return_json=True):
        self.API_BASE = '/api'
        self.app = app
        self.return_json = return_json

    def response_or_json(self, response):
        result = response.json if self.return_json else response
        return result
        
    def events(self, params):
        resp = self.app.get(f'{self.API_BASE}/events/?{params}&format=json')
        return self.response_or_json(resp)

    def matches(self, params):
        resp = self.app.get(f'{self.API_BASE}/matches/?{params}&format=json')
        return self.response_or_json(resp)

    def streams(self, params):
        resp = self.app.get(f'{self.API_BASE}/streams/?{params}&format=json')
        return self.response_or_json(resp)

    def players(self, params):        
        resp = self.app.get(f'{self.API_BASE}/players/?{params}&format=json')
        return self.response_or_json(resp)

    def playing(self):
        resp = self.app.get(f'{self.API_BASE}/playing/?format=json')
        return self.response_or_json(resp)
