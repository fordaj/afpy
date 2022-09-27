
"""
Services
----------------
An example showing how to fetch all services and print them.
Updated on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>
"""

import sys
import asyncio
import platform

from bleak import BleakClient

ADDRESS = (
    "24:71:89:cc:09:05"
    if platform.system() != "Darwin"
    else "EFB418F4-7CBD-86EC-C5DD-532ADC48DCD5"

)
ADDRESS = "EFB418F4-7CBD-86EC-C5DD-532ADC48DCD5"


async def main(address: str):
    async with BleakClient(address) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) == 2 else ADDRESS))