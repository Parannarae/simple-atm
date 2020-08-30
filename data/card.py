class Card:
    def __init__(self, card_number: str):
        self.card_number = card_number

    def __repr__(self):
        return f'Card(card_number={self.card_number})'