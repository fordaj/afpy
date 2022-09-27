import asyncio
from bleak import BleakClient

EPG0000_ADDRESS = "11DFCA97-5F80-8691-2B98-64B3DD8D6699"
MODEL_NBR_UUID = "00002902-0000-1000-8000-00805f9b34fb"

UUID_NAMES = {
    "00001801-0000-1000-8000-00805f9b34fb" : "Generic Attribute Service",
    "0000180a-0000-1000-8000-00805f9b34fb" : "Device Information Service",
    "e95d93b0-251d-470a-a062-fa1922dfa9a8" : "DFU Control Service",
    "e95d93af-251d-470a-a062-fa1922dfa9a8" : "Event Service",
    "e95d9882-251d-470a-a062-fa1922dfa9a8" : "Button Service",
    "e95d6100-251d-470a-a062-fa1922dfa9a8" : "Temperature Service",
    "e95dd91d-251d-470a-a062-fa1922dfa9a8" : "LED Service",
    "00002a05-0000-1000-8000-00805f9b34fb" : "Service Changed",
    "e95d93b1-251d-470a-a062-fa1922dfa9a8" : "DFU Control",
    "00002a05-0000-1000-8000-00805f9b34fb" : "Service Changed",
    "00002a24-0000-1000-8000-00805f9b34fb" : "Model Number String",
    "00002a25-0000-1000-8000-00805f9b34fb" : "Serial Number String",
    "00002a26-0000-1000-8000-00805f9b34fb" : "Firmware Revision String",
    "e95d9775-251d-470a-a062-fa1922dfa9a8" : "micro:bit Event",
    "e95d5404-251d-470a-a062-fa1922dfa9a8" : "Client Event",
    "e95d23c4-251d-470a-a062-fa1922dfa9a8" : "Client Requirements",
    "e95db84c-251d-470a-a062-fa1922dfa9a8" : "micro:bit Requirements",
    "e95dda90-251d-470a-a062-fa1922dfa9a8" : "Button A State",
    "e95dda91-251d-470a-a062-fa1922dfa9a8" : "Button B State",
    "e95d9250-251d-470a-a062-fa1922dfa9a8" : "Temperature",
    "e95d93ee-251d-470a-a062-fa1922dfa9a8" : "LED Text",
    "00002902-0000-1000-8000-00805f9b34fb" : "Client Characteristic Configuration",
}    

SPARK_EPG_SERVICE_UUID = "e0f506f6-25a8-11e9-ab14-d663bd873d93"
SPARK_EPG_CONTROL_POINT_CHR_UUID = "e0f5098a-25a8-11e9-ab14-d663bd873d93"
SPARK_EPG_DATA_CHR_UUID = "e0f50ad5-25a8-11e9-ab14-d663bd873d93"

THERMOMETER_EXAMPLE_ADDRESS = "EFB418F4-7CBD-86EC-C5DD-532ADC48DCD5"

address = EPG0000_ADDRESS

async def main(address):
    async with BleakClient(address) as client:
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print("Model Number: {0}".format("".join(map(chr, model_number))))

asyncio.run(main(address))