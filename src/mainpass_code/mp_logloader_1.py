import lasio
import os


def mainpass_well(file_path):
    """
    This function reads an LAS file and prints various information.

    Returns:
         columns: length of non_depth_curves list.
         non_depth_curves: list of curves without depth.
         curve_unit_list: list of all curve units excluding depth.
         df: the LAS file converted to a pandas DataFrame.
    """
    las = lasio.read(os.path.abspath(file_path))

    df = las.df()  # converting to pandas dataframe
    df['DEPTH'] = df.index  # adding depth column
    # print(f'df describe: {df.describe()}')  # prints stats

    curve_list = las.curves
    # print(f'curve list: {curve_list}')

    # mapping curve mnemonic to descrip
    curve_name_dict = {curve.mnemonic: curve.descr for curve in las.curves}
    # print(f'dictionary: {curve_name_dict}')

    # making list of units
    curve_unit_list = {curve.mnemonic: curve.unit for curve in las.curves if curve.mnemonic != 'DEPT'}
    # print(f'units: {curve_unit_list}')

    non_depth_curves = [
        curve_name.mnemonic for curve_name in curve_list if curve_name.mnemonic != 'DEPT'
            and curve_name.mnemonic in df.columns]
    # removing the DEPT curve

    columns = len(non_depth_curves)


    loc = las.well.LOC.value if 'LOC' in las.well else None
    comp = las.well.COMP.value if 'COMP' in las.well else None
    kb = las.params['EREF'].value if 'EREF' in las.params else None
    # print(f'LAS KB value: {kb}')

    # depth to ss
    df['SUBSEA'] = 824 - df['DEPTH']
    df[['DEPTH', 'SUBSEA']].reset_index()  # turns depth into normal column

    df['DT'] = df['DT'].clip(upper=450)  # trimming DT
    df['ILD'] = df['ILD'].clip(upper=30)  # trimming DT

    # print(f'dt lims: {df['DT'].min(), df['DT'].max()}')

    return columns, non_depth_curves, curve_unit_list, df, loc, comp, kb
