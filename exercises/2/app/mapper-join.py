#!/usr/local/bin/python
import sys

def process_line(line):
    record = line.strip('\n').split(',')
    values = []
    for value in record:
        stripped_value = value.strip('"')
        values.append(stripped_value)
    return values

def read_csv_file(filepath):
    with open(filepath,'r') as f:
        lines = f.readlines()
        # print(f'lines: {lines}')
        records = []
        for line in lines:
            record = process_line(line)
            records.append(record)
        return records[1:]

processes = read_csv_file('processes.csv')
# print(f'process records: {processes}')

for line in sys.stdin:
    image = process_line(line)
    image_process_id = image[8]
    # print(f'image_process_id: {image_process_id}')
    for process in processes:
        # print(f'process_id: {process[0]}')
        process_id = process[0]
        if process_id == image_process_id:
            image += process[1:]
            print(f"{process_id}\t{','.join(image)}")
        break
    