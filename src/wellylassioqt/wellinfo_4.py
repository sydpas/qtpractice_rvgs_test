import pandas as pd


def horz_loader():
    """
    This function reads a CSV file and pulls horizontal well information.
    """


    surv_1_7 = pd.read_csv('../csv_files/ss_1-7Surv.csv')

    df = pd.DataFrame({
        'UWI': surv_1_7['UWI'],
        'EW': surv_1_7['EW Offset'],
        'NS': surv_1_7['NS Offset'],
        'MD': surv_1_7['Measured Depth'],
        'TVD': surv_1_7['TVD'],
        'SS': surv_1_7['subsea']})

    return df