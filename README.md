The required modules must be installed before use.

`pip install httpx`
`pip install selenium`
`pip install playwright`
`pip install pyppeteer`


After just 

    octoapi = OctoApi(
       api_key='YOUR_API_KEY',
    ) 

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
