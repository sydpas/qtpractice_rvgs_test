import pandas as pd


def horz_loader():
    """
    This function reads a CSV file and pulls horizontal well information.
    """


    surv_1_7 = pd.read_csv('../csv_files/horz_1-7Surv.csv')

    df = pd.DataFrame({
        'UWI': surv_1_7['UWI'],
        'EW': surv_1_7['eoff'],
        'NS': surv_1_7['noff'],
        'MD': surv_1_7['MD'],
        'TVD': surv_1_7['tvd'],
        'SS': surv_1_7['ss']})


    return df