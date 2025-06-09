import pandas as pd


def horz_loader():
    """
    This function reads a CSV file and pulls horizontal well information.
    """


    surv_1_7 = pd.read_csv('../csv_files/1-7Surv.csv')

    df = pd.DataFrame({
        'EW': surv_1_7['EW Offset'],
        'MD': surv_1_7['Measured Depth'],
        'TVD': surv_1_7['TVD']})

    return df