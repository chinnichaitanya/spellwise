from spell_checker import Typox

suggester = Typox()
suggester.add_from_path("examples/data/american-english")

suggestions = suggester.get_suggestions("hallo")
print(suggestions)
