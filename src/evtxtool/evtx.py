#!/usr/bin/env python3
import json
import sys


SAMPLE = '../../data/Security_big_sample.json'


class Json2csv:
    def __init__(self, conf_path: str, path: str, out: str):
        self.headers = []
        self.header_idx = {}
        self.input_filename = path
        self.out_filename = path
        self.num_of_lines = 0
        self.delimeter = ':'
        self.csv_line = []
        self.enable_multiline = False


    def __set_config(self, conf_path: str):
        if conf_path == '':
            return
        with open(conf_path, 'r') as f:
            conf = json.loads(f.read())
        
        for key in conf:
            self.__setattr__(key, conf[key])

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
        with open(self.input_filename, 'r') as f:
            for line in f:
                self.num_of_lines += 1
                j = json.loads(line)
                self.__build_headers_loop(j)

        self.headers = list(set(self.headers))
        self.headers.sort()
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
            # elif self.enable_multiline and \
            #     (isinstance(v, list) or isinstance(v, tuple)):
            #     self.csv_line[self.header_idx[header]] = '\n'.join(
            #         f'{s}' for s in v
            #     )
            else:
                idx = self.header_idx[header]
                self.csv_line[idx] = f'{v}'.replace('"','\'')
                header = header.lower()

                if 'binarydatasize' not in header and 'binary' in header:
                    self.csv_line[idx] = f'\'{self.csv_line[idx]}\''

    def to_csv(self):
        # print headers
        str_headers = ','.join(f'"{s}"' for s in self.headers)
        print(str_headers)

        # print contents
        i = 1
        with open(self.input_filename, 'r') as f:
            for line in f:
                self.csv_line = [''] * len(self.headers)
                self.csv_line[0] = i
                j = json.loads(line)
                self.__json_to_csv(j)
                print(','.join(f'"{s}"' for s in self.csv_line))
                i += 1

    def run(self):
        self.__build_headers()
        self.to_csv()
        

def json2csv(conf_path='', in_path='', out_path=''):
    tool = Json2csv('', in_path, out_path)
    tool.run()


if __name__ == '__main__':
    json2csv(in_path=SAMPLE)



"""
PWD = os.getcwd()
DATA_SHEET = 'rawdata'
TEMPLATE_FILENAME = f'{os.path.dirname(__file__)}/../data/template.xlsm'
TMP_FILENAME = f'{PWD}/tmp.xlsx'
ZF_TMP_PATH = f'{PWD}/_x_tmp'
OUTFILE_EXT = 'xlsm'


class EvtxRecord(object):
    def __init__(self):
        self._data = None

    def load_csv_file(self, filename):
        print(f'[|] {filename} file')
        _b = pd.read_csv(filename)
        self.df = _b if self.df is None else pd.concat([self.df, _b])

    def load_csv_files(self, path):
        os.chdir(path)
        files = list(filter(lambda x: x.find('.csv') != -1, os.listdir()))

        for fn in files:
            if os.path.isfile(fn) is False:
                print(f'{fn} not found')
                sys.exit(2)
            self.load_csv_file(fn)
    
    def save_to_xlsm_file(self, filename):
        with pd.ExcelWriter(TMP_FILENAME, engine='openpyxl') as wt:
            wb = openpyxl.load_workbook(TEMPLATE_FILENAME, keep_vba=True)
            wt.book = wb
            wt.sheets = dict((ws.title, ws) for ws in wb.worksheets)
            wt.vba_archive = wb.vba_archive

            self.df.to_excel(
                wt, sheet_name=DATA_SHEET, index=False, header=False, startrow=2
            )
            wt.save()

        with zipfile.ZipFile(TMP_FILENAME, 'r') as zf:
            zf.extractall(ZF_TMP_PATH)

        with zipfile.ZipFile(TEMPLATE_FILENAME, 'r') as zf:
            extracts = (
                '[Content_Types].xml',
                'xl/_rels/workbook.xml.rels',
                'xl/vbaProject.bin',
                'xl/sharedStrings.xml'
            )
            for fn in extracts:
                zf.extract(fn, path=ZF_TMP_PATH)

        with zipfile.ZipFile(filename, 'w') as zf:
            os.chdir(ZF_TMP_PATH)
            for root, dirs, files in os.walk('./'):
                for file in files:
                    zf.write(os.path.join(root, file))

        #clean
        rmtree(ZF_TMP_PATH)
        os.remove(f'{PWD}/tmp.xlsx')

    def merge(self):
        print(f'[*] sort dataframe')
        self.df = self.df.sort_values(
            by=['CVSS', 'NVT Name', 'IP', 'Port'],
            ascending=[False, True, True, True]
        ).reset_index(drop=True)
        self.df.insert(0, 'IDX', self.df.index + 1)

        headers = self.df.columns.values
        col_len, row_len = len(headers), len(self.df)
        print(f'[+] {row_len} x {col_len} table was loaded')


def merge_report(path, out):
    print(f'[+] load csv files and merge')
    report = Report()
    report.load_csv_files(path)
    
    report.merge()

    outfilename = f'{PWD}/'
    if out is not None:
        outfilename += f'{out}.{OUTFILE_EXT}'
    else:
        outfilename += datetime.date.today().strftime('%Y%m%d')
        outfilename += '-Monthly VA.xlsm'
        

    print(f'[*] Save report : {outfilename}')
    report.save_to_xlsm_file(outfilename)


# Backup Code
# with pd.ExcelWriter(f'{PWD}/test.xlsm', engine='openpyxl') as wt:
#     wb = openpyxl.load_workbook(TEMPLATE_FILENAME, keep_vba=True)
#     wt.book = wb
#     wt.sheets = dict((ws.title, ws) for ws in wb.worksheets)
#     wt.vba_archive = wb.vba_archive

#     sorted.to_excel(wt, sheet_name=DATA_SHEET, index=False, header=False, startrow=2)
#     wt.save()
"""