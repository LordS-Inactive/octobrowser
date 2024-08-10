

class Proxies:
    def __init__(self, _):
        self.octoapi = _

    async def get_proxies(self):
        response = await self.octoapi.session.get(
            url=f'{self.octoapi.base_url}/automation/proxies'
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True, 'proxies': response.json()['data']}

        return {'status': False, 'msg': response.text}

    async def create_proxy(
        self,
        type: str,
        host: str,
        port: int,
        title: str,
        login: str = None,
        password: str = None,
        change_ip_url: str = None,
        external_id: str = None
    ):

        json_data = {
            'type': type,
            'host': host,
            'port': port,
            'title': title
        }

        if login:
            json_data['login'] = login
        if password:
            json_data['password'] = password
        if change_ip_url:
            json_data['change_ip_url'] = change_ip_url
        if external_id:
            json_data['external_id'] = external_id

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.base_url}/automation/proxies',
            json=json_data,
        )

        if response.status_code == 201:
            if response.json()['success'] is True:
                return {'status': True, 'proxy': response.json()['data']}

        return {'status': False, 'msg': response.text}

    async def remove_proxy(self, uuid: str):
        response = await self.octoapi.session.delete(
            url=f'{self.octoapi.base_url}/automation/proxies/{uuid}',
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True}

        return {'status': False, 'msg': response.text}

    async def update_proxy(
            self,
            uuid: str,
            type: str = None,
            host: str = None,
            port: int = None,
            login: str = None,
            password: str = None,
            title: str = None,
            change_ip_url: str = None,
            external_id: str = None
    ):
        proxy_data = {}

        if type:
            proxy_data['type'] = type
        if host:
            proxy_data['host'] = host
        if port:
            proxy_data['port'] = port
        if login:
            proxy_data['login'] = login
        if password:
            proxy_data['password'] = password
        if title:
            proxy_data['title'] = title
        if change_ip_url:
            proxy_data['change_ip_url'] = change_ip_url
        if external_id:
            proxy_data['external_id'] = external_id

        if not proxy_data:
            return {'success': False, 'msg': 'No data provided to update'}

        response = await self.octoapi.session.patch(
            url=f'{self.octoapi.base_url}/automation/proxies/{uuid}',
            json=proxy_data
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True}
        if response.status_code == 404:
            if response.json()['success'] is False:
                return {'status': False, 'msg': response.json()['msg']}

        return {'status': False, 'msg': response.text}
