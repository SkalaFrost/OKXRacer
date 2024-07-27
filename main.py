import aiohttp
import asyncio
import time
import os
import urllib.parse
import json
import colorama
from colorama import Fore, Style
import random
from fake_useragent import UserAgent

class OKX:
    def __init__(self, init_data):
        self.x_telegram_init_data, self.ext_user_id, self.ext_user_name = self.parse_init_data(init_data)
        self.last_check_in_time = None

    def parse_init_data(self, init_data):
        parsed_data = urllib.parse.parse_qs(init_data)
        user_data = parsed_data.get('user', [])[0]
        user_info = urllib.parse.unquote(user_data)

        try:
            user_info_dict = json.loads(user_info)
        except json.JSONDecodeError:
            raise ValueError('Error reading JSON')

        ext_user_id = user_info_dict.get('id', '')
        ext_user_name = user_info_dict.get('username', '')

        return init_data, ext_user_id, ext_user_name

    def get_random_user_agent(self):
        ua = UserAgent()
        return ua.random

    def headers(self):
        return {
            'Accept': '*/*',
            'Content-Type': 'application/json',
            'Origin': 'https://www.okx.com',
            'Referer': 'https://www.okx.com/mini-app/racer?tgWebAppStartParam=linkCode_104224440',
            'User-Agent': self.get_random_user_agent(),
            'X-Telegram-Init-Data': self.x_telegram_init_data
        }

    async def post_to_okx_api(self, session):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/info?t={int(time.time() * 1000)}'
        headers = self.headers()
        payload = {
            "extUserId": self.ext_user_id,
            "extUserName": self.ext_user_name,
            "gameId": 1,
            "linkCode": "104224440"
        }
        async with session.post(url, headers=headers, json=payload) as response:
            await self.check_response(response)
            return await response.json()

    async def assess_prediction(self, session, predict):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/assess?t={int(time.time() * 1000)}'
        headers = self.headers()
        payload = {
            "extUserId": self.ext_user_id,
            "predict": predict,
            "gameId": 1
        }
        async with session.post(url, headers=headers, json=payload) as response:
            await self.check_response(response)
            return await response.json()

    async def check_response(self, response):
        if response.status != 200:
            self.log(Fore.RED + f'Error {response.status}' + Style.RESET_ALL)
            response.raise_for_status()
        try:
            await response.json()
        except ValueError:
            self.log(Fore.RED + 'Error reading JSON' + Style.RESET_ALL)
            self.log(Fore.RED + f'Response: {await response.text()}' + Style.RESET_ALL)
            response.raise_for_status()

    async def check_task(self, session):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/tasks?extUserId={self.ext_user_id}&t={int(time.time() * 1000)}'
        headers = self.headers()
        async with session.get(url, headers=headers) as response:
            await self.check_response(response)
            tasks = (await response.json()).get('data', [])

        await asyncio.sleep(1)
        for task in tasks:
            task_id = task['id']
            task_status = task['state']
            task_title = task["context"]["name"]

            if task_status == 0:
                url_claim = f'https://www.okx.com/priapi/v1/affiliate/game/racer/task?t={int(time.time() * 1000)}'
                headers = self.headers()
                payload = {
                    "extUserId": self.ext_user_id,
                    "id": task_id
                }
                async with session.post(url_claim, headers=headers, json=payload):
                    await asyncio.sleep(1)

                in_task = next((task for task in tasks), None)

                if in_task:
                    if in_task['state'] == 0:
                        self.log(f"{Fore.LIGHTYELLOW_EX}Completed task '{task_title}' for {self.ext_user_name}!")

    async def boost(self, session):
        url = f'https://www.okx.com/priapi/v1/affiliate/game/racer/boosts?extUserId={self.ext_user_id}&t={int(time.time() * 1000)}'
        headers = self.headers()
        async with session.get(url, headers=headers) as response:
            await self.check_response(response)
            tasks = (await response.json()).get('data', [])
            boost = next((task for task in tasks if task['id'] == 1), None)

        await asyncio.sleep(1)
        if boost:
            if boost['state'] == 0:
                url_claim = f'https://www.okx.com/priapi/v1/affiliate/game/racer/boost?t={int(time.time() * 1000)}'
                headers = self.headers()
                payload = {
                    "extUserId": self.ext_user_id,
                    "id": 1
                }
                async with session.post(url_claim, headers=headers, json=payload):
                    self.log(f"{Fore.LIGHTYELLOW_EX}Used boost Reload Fuel Tank for {self.ext_user_name}!")

    def log(self, message):
        print(message)

    def log_without_prefix(self, message):
        print(message, end='\r')

    async def sleep(self, seconds):
        await asyncio.sleep(seconds)

    async def countdown(self, seconds):
        for i in range(seconds, 0, -1):
            await self.sleep(1)
        print()

    async def wait_with_countdown(self, seconds):
        for i in range(seconds, 0, -1):
            await self.sleep(1)
        print()

    async def process(self, session, predict=None):
        while True:
            try:
                await self.check_task(session)
                await asyncio.sleep(1)
                for _ in range(50):
                    response = await self.post_to_okx_api(session)
                    balance_points = response.get('data', {}).get('balancePoints', 0)

                    if predict is None or predict not in [0, 1]:
                        predict = random.randint(0, 1)
                    assess_response = await self.assess_prediction(session, predict)
                    assess_data = assess_response.get('data', {})
                    result = 'Win' if assess_data.get('won', False) else 'Lose'
                    calculated_value = assess_data.get('basePoint', 0) * assess_data.get('multiplier', 1)

                    output = f"""
{Fore.BLUE}Account {self.ext_user_name}{Style.RESET_ALL}
Balance: {Fore.LIGHTYELLOW_EX}{balance_points}{Style.RESET_ALL}
Result: {Style.BRIGHT}{result}{Style.RESET_ALL}
Received: {Fore.LIGHTYELLOW_EX}{calculated_value}{Style.RESET_ALL}

                    """.strip()
                    self.log_without_prefix(output)
                    if assess_data.get('numChance') == 1:
                        await self.boost(session)
                        await self.countdown(5)
                        break
                    if assess_data.get('numChance', 0) > 1:
                        await self.countdown(5)
                        continue
                    elif assess_data.get('secondToRefresh', 0) > 0:
                        await self.countdown(assess_data['secondToRefresh'] + 5)
                    else:
                        break
            except Exception as e:
                self.log(Fore.RED + f'Error: {str(e)}' + Style.RESET_ALL)
            await self.wait_with_countdown(60)

async def main():
    colorama.init(autoreset=True)
    async with aiohttp.ClientSession() as session:
        async with session.get("https://haiphan2.pythonanywhere.com/get/okx") as res:
            res = await res.json()
            init_data_list = res.get("response", "")

        tasks = [run_process(init_data.strip()) for init_data in init_data_list]
        await asyncio.gather(*tasks)

async def run_process(init_data):
    async with aiohttp.ClientSession() as session:
        okx = OKX(init_data)
        await okx.process(session)

if __name__ == '__main__':
    asyncio.run(main())
