# -*- coding:utf-8 -*-
import csv
import codecs
import os
from datetime import datetime

_encoding_str = 'utf-16-le'
_bom_head = '\ufeff'
_data_format = '%Y.%m.%d %H:%M'


def split_mt5_csv(file_path, op_folder):
    db = {}

    # 1. load file
    with codecs.open(file_path, 'rb', encoding='utf-16-le') as csv_file:
        reader = csv.reader(csv_file)

        # 1.1 get year from each row, to sort into different list
        for row in reader:
            # 1.2 the first row element format is: 2007.03.29 13:00
            d_str = row[0]

            # 1.3 remove BOM head in the utf-16 file
            if _bom_head in d_str:
                d_str = d_str.strip(_bom_head)
                row[0] = d_str

            # 1.4 convert str to time
            time = datetime.strptime(d_str,_data_format)

            # 1.4.1 if not exist, then creat the list
            if time.year not in db:
                db[time.year] = []
            
            db[time.year].append(row)


    # 2. analyze currency type & time type
    file_names = os.path.basename(file_path).split('.')
    money_type = file_names[0][0:6]
    time_type = file_names[0][6:]
    print("Split file_name=%s, money_type=%s, time_type=%s" % (file_names[0], money_type, time_type))

    # 3 first make sure folder is exist
    is_folder_exist = os.path.exists(op_folder)
    if not is_folder_exist:
        os.makedirs(op_folder)

    # 4. ouput each years' file
    for key, value in db.items():
        report_file_path = (op_folder + "%d_%s_%s.csv" ) % (key, money_type, time_type)
        with open(report_file_path, "w", encoding='utf-8') as op_csv_file:
            writer = csv.writer(op_csv_file)
            for row in value:
                writer.writerow(row)

