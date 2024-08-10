import asyncio
import json


class LocalClient:
    def __init__(self, _):
        self.octoapi = _

    async def start_profile(self, uuid: str, headless: bool = False, debug_port: bool = True,
                            only_local: bool = None, flags: list = None, timeout: int = 360,
                            password: str = None):

        json_data = {
            'uuid': uuid,
            'headless': headless,
            'debug_port': debug_port,
            'flags': flags if flags else [],
            'timeout': timeout,
        }

        if password is not None:
            json_data['password'] = password

        if only_local is not None:
            json_data['only_local'] = only_local

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.local_url}/profiles/start',
            json=json_data,
        )

        if response.status_code == 200:
            if 'ws_endpoint' in response.json():
                return {'status': True, 'profile': response.json()}

        return {'status': False, 'msg': response.text}

    async def stop_profile(self, uuid: str):

        json_data = {
            'uuid': uuid,
        }

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.local_url}/profiles/stop',
            json=json_data,
        )

        if response.status_code == 200:
            if response.json()['msg'] == 'Profile stopped':
                return {'status': True}

        return {'status': False, 'msg': response.text}

    async def force_stop_profile(self, uuid: str):
        json_data = {
            'uuid': uuid,
        }

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.local_url}/profiles/force_stop',
            json=json_data,
        )

        if response.status_code == 200:
            if response.json()['msg'] == 'Profile stopped successfully':
                return {'status': True}

        return {'status': False, 'msg': response.text}

    async def one_time_profile(self, title: str = 'OctoAPI TempProfile', fingerprint: dict = None,
                               flags: list = None, timeout: int = 360, headless: bool = False, debug_port: bool = True):

        #Потому что я бомж, я не могу проверить работает ли эта функция как надо

        if fingerprint is None:
            fingerprint = {
                'os': 'win'
            }

        json_data = {
            'profile_data': {
                'title': title,
                'fingerprint': fingerprint,
            },
            'headless': headless,
            'debug_port': debug_port,
            'flags': flags if flags else [],
            'timeout': timeout
        }

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.local_url}/profiles/one_time/start',
            json=json_data,
        )

        if response.status_code == 200:
            if 'ws_endpoint' in response.json():
                return {'status': True, 'profile': response.json()}

        return {'status': False, 'msg': response.text}

    async def set_profile_password(self, uuid: str, password: str):
        json_data = {
            'uuid': uuid,
            'password': password,
        }

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.local_url}/profiles/password',
            json=json_data,
        )

        if response.status_code == 200:
            if response.json()['msg'] == 'Profile password has been set':
                return {'status': True}

        return {'status': False, 'msg': response.text}

    async def delete_profile_password(self, uuid: str, password: str):
        json_data = {
            'uuid': uuid,
            'password': password,
        }

        response = await self.octoapi.session.request(
            method='DELETE',
            url=f'{self.octoapi.local_url}/profiles/password',
            content=json.dumps(json_data)
        )

        if response.status_code == 200:
            if response.json()['msg'] == 'Profile password has been cleared':
                return {'status': True}

        return {'status': False, 'msg': response.text}

    async def get_active_profiles(self):
        response = await self.octoapi.session.get(
            url=f'{self.octoapi.local_url}/profiles/active',
        )

        if response.status_code == 200:
            return {'status': True, 'profiles': response.json()}

