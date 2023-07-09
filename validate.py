# Made and tested using Python 3.11.3
import tomli_w
import tomllib
from itertools import permutations

class GlossaryCheck:
    def __init__(self, input_file):
        self.input_file = input_file
        self.data = self.load()

    def load(self):
        with open(self.input_file, 'rb') as toml_file:
            data = tomllib.load(toml_file)
        return data

    def check_permutations(self):
        for definition in self.data['definition']:
            word = definition['word']
            if '/' in word:
                aliases = definition.get('aliases', '').split(', ')
                word_permutations = ['/'.join(perm) for perm in permutations(word.split('/'))]
                missing_permutations = set(word_permutations) - set(aliases) - {word}
                if missing_permutations:
                    print(f'Missing permutations in aliases of the word "{word}": {", ".join(missing_permutations)}')

    def check_toml_keys(self):
        valid_keys = ('word', 'aliases', 'definition')
        for definition in self.data['definition']:
            for key in definition.keys():
                if key not in valid_keys:
                    raise Exception(f"Unexpected key '{key}' in the definition of the word '{definition['word']}'")

    def sort_alphabetical(self):
        sorted_definitions = sorted(self.data['definition'], key=lambda d: d['word'])
        self.data['definition'] = sorted_definitions
        with open('glossary_sorted.toml', 'wb') as toml_file:
            tomli_w.dump(self.data, toml_file)
            print('Created "glossary_sorted.toml"')


if __name__ == "__main__":
    handler = GlossaryCheck('glossary.toml')
    handler.check_permutations()
    handler.check_toml_keys()
    handler.sort_alphabetical()
    print('Finished')
