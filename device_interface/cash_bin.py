class CashBin:
    def __init__(self):
        self.cash_bin_system = None

    def open_bin(self):
        raise NotImplementedError

    def close_bin(self):
        raise NotImplementedError

    def close_bin_if_empty(self):
        raise NotImplementedError

    def count_money(self) -> int:
        """Return an amount inside the bin.
        """
        raise NotImplementedError

    def withdraw_money(self, amount):
        raise NotImplementedError