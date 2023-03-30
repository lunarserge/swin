# swin (SoftWare INsights)

Simple analytics for PyPI packages based on `pypistats` (https://pypi.org/project/pypistats). In addition to daily downloads chart, `swin` adds a linear trend line and a summary stats table.

## Installation from PyPI

`pip install --upgrade swin`

## Command-Line Use

`swin [--help] [--version] packages`

`swin` will create 'charts' folder (or use the existing one) in the current directory and put there one PNG file per input package with daily downloads chart and a trend over time.

`swin` will also print a sorted table with download statistics of the packages specified in the command line.