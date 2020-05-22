import xlrd
import json
from collections import OrderedDict
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--excel_path', required=True)
    parser.add_argument('--foldername', required=True)
    config = parser.parse_args()

    _excel = xlrd.open_workbook(config.excel_path, on_demand=False, encoding_override='cp949')
    sheet = _excel.sheet_by_name("Sheet1")

    _json = OrderedDict()

    row_count = sheet.nrows
    for index in range(0, row_count):
        value = sheet.row_values(index)[0]
        string_index = str(index).zfill(4)
        key = "./datasets/" + config.foldername + "/audio/Raw." + string_index + ".wav"
        _json[key] = value

    with open("./datasets/" + config.foldername + '/recognition.json', 'w') as f:
        json.dump(_json, f, indent=2, ensure_ascii=False)

    _excel.release_resources()
    del _excel