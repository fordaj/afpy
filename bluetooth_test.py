import afpy


iphone_address = '5B249B07-94DB-71DE-16AD-81B2730DD1F2'
BATTERY_SERVICE = '00002a19-0000-1000-8000-00805f9b34fb'

BT = afpy.Communicator().Bluetooth()
IPHONE = BT.add_device(iphone_address)
IPHONE.scan()
IPHONE.connect()
IPHONE.read_gatt(by_name="Battery Level")
IPHONE.read_gatt(by_name="Battery Level")
IPHONE.read_gatt(uuid='00002a19-0000-1000-8000-00805f9b34fb')



# BP05 =                      '99EFB9E6-0917-88C1-3D83-8CB1BCE43FF3'
# UUID_MANUFACTURER_NAME =    '00002a29-0000-1000-8000-00805f9b34fb'
# UUID_BATTERY_LEVEL =        '00002a19-0000-1000-8000-00805f9b34fb'

# IPHONE = '5B249B07-94DB-71DE-16AD-81B2730DD1F2'
# BATTERY_SERVICE = '00002a19-0000-1000-8000-00805f9b34fb'




# import asyncio
# from bleak import BleakClient

# address = IPHONE
# MODEL_NBR_UUID = BATTERY_SERVICE

# async def main(address):
#     async with BleakClient(address) as client:
#         services = await client.get_services()
#         print(services)
#         print(services.characteristics)
#         model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         print("Model Number: {0}".format("".join(map(chr, model_number))))

# asyncio.run(main(address))



CM_BT = afpy.Communicator().Bluetooth()
CM_BT.scan(keyword="Andy")
CM_BT.connect(address=IPHONE)
CM_BT.report_services()
print(CM_BT.read_characteristic_by_uuid(BATTERY_SERVICE))


# CM_BT.connect_by_mac_address(BP05)


# #UUID_MANUFACTURER_NAME = CM_BT.get_characteristic_uuid_by_name("Manufacturer Name")
# print(CM_BT.read_characteristic_by_uuid(UUID_MANUFACTURER_NAME))

# #UUID_BATTERY_LEVEL = CM_BT.get_characteristic_uuid_by_name("Battery Level")


print("")