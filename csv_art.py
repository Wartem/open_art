from pprint import pprint

import pandas as pd


def row_type(rows):
    types = {}
    for row in rows:
        temp_type = type(row).__name__
        if temp_type not in types:
            types[temp_type] = 1
        else:
            temp = types[temp_type]
            types[temp_type] = temp + 1
    return types


class Art_csv:

    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
        self.data = pd.read_csv(
            filepath, on_bad_lines="skip", index_col=False, dtype="unicode"
        )
        self.number_of_rows = self.data.shape[0]
        self.number_of_columns = self.data.shape[1]

    def resolve_column(self, name: str):
        """Return the actual column name matching name (case-insensitive, stripped), or None."""
        name = name.strip()
        for col in self.data.columns:
            if col.strip().lower() == name.lower():
                return col
        return None

    def has_column_unique_values(self, column):
        column_rows = self.data[column]
        c_set_len = column_rows.nunique()
        print("Unique values: ", c_set_len)
        num_rows = len(column_rows)
        print("Number of rows: ", num_rows)
        if c_set_len < num_rows:
            return False
        return True

    def all_row_types(self):

        all_types = []
        for column in self.data.columns:
            column_rows = self.data[column]

            types = row_type(column_rows)
            all_types.append([column, types])
        return all_types

    def get_column_data(self, column_name):
        if not column_name:
            return self.data.columns
        resolved = self.resolve_column(column_name)
        if resolved is None:
            return None
        if self.has_column_unique_values(resolved):
            print("The column has unique values.")
        else:
            print("The column does not have unique values.")
        return self.data[resolved]

    def report_data_info(self):

        row_info = self.all_row_types()

        num_type_in_cells = {}

        for item in row_info:
            for key, value in item[1].items():

                if key not in num_type_in_cells:
                    num_type_in_cells[key] = 1
                else:
                    num_type_in_cells[key] += 1

        info = "Information about " + self.filepath + "\n"
        info += "Number of colums: " + str(self.number_of_columns) + "\n"
        info += "Number of rows: " + str(self.number_of_rows) + "\n"

        for inf in num_type_in_cells.items():
            info += "\n"
            info += "Number of type " + inf[0] + ": " + str(inf[1])

        info += "\n" * 2
        info += "Below: Column name and number of types in the column"

        return [info, row_info]

    def print_report(self):

        pprint("-------------------------")
        report = self.report_data_info()
        print(report[0])

        dirty = []

        for item in report[1]:
            from_d = list(item)
            dict_d = str(from_d[1])
            print(
                from_d[0]
                + ": "
                + dict_d.replace("{", "")
                .replace(":", "")
                .replace("}", " times")
                .replace(",", " times and")
            )
            if len(item[1]) > 1:
                dirty.append(f"{item[0]} is dirty.\n")
        print("")
        print("".join(sorted(dirty)))
        pprint("-------------------------")


if __name__ == "__main__":
    print("Not standalone")
