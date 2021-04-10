from collections import OrderedDict
from datetime import date

import gspread

from src.settings import SHEETS_NAME


class ExpenseSheet:
    def __init__(self):
        gc = gspread.service_account(filename="../creds.json")

        self.sheets = gc.open(SHEETS_NAME)
        self.sheet_data = self.sheets.worksheet("everyday_data")
        self.sheet_dicts = self.sheets.worksheet("dicts")

    def get_expense_groups(self) -> OrderedDict:
        dict_values = self.sheet_dicts.get("A2:F19")
        groups = OrderedDict()
        for row in dict_values:
            group = row.pop(0)
            groups[group] = row
        return groups

    def add_expense(
        self,
        name: str,
        value: int,
        group: str,
        subgroup: str = None,
        comment: str = None,
    ) -> None:

        self.sheet_data.append_row(
            [date.today().strftime("%d.%m.%Y"), name, group, subgroup, value, comment],
            table_range="A:F",
            value_input_option="USER_ENTERED",
        )


sheets = ExpenseSheet()
