

class FingerPrint:
    def __init__(self, _):
        self.octoapi = _

    async def get_renders(self, page_len: int = 100,  page: int = 0, os: str = 'win', os_arch: str = 'x86'):

        params = {
            'page_len': page_len,
            'page': page,
            'os': os,
            'os_arch': os_arch
        }

        response = await self.octoapi.session.get(
            url=f'{self.octoapi.base_url}/automation/fingerprint/renderers',
            params=params,
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True, 'renders': response.json()['data']}

        return {'status': False, 'msg': response.text}

    async def get_screens(self, os: str = 'win', os_arch: str = 'x86'):

        params = {
            'os': os,
            'os_arch': os_arch
        }

        response = await self.octoapi.session.get(
            url=f'{self.octoapi.base_url}/automation/fingerprint/screens',
            params=params,
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True, 'screens': response.json()['data']}

        return {'status': False, 'msg': response.text}
