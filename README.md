# evtxtool

## Prerequisites
* Python Version >= 3.6 (to use f-string)
* EVTX: https://github.com/omerbenamram/evtx.git

## Install

```bash
# git clone this repository
cd evtxtool
python setup.py build
python setup.py install
```

You should copy evtx_dump binary to src/bin directory ("src/bin/evtx_dump") before you run the setup.py if you want to run evtx2csv without the parameter "--evtx-bin"
* You can find evtx_dump binary on https://github.com/omerbenamram/evtx.git

## Commands
* evtx2csv
* json2csv