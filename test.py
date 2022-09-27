import afpy

CWD = afpy.Formatter().path()

afpy.Generator().Mermaid(input_paths=[CWD],output_path=CWD)

print("Done")