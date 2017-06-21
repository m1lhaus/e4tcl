# e4tcl

Simple company VCF contact generator from contact list stored in HTML format.

- pure Python 3
- Qt framework via PyQt5

## GUI

e4tcl has rich modern GUI based on Qt framework. It supports all Windows versions since WinXP and scales to custom DPI.

![e4tcl GUI](images/screen.PNG "e4tcl GUI")

## CLI

e4tcl also offers command line interface. Unfortunately no stdout output is provided for GUI executable due win32 limitations.


```
usage: e4tcl.py [-h] [-d] [-o OUTPUT] [input [input ...]]

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

## Download

For download, please refer to releases section. Available binary was build under Windows 7 targeting MSVCR14.

## Licence

GPL v3