from datetime import datetime
import csv


class CsvWriter:
    def __init__(self, file, data):
        self.file = file + ".csv"
        header = sorted(data.keys())
        self.header = self.file_header(header)
        self.diff_header = False
        if self.header != header:
            self.file = file + datetime.now().strftime("%d%m%y%H%M%S") + ".csv"
            self.header = self.file_header(header)
            self.diff_header = True

        self.write_line(data)

    def file_header(self, header):
        try:
            with open(self.file, "r") as f:
                reader = csv.reader(f)
                for fileheader in reader:
                    return fileheader
        except FileNotFoundError:
            with open(self.file, mode='w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=header)
                writer.writeheader()
                return header

    def write_line(self, data):
        with open(self.file, "a", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.header)
            writer.writerow(data)
        if self.diff_header:
            print("Different header between data and file! Writting to alternative file.")
