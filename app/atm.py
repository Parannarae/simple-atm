from enum import Enum
from typing import Optional

from data.card import Card
from device_interface.bank_system import BankSystem
from device_interface.card_reader import CardReader
from device_interface.cash_bin import CashBin
from device_interface.display import Display
from device_interface.keypad import KeyPad

class ATM:
    MAX_RETRY_PIN = 5
    MAX_RETRY_MENU = 5

    class OpType(Enum):
        BALANCE = 1
        DEPOSIT = 2
        WITHDRAW = 3

    def __init__(self,
                 bank_system: BankSystem,
                 card_reader: CardReader,
                 display: Display,
                 keypad: KeyPad,
                 cash_bin: CashBin
                ):
        # connected device/server
        self.bank_system = bank_system
        self.card_reader = card_reader
        self.display = display
        self.keypad = keypad
        self.cash_bin = cash_bin

        self.current_card: Card = None
        self.current_account_num: str = None

    def read_card(self) -> bool:
        """Read card information from card_reader.

        Returns:
            true if a card is presented in the reader
        """
        card = self.card_reader.read_card()
        if card:
            self.current_card = card
            return True
        else:
            return False

    def read_and_validate_pin(self) -> bool:
        """Read pin from keypad and check if it is correct pin.

        Returns:
            True if the correct pin is given
        """
        authorized = False
        pin_attempt = 0
        while not authorized and pin_attempt < self.MAX_RETRY_PIN:
            self.display.display_str("Put your pin number")
            pin = self.keypad.read()
            authorized = self.bank_system.is_correct_pin(pin)
            pin_attempt += 1
        return authorized

    def select_account(self) -> bool:
        """Get an account number chosen by an user.

        Returns:
            True if the user choose an account
        """
        accounts = self.bank_system.get_accounts(self.current_card)
        select_attempt = 0
        while not self.current_account_num and select_attempt < self.MAX_RETRY_MENU:
            self.display.display_str(accounts)
            selected_num = self.keypad.read()
            if selected_num < len(accounts):
                self.current_account_num = accounts[selected_num]

            select_attempt += 1

        return self.current_account_num is not None

    def get_operation_menu(self) -> Optional['ATM.OpType']:
        """Get a transaction operation to be executed for the current account.

        Returns:
            The operation the user chosen
        """
        op = None
        select_attempt = 0
        while not op and select_attempt < self.MAX_RETRY_MENU:
            self.display.display_str(
                "1. Balance 2. Deposit 3. Withdraw"
            )
            selected_num = self.keypad.read()
            try:
                op = self.OpType(selected_num)
            except ValueError:
                pass

            select_attempt += 1

        return op

    def _show_balance(self):
        cur_balance = self.bank_system.get_balance(self.current_account_num)
        self.display.display_str(f"{self.current_account_num} balance: {cur_balance}")

    def _deposit(self):
        self.cash_bin.open_bin()
        self.display.display_str("Put money in to the bin and press any key.")
        self.cash_bin.close_bin()
        deposit_amount = self.cash_bin.count_money()

        self.bank_system.deposit(self.current_account_num, deposit_amount)

    def _withdraw(self):
        cur_balance = self.bank_system.get_balance(self.current_account_num)
        withdraw_attempt = 0
        while withdraw_attempt < self.MAX_RETRY_MENU:
            self.display.display_str("Amount to Withdraw: ")
            amount = self.keypad.read()
            if amount <= cur_balance:
                self.bank_system.withdraw(self.current_account_num, amount)
                self.cash_bin.withdraw_money(amount)
                self.cash_bin.open_bin()
                self.cash_bin.close_bin_if_empty()

    def execute_operation(self, op: 'ATM.OpType'):
        if op == self.OpType.BALANCE:
            self._show_balance()
        elif op == self.OpType.DEPOSIT:
            self._deposit()
            self._show_balance()

        elif op == self.OpType.WITHDRAW:
            self._withdraw()
            self._show_balance()

    def _clear_information(self):
        # reset current information before proceed to next iteration
        self.current_card = None
        self.current_account_num = None

    def run(self):
        turn_off = False
        while not turn_off:
            self.display.display_str("Insert your card")
            if self.read_card():
                authorized = self.read_and_validate_pin()
                if authorized:
                    if not self.select_account():
                        self._clear_information()
                        continue

                    op = self.get_operation_menu()
                    if not op:
                        self._clear_information()
                        continue

                    self.execute_operation(op)

            self._clear_information()







