class BuzzClient:
    """
    A client for connecting to the buzz API.
    """
    def __init__(self, app, token=None, return_json=True):
        self.API_BASE = ''
        self.app = app
        self.return_json = return_json
        self.headers = []
        
        if token:
            self.headers.append(
                ('Authorization', f'Token {token.key}')
            ) 

    def response_or_json(self, response):
        result = response.json if self.return_json else response
        return result

    def request(
        self, url, id=None, data=None, method='GET', expect_errors=False):

        if method == 'GET':
            resp = self.app.get(url, headers=self.headers, expect_errors=expect_errors)

        elif method == 'POST':
            resp = self.app.post_json(
                url, params=data, headers=self.headers, expect_errors=expect_errors)

        elif method == 'PATCH':
            resp = self.app.patch_json(
                url, params=data, headers=self.headers, expect_errors=expect_errors)

        elif method == 'DELETE':
            resp = self.app.delete_json(
                url, headers=self.headers, expect_errors=expect_errors)

        return self.response_or_json(resp)
    
    def matches(self, params):
        resp = self.app.get(f'{self.API_BASE}/matches/?{params}&format=json')
        return self.response_or_json(resp)

    def player(self, id, data=None, method='GET', expect_errors=False):
        url = f'{self.API_BASE}/players/{id}/?format=json'
        
        return self.request(
            url, data=data, method=method, expect_errors=expect_errors
        )

    def players(self, params, data=None, method='GET', expect_errors=False):

        url = f'{self.API_BASE}/players/?{params}&format=json'
        return self.request(
            url, data=data, method=method, expect_errors=expect_errors
        )

    def team(self, id, data=None, method='GET', expect_errors=False):
        url = f'{self.API_BASE}/teams/{id}/?format=json'
        
        return self.request(
            url, data=data, method=method, expect_errors=expect_errors
        )

    def teams(self, params, data=None, method='GET', expect_errors=False):
        
        url = f'{self.API_BASE}/teams/?{params}&format=json'
        return self.request(
            url, data=data, method=method, expect_errors=expect_errors
        )

    def join_team(self, id, data=None, method='POST', expect_errors=False):
        url = f'{self.API_BASE}/teams/{id}/join/?format=json'
        
        return self.request(
            url, data=data, method=method, expect_errors=expect_errors
        )
