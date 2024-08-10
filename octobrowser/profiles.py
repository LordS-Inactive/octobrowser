import json


class Utils:
    @classmethod
    def generate_random_fingerprint(cls):
        return {
            'title': 'OctoAPI Profile',
            'description': 'OctoAPI Profile',
            'start_pages': [],
            'password': None,
            'tags': [],
            'proxy': None,

            'storage_options': {
                'cookies': True,
                'passwords': True,
                'extensions': True,
                'localstorage': True,
                'history': False,
                'bookmarks': True
            },

            'cookies': None,
            'image': '36fb48f4e99d47d3b18383d0c27feac2',
            'extensions': [],

            'fingerprint': {
                'os': 'win',

                'languages': {
                    'type': 'ip'
                },

                'timezone': {
                    'type': 'ip'
                },

                'geolocation': {
                    'type': 'ip'
                },

                'webrtc': {
                    'type': 'ip'
                },

                'dns': '1.1.1.1',

                'media_devices': {
                    'video_in': 1,
                    'audio_in': 1,
                    'audio_out': 1
                }
            }
        }


class Profiles:
    def __init__(self, _):
        self.octoapi = _

    async def create_profile(self, profile_data: dict | None = None):
        if profile_data is None:
            profile_data = Utils.generate_random_fingerprint()

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.base_url}/automation/profiles',
            json=profile_data,
        )

        if response.status_code == 201:
            if response.json()['success'] is True:
                return {'success': True, 'uuid': response.json()['data']['uuid']}
        return {'success': False, 'response': response.text}

    async def delete_profile(self, uuids: str | list):
        if type(uuids) is str:
            uuids = [uuids]

        json_data = {
            'uuids': uuids,
            'skip_trash_bin': False,
        }

        response = await self.octoapi.session.request(
            method='DELETE',
            url=f'{self.octoapi.base_url}/automation/profiles',
            content=json.dumps(json_data)
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True}
        if response.status_code == 404:
            if response.json()['success'] is False:
                if 'msg' in response.json():
                    return {'status': False, 'msg': response.json()['msg']}
                return {'status': False, 'msg': response.json()}
        return {'status': False, 'msg': response.text}

    async def update_profile(self, uuid: str, profile_data: dict = None):
        if profile_data is None:
            return {'success': False, 'msg': 'Data is None.'}

        #if type(profile_data) is dict:
        #    if 'start_pages' not in profile_data:
        #        profile_data['start_pages'] = []

        response = await self.octoapi.session.patch(
            url=f'{self.octoapi.base_url}/automation/profiles/{uuid}',
            json=profile_data,
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'success': True, 'uuid': response.json()['data']['uuid']}

        return {'success': False, 'response': response.text}

    async def get_profile(self, uuid: str):
        response = await self.octoapi.session.get(
            url=f'{self.octoapi.base_url}/automation/profiles/{uuid}',
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'success': True, 'profile': response.json()['data']}
        if response.status_code == 404:
            if response.json()['success'] is False:
                if 'msg' in response.json():
                    return {'status': False, 'msg': response.json()['msg']}

        return {'status': False, 'msg': response.text}

    async def get_profiles(
            self,
            search: str = None,
            search_tags: list = None,
            page_len: int = 100,
            page: int | list = 0,
            fields: list = None,
            ordering: str = 'active',
            status: int = None,
            password: bool = None,
            proxies: list = None
    ):

        params = {}

        if search:
            params['search'] = search
        if search_tags:
            params['search_tags'] = ','.join(search_tags)
        if page_len:
            params['page_len'] = page_len
        if fields:
            params['fields'] = ','.join(fields)
        if ordering:
            params['ordering'] = ordering
        if status is not None:
            params['status'] = status
        if password is not None:
            params['password'] = 'True' if password else 'False'
        if proxies:
            params['proxies'] = ','.join(proxies)

        if type(page) is int:
            if page is not None:
                params['page'] = page

            response = await self.octoapi.session.get(
                url=f'{self.octoapi.base_url}/automation/profiles',
                params=params,
            )

            if response.status_code == 200:
                if response.json()['success'] is True:
                    return {'status': True, 'profiles': response.json()['data']}

            return {'status': False, 'msg': response.text}

        else:
            profiles = []
            for _ in page:
                params['page'] = _

                response = await self.octoapi.session.get(
                    url=f'{self.octoapi.base_url}/automation/profiles',
                    params=params,
                )

                if response.status_code == 200:
                    if response.json()['success'] is True:
                        profiles += response.json()['data']

            return {'status': True, 'profiles': profiles}

    async def force_stop_profile(self, uuid: str):
        response = await self.octoapi.session.post(
            url=f'{self.octoapi.base_url}/automation/profiles/{uuid}/force_stop',
            json={'version': 1}
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True}
        if response.status_code == 409:
            if response.json()['success'] is False:
                return {'status': False, 'msg': response.json()['msg']}

        return {'status': False, 'msg': response.text}

    async def transfer_profile(self, email: str, uuids: str | list, with_proxy: bool = False):
        if type(uuids) is str:
            uuids = [uuids]

        json_data = {
            'uuids': uuids,
            'receiver_email': f'{email}',
            'transfer_proxy': with_proxy
        }

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.base_url}/automation/profiles/transfer',
            json=json_data,
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True}
        if response.status_code == 404:
            if response.json()['success'] is False:
                if 'msg' in response.json():
                    return {'status': False, 'msg': response.json()['msg']}

        return {'status': False, 'msg': response.text}

    async def import_cookies(self, uuid: str, cookies: str | dict | list):
        # Эта функция не обрабатывает, какой у вас тип куков, что вы отправите в cookies то и будет отправленно на сервер.
        json_data = {
            'cookies': cookies
        }

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.base_url}/automation/profiles/{uuid}/import_cookies',
            json=json_data,
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'status': True}
        if response.status_code == 400:
            if response.json()['success'] is False:
                if 'msg' in response.json():
                    return {'status': False, 'msg': response.json()['msg']}

        return {'status': False, 'msg': response.text}
