import asyncio
from bleak import BleakScanner

class Device:
    address = ""
    name = ""
    is_paired = False
    is_connected = False
    services = {}
    
    def __init__(self, address:str):
        self.address = address
    
    async def __scan(self, timeout:int=5, detection_callback=None):
        if detection_callback != None:
            scanner = BleakScanner(detection_callback)
        else:
            scanner = BleakScanner()
        await scanner.start()
        await asyncio.sleep(5.0)
        await scanner.stop()
        return scanner.discovered_devices
    
    def scan(self, timeout:int=5, detection_callback=None) -> bool:
        discovered_devices = asyncio.run(self.__scan(timeout, detection_callback))
        for device in discovered_devices:
            print(f"Address: {device.address}\tName: {device.name}")
            if self.address == device.address:
                print("")

    def pair(self) -> bool:
        pass
    def unpair(self) -> bool:
        pass
    def connect(self) -> bool:
        pass
    def disconnect(self) -> bool:
        pass
    def start_notifications(self) -> bool:
        pass
    def stop_notifications(self) -> bool:
        pass
    def get_services(self) -> bool:
        pass
    def read_gatt(self, uuid:str=None) -> bool:
        pass
    def write_gatt(self, uuid:str, value):
        pass

class Bluetooth:
    devices = {}
    def __init__(self):
        pass
    def add_device(self, address:str) -> Device:
        device = Device(address)
        self.devices[address] = device
        return device
    def remove_device(self, address:str) -> bool:
        pass
    def print_devices(self):
        pass









# import asyncio
# from bleak import BleakScanner, BleakClient

# from typing import List

# class Bluetooth:
#     def __init__(self):
#         self.devices = None
#         self.is_connected = False
#         self.name = None
#         self.address = None
#         self.services = None
#         pass

#     async def __scan_async(self):
#         self.discovered_devices = await BleakScanner.discover()

#     def scan(self, verbosity:int=0, keyword:str=None):
#         self.is_scan_completed = False
#         self.discovered_devices = []
#         asyncio.run(self.__scan_async())
#         filtered_discovered_devices = []
#         for device in self.discovered_devices:
#             if (keyword != None) and (keyword in str(device)):
#                 filtered_discovered_devices.append(device)
#         self.discovered_devices = filtered_discovered_devices
#         for device in self.discovered_devices:
#                 if (verbosity > 0):
#                     print(device)
#         self.is_scan_completed = True
#         return None

#     # def __clear_name_and_address(self):
#     #     self.address = []
#     #     self.name = []
#     #     return None

#     # def __extract_name_and_address_by_keyword(self,keyword:str)->bool:
#     #     self.__clear_name_and_address()
#     #     for device in self.devices:
#     #         device = str(device)
#     #         if keyword in device:
#     #             (address, name) = device.split(": ")
#     #             self.address.append(address)
#     #             self.name.append(name)

#     #     return True

#     async def __connect(self, address):
#         self.client = BleakClient(address)
#         try:
#             await self.client.connect()
#             self.is_connected = True
#         #     model_number = await client.read_gatt_char(MODEL_NBR_UUID)
#         #     print("Model Number: {0}".format("".join(map(chr, model_number))))
#         except Exception as e:
#             self.is_connected = False
#             print(e)
#         # finally:
#         #     await client.disconnect()

#     def connect(self, name:str=None, address:str=None):
#         if (name==None) and (address==None):
#             print("Please provide a name or an address.")
#         if self.is_scan_completed == False:
#             self.scan()

#         #TODO: Add get_address_by_name
#         asyncio.run(self.__connect(address))
#         self.address = address

#     async def __read_characteristic(self, UUID):
#         async with BleakClient(self.address) as client:
#             self.characteristic_result = await client.read_gatt_char(UUID)

#     def read_characteristic_by_uuid(self, UUID:str)->str:
#         if self.is_connected == True:
#             asyncio.run(self.__read_characteristic(UUID))
#             return self.characteristic_result
#         else:
#             print("Connect before reading characteristics")
#             return ""

#     async def __get_services(self):
#         self.services = await self.client.get_services()

#     def report_services(self):
#         asyncio.run(self.__get_services())

#     def get_characteristic_uuid_by_name(self, name:str):
#         if self.services == None:
#             self.report_services()
        
#         for index in self.services.characteristics:
#             description = self.services.characteristics[index].description
#             uuid = self.services.characteristics[index].uuid
#             if name in description:
#                 return uuid

#         return None
        


# # class Bluetooth:
# #     devices = {}
# #     discovered_devices = None
# #     is_scan_completed = False
# #     def __init__(self):
# #         pass

# #     async def __scan_async(self):
# #         self.discovered_devices = await BleakScanner.discover()

# #     def scan(self, verbosity:int=0, keyword:str=None):
# #         self.is_scan_completed = False
# #         self.discovered_devices = []
# #         asyncio.run(self.__scan_async())
# #         filtered_discovered_devices = []
# #         for device in self.discovered_devices:
# #             if (keyword != None) and (keyword in str(device)):
# #                 filtered_discovered_devices.append(device)
# #         self.discovered_devices = filtered_discovered_devices
# #         for device in self.discovered_devices:
# #                 if (verbosity > 0):
# #                     print(device)
# #         self.is_scan_completed = True
# #         return None

# #     def connect(self, name:str=None, address:str=None):
# #         if (name==None) and (address==None):
# #             print("Please provide a name or an address.")
# #         if self.is_scan_completed == False:
# #             self.scan()

# #         #TODO: Add get_address_by_name
# #         current_device = Device(address)
# #         self.devices[address] = current_device
# #         current_device.connect()



# # class Device:
# #     is_scan_completed = False
# #     is_connected = False
# #     is_paired = False
# #     name = None
# #     address = None
# #     def __init__(self, address):
# #         self.address = address
# #         return None
# #     def pair(self):
# #         return None
# #     def unpair(self):
# #         return None

# #     async def __connect(self, address):
# #         self.client = BleakClient(address)
# #         try:
# #             await self.client.connect()
# #             self.is_connected = True
# #         #     model_number = await client.read_gatt_char(MODEL_NBR_UUID)
# #         #     print("Model Number: {0}".format("".join(map(chr, model_number))))
# #         except Exception as e:
# #             self.is_connected = False
# #             print(e)
# #         # finally:
# #         #     await client.disconnect()
# #     def connect(self):
# #         asyncio.run(self.__connect(self.address))
# #     def disconnect(self):
# #         return None
# #     def read_gatt(self, uuid:str=None, uuids=List[str], name=str, names=List[str]):
# #         return None