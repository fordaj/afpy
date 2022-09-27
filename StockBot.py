import afpy

FORMATTER = afpy.Formatter()

IMPORTER = afpy.Importer()
ALPACA = IMPORTER.Alpaca(FORMATTER.path("/Users/andyford/Vault/Computers/Keys"), mode="paper")



print("Done")