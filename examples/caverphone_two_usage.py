from spellwise import CaverphoneTwo

suggester = CaverphoneTwo()
suggester.add_from_path("examples/data/american-english")

suggestions = suggester.get_suggestions("hallo")
print(suggestions)
