#!/usr/bin/env python3
import json
import sys
from tqdm import tqdm


SAMPLE = '../../data/Security_big_sample.json'


class Json2csv:
    def __init__(self, infile: str, outfile: str):
        self.headers = []
        self.header_idx = {}
        self.infile = infile
        self.outfile = outfile
        self.num_of_lines = 0
        self.delimeter = ':'
        self.csv_line = []
        self.enable_multiline = False
        self.is_no_column_needed = True

        if outfile != '':
            self.out = open(outfile, 'wt', encoding='UTF8')
        else:
            self.out = sys.stdout

    def __del__(self):
        if self.out != sys.stdout:
            self.out.close()

    def __build_headers_loop(self, j: dict, prefix=''):
        for k in j:
            v = j[k]
            header = k if prefix == '' else prefix + self.delimeter + k
            if isinstance(v, dict):
                self.__build_headers_loop(v, header)
            elif v is None:
                continue
            else:
                self.headers.append(header)

    def __build_headers(self):
        with open(self.infile, 'rt', encoding='UTF8') as f:
            for line in f:
                self.num_of_lines += 1
                j = json.loads(line)
                self.__build_headers_loop(j)

        self.headers = list(set(self.headers))
        self.headers.sort()
        if self.is_no_column_needed:
            self.headers.insert(0, 'No')
        for i in range(len(self.headers)):
            self.header_idx[self.headers[i]] = i

    def __json_to_csv(self, j: dict, prefix=''):
        for k in j:
            v = j[k]
            header = k if prefix == '' else prefix + self.delimeter + k
            
            if v is None:
                continue
            elif isinstance(v, dict):
                self.__json_to_csv(v, header)
            else:
                idx = self.header_idx[header]
                self.csv_line[idx] = f'{v}'.replace('"','\'')
                header = header.lower()

                if 'binarydatasize' not in header and 'binary' in header:
                    self.csv_line[idx] = f'\'{self.csv_line[idx]}\''

    def __write_csv_headers(self, out):
        # print headers
        str_headers = ','.join(f'"{s}"' for s in self.headers)
        print(str_headers, file=out)

    def __write_csv_contents(self, out):
        with open(self.infile, 'rt', encoding='UTF8') as f:
            for i, line in enumerate(
                tqdm(f, total=self.num_of_lines)
            ):
                self.csv_line = [''] * len(self.headers)
                if self.is_no_column_needed:
                    self.csv_line[0] = i + 1
                self.__json_to_csv(json.loads(line))
                print(','.join(f'"{s}"' for s in self.csv_line), file=out)

    def to_csv(self):
        # print contents
        self.__write_csv_headers(self.out)
        self.__write_csv_contents(self.out)

    def run(self):
        print(
            f'[+] Loading headers from all objects in file, {self.infile}',
            file=sys.stderr
        )
        self.__build_headers()
        print(
            f'[+] {len(self.header_idx)} headers were loaded.',
            file=sys.stderr
        )
        print(f'[+] Start to convert from JSON to CSV', file=sys.stderr)
        self.to_csv()


if __name__ == '__main__':
    tool = Json2csv('', SAMPLE, 'test1.csv')
    tool.run()
