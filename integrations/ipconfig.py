import aiohttp


async def get_my_ip() -> str:
    """
        Get  your public ip address
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('https://ifconfig.me/ip') as response:
            return await response.text()
