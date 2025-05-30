import pandas as pd


def top_load():
    """
    This function reads a CSV file and creates a list of all the well tops.

    Return:
        well_tops_list: list of all well tops from a CSV file.
    """
    well_tops = pd.read_csv('../csv_files/1506tops.csv')

    # print(well_tops.head())

    well_tops_list = []
    for _, row in well_tops.iterrows():  # iterrows is pandas
        tops = {column: row[column] for column in well_tops.columns
                if pd.notna(row[column]) and column != 'UWI'}  # notna skips NaN
        well_tops_list.append(tops)

    # print(f'well tops list: {well_tops_list}')

    return well_tops_list