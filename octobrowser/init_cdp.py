from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

import pyppeteer


class ClientCDP:
    @staticmethod
    def init_selenium_client(debug_port: int, driver_path: str = 'undetected_chromedriver.exe',
                             options: webdriver.ChromeOptions = None):
        if options is None:
            options = webdriver.ChromeOptions()
            options.page_load_strategy = 'normal'

        options.add_experimental_option(
            'debuggerAddress', f'127.0.0.1:{debug_port}')

        return webdriver.Chrome(service=Service(driver_path), options=options)

    @staticmethod
    async def init_playwright_client_async(ws_endpoint: str):
        client = await async_playwright().start()
        return client, await client.chromium.connect_over_cdp(ws_endpoint)

    @staticmethod
    def init_playwright_client_sync(ws_endpoint: str):
        client = sync_playwright().start()
        return client, client.chromium.connect_over_cdp(ws_endpoint)

    @staticmethod
    async def init_pyppeteer_client_async(ws_endpoint: str):
        return await pyppeteer.launcher.connect(browserWSEndpoint=ws_endpoint)