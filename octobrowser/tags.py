

class Tags:
    def __init__(self, _):
        self.octoapi = _

    async def get_tags(self):
        response = await self.octoapi.session.get(
            url=f'{self.octoapi.base_url}/automation/tags',
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'success': True, 'tags': response.json()['data']}

        return {'success': False, 'msg': response.text}

    async def create_tag(self, name: str, color: str = 'grey'):
        json_data = {
            'name': name,
            'color': color,
        }

        response = await self.octoapi.session.post(
            url=f'{self.octoapi.base_url}/automation/tags',
            json=json_data
        )

        if response.status_code == 201:
            if response.json()['success'] is True:
                return {'success': True, 'tag': response.json()['data']}

        if response.status_code == 403:
            if response.json()['success'] is False:
                if 'msg' in response.json():
                    return {'success': False, 'msg': response.json()['msg']}

        return {'success': False, 'msg': response.text}

    async def remove_tag(self, uuid: str):
        response = await self.octoapi.session.delete(
            url=f'{self.octoapi.base_url}/automation/tags/{uuid}',
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'success': True}

        if response.status_code == 404:
            if response.json()['success'] is False:
                if 'msg' in response.json():
                    return {'success': False, 'msg': response.json()['msg']}

        return {'success': False, 'msg': response.text}

    async def update_tag(self, uuid: str, name: str, color: str = None):

        json_data = {
            'name': name,
            'color': color,
        }

        response = await self.octoapi.session.patch(
            url=f'{self.octoapi.base_url}/automation/tags/{uuid}',
            json=json_data
        )

        if response.status_code == 200:
            if response.json()['success'] is True:
                return {'success': True, 'tag': response.json()['data']}

        if response.status_code == 409:
            if response.json()['success'] is False:
                if 'msg' in response.json():
                    return {'success': False, 'msg': response.json()['msg']}

        return {'success': False, 'msg': response.text}