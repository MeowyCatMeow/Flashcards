"""
Flashcards
https://hyperskill.org/projects/127/stages/679/implement#comment
https://imgur.com/a/fO5NQRY
https://imgur.com/a/jzo1ZMd
"""
import random
import json
import argparse
from datetime import datetime


class Flashcards:
    def __init__(self):
        self.cards = {}
        self.log = []
        self.to_export = ''

    def print(self, message=''):
        self.log.append('SYSTEM: ' + message + '\n')
        print(message)

    def input(self, message=''):
        if message != '':
            self.print(message)
        term = input()
        self.log.append('USER: ' + term + '\n')
        return term

    def value_in(self, value):
        for _k in self.cards.keys():
            if value == self.cards[_k]['definition']:
                return _k

    def add_card(self):
        term = self.input('The card:')
        while term in self.cards.keys():
            term = self.input(f'The card "{term}" already exists. Try again:')
        definition = self.input(f'The definition of the card:')
        while self.value_in(definition):
            definition = self.input(f'The definition "{definition}" already exists. Try again:')
        self.cards[term] = {'definition': definition, 'error': 0}
        self.print(f'The pair ("{term}": "{definition}") has been added')

    def ask_card(self):
        ask_times = int(self.input('How many times to ask?'))
        for x in range(ask_times):
            random_key = random.choice(list(self.cards.keys()))
            answer = self.input(f'Print the definition of "{random_key}":')
            k = self.value_in(answer)
            if answer == self.cards[random_key]['definition']:
                self.print('Correct!')
            elif k:
                self.print(
                    f"Wrong. The right answer is \"{self.cards[random_key]['definition']}\", but your definition is correct for \"{k}\'s answer\".")
                self.cards[random_key]['error'] += 1
            else:
                self.print(f"Wrong. The right answer is \"{self.cards[random_key]['definition']}\".")
                self.cards[random_key]['error'] += 1

    def remove_card(self):
        card = self.input('Which card?')
        if card in self.cards:
            del self.cards[card]
            self.print('The card has been removed.')
        else:
            self.print(f'Can\'t remove "{card}": there is no such card.')

    def export_cards(self, f_name=''):
        if f_name == '':
            f_name = self.input('File name:')
        with open(f'{f_name}', 'w') as f:
            f.write(json.dumps(self.cards))
        self.print(f'{len(self.cards)} cards have been saved.')

    def import_cards(self, f_name=''):
        if f_name == '':
            f_name = self.input('File name:')
        try:
            with open(f_name, 'r') as j:
                temp_d = json.load(j)
                self.cards.update(temp_d)
            self.print(f'{len(temp_d)} cards have been loaded.')
        except FileNotFoundError:
            self.print('File not found.')

    def log_info(self):
        name = self.input('File name:')
        timestamp = datetime.now().strftime("%m/%d/%Y %I:%M:%S %p")
        with open(name, 'w') as f:
            for _l in self.log:
                f.write(f'{timestamp} {_l}')
        self.print('The log has been saved.')

    def hardest_card(self):
        times = 0
        card = []
        times = max((self.cards[k]['error'] for k in self.cards), default=0)
        for x in self.cards:
            if self.cards[x]['error'] == times:
                card.append(x)
        if times == 0:
            self.print('There are no cards with errors.')
        else:
            if len(card) == 1:
                self.print(f'The hardest card is "{card[0]}". You have {times} errors answering it')
            else:
                self.print('The hardest cards are ')
                for c in card:
                    if c != card[-1]:
                        self.print(f'"{c}", ')
                    else:
                        self.print(f'"{c}".')
                print(f' You have {times} errors answering it')

    def reset(self):
        for c in self.cards:
            self.cards[c]['error'] = 0
        self.print('Card statistics have been reset.')

    def arg(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--import_from')
        parser.add_argument('--export_to')
        args = parser.parse_args()
        to_import = args.import_from
        self.to_export = args.export_to
        if to_import:
            self.import_cards(to_import)

    def operate(self):
        self.arg()
        while True:
            action = self.input(
                'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):')
            if action == 'add':
                self.add_card()
            elif action == 'ask':
                self.ask_card()
            elif action == 'remove':
                self.remove_card()
            elif action == 'import':
                self.import_cards()
            elif action == 'export':
                self.export_cards()
            elif action == 'log':
                self.log_info()
            elif action == 'hardest card':
                self.hardest_card()
            elif action == 'reset stats':
                self.reset()
            elif action == 'exit':
                if self.to_export != '':
                    self.export_cards(self.to_export)
                self.print('Bye bye!')
                break
            else:
                self.print('No such command')


cards = Flashcards()
cards.operate()
