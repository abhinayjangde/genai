from pathlib import Path

# print(Path(__file__).parent)
# print(Path.cwd())
# print(Path.home())

# file = Path("README.md")
# file.write_text("automating works")
# print(file.read_text())

for item in Path(".").iterdir():
    print(f"{item}: {item.is_dir()}")