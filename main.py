import asyncio
import random

import httpx

from octobrowser.profiles import Profiles
from octobrowser.tags import Tags
from octobrowser.proxies import Proxies
from octobrowser.local_client import LocalClient
from octobrowser.init_cdp import ClientCDP
from octobrowser.fingerprint import FingerPrint


class Fields:
    def __init__(self):
        self.title = 'title'
        self.tags = 'tags'
        self.proxy = 'proxy'
        self.version = 'version'
        self.password = 'password'
        self.created_at = 'created_at'
        self.updated_at = 'updated_at'
        self.start_pages = 'start_pages'
        self.last_active = 'last_active'
        self.description = 'description'
        self.storage_options = 'storage_options'


class TagsColor:
    def __init__(self):
        self.green = 'green'
        self.yellow = 'yellow'
        self.purple = 'purple'
        self.orange = 'orange'
        self.blue = 'blue'
        self.grey = 'grey'
        self.cyan = 'cyan'
        self.red = 'red'


class OctoApi:
    def __init__(self, api_key: str, local_port: int = 58888):
        self.session = httpx.AsyncClient(
            headers={
                'X-Octo-Api-Token': api_key,
                'Content-Type': 'application/json',
            },
            timeout=360,
        )

        self.base_url = 'https://app.octobrowser.net/api/v2'
        self.local_url = f'http://localhost:{local_port}/api'

        self.fields = Fields()
        self.tags_color = TagsColor()

        self.tags = Tags(self)
        self.proxies = Proxies(self)
        self.cdp_client = ClientCDP()
        self.profiles = Profiles(self)
        self.fingerprint = FingerPrint(self)
        self.local_api = LocalClient(self)


async def main():
    random_render = random.choice((await octoapi.fingerprint.get_renders())['renders'])
    random_screen = random.choice((await octoapi.fingerprint.get_screens())['screens'])

    print(f'Benchmark API:')
    print(f'Random Render: {random_render}')
    print(f'Random Screen: {random_screen}')

    random_profile = await octoapi.profiles.create_profile()
    print(f'Random Profile: {random_profile}')

    response = await octoapi.local_api.set_profile_password(
        uuid=random_profile['uuid'],
        password='devbylords'
    )

    print(f'Set Password: {response}')

    response = await octoapi.local_api.delete_profile_password(
        uuid=random_profile['uuid'],
        password='devbylords'
    )

    print(f'Delete Password: {response}')

    response = await octoapi.profiles.update_profile(
        uuid=random_profile['uuid'],
        profile_data={
            'tags': ['kick'],
        }
    )

    print(f'Update Profile: {response}')

    response = await octoapi.profiles.get_profile(
        uuid=random_profile['uuid'],
    )

    print(f'Get Profile: {response}')

    start_profile = await octoapi.local_api.start_profile(
        uuid=random_profile['uuid'],
    )

    ws_endpoint = start_profile['profile']['ws_endpoint']

    client, browser = await octoapi.cdp_client.init_playwright_client_async(ws_endpoint)
    page = browser.contexts[0].pages[0]
    await page.goto('https://fv.pro/')
    await asyncio.sleep(10)

    await client.stop()

    active_profiles = await octoapi.local_api.get_active_profiles()
    for profile in active_profiles['profiles']:
        if profile['uuid'] == random_profile['uuid']:
            print('Account found in active Profiles!')

    #sync selenium
    driver = octoapi.cdp_client.init_selenium_client(debug_port=start_profile['profile']['debug_port'])
    driver.get('https://google.com/')

    await asyncio.sleep(3)

    response = await octoapi.local_api.stop_profile(
        uuid=random_profile['uuid'],
    )

    print(f'Stop Profile: {response}')

    response = await octoapi.profiles.delete_profile(
        uuids=random_profile['uuid'],
    )

    print(f'Delete Profile: {response}')

    response = await octoapi.tags.create_tag(
        name='devbylords',
        color=octoapi.tags_color.blue,
    )

    print(f'Create Tag: {response}')

    response = await octoapi.tags.update_tag(
        name='bebrik228',
        color=octoapi.tags_color.cyan,
        uuid=response['tag']['uuid'],
    )

    print(f'Update Tag: {response}')

    response = await octoapi.tags.remove_tag(
        uuid=response['tag']['uuid']
    )

    print(f'Delete Tag: {response}')


if __name__ == '__main__':
    octoapi = OctoApi(
        api_key='YOUR_API_KEY',
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
