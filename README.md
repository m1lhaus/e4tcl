# dqcl vCard contact list generator

Simple company VCF contact generator from contact list stored in Excel files.

- Python 3
- [Pandas](https://pandas.pydata.org)
- [OpenPyXL](https://openpyxl.readthedocs.io)
- Qt framework via [PyQt5](https://pypi.org/project/PyQt5/)

## How to

### Download

Download the [latest windows binary version](https://nexus.dq.vwgroup.com/repository/dq-raw/DQD-tools/dqcl/dqcl.exe) from Nexus. The binary is unfortunately pretty huge since it likely contains big DLLs from dependencies and likely also MS runtime DDLs. I am too lazy to go though them and exclude them :) 

Alternatively clone the repo, install the dependencies and run `dqcl.py`.

### Export DQ contact list

Export the [contact list from the InfoPortal](https://infoportal.dq.skoda.vwg/APP/PBS/Lists/Kontakty/Employees.aspx). Just select "Export to Excel" button. Alternatively you can set custom filters and export custom subset of the list. The script query.iqy will be downloaded. Open the script and save created Excel table to XLSX. If needed, you can do this procedure for multiple custom exports resulting in more than one Excel files.

### Generate vCard contacts via GUI

dqcl has GUI based on Qt framework. It supports all Windows versions since WinXP and scales to custom DPI.

Open `dqcl.exe`, choose exported Excel files via Add and Generate the contact list.

![dqcl GUI](images/screen.PNG "dqcl GUI")

Simply use Add button to select Excel files with contacts you've exported from Infoportal. Optionally the app can generate contacts in old format for Nokia dumb phones.

### Generate vCard contacts via CLI

dqcl also offers command line interface. Unfortunately no stdout output is provided for GUI executable due win32 limitations.

```
usage: dqcl.py [-h] [-d] [-o OUTPUT] [input [input ...]]

positional arguments:
  input                 list of XLS files with contacts

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           enables debug logging
  -o OUTPUT, --output OUTPUT
                        output filepath of VCF file

```

## Requirements

- Python 3+
- PyQt 5+
- PyInstaller 3.2+ (for build)
- Pandas
- OpenPyXL

## Build

In order to build, use **vanilla Python distribution** and install only required packages from `requirements.txt`. If you use some custom distribution like anaconda, pyinstaller hooks might not find all packages correctly.

```
pyinstaller dqcl.spec
```

The binary will be built into `./dist` folder.
