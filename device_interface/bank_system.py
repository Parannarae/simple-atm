from typing import List

from data.card import Card

class BankSystem:
    def __init__(self):
        # bank system connection code
        self.bank_system = None

    def is_correct_pin(self, pin_input: str) -> bool:
        raise NotImplementedError

    def get_accounts(self, card: Card) -> List[str]:
        raise NotImplementedError

    def get_balance(self, account_number: str) -> str:
        raise NotImplementedError

    def deposit(self, account_number: str, amount: int):
        raise NotImplementedError

    def withdraw(self, account_number: str, amount: int):
        raise NotImplementedError