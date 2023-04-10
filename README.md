# swin (SoftWare INsights)

Simple analytics for PyPI packages based on `pypistats` (https://pypi.org/project/pypistats). In addition to daily downloads chart, `swin` adds a linear trend line and a summary stats table.

## Installation from PyPI

`pip install --upgrade swin`

## Command-Line Use

    swin [--help] [--version] [--ref REF] package [package ...]

    positional arguments:
      package     PyPI package names for processing

    options:
      -h, --help  show this help message and exit
      --version   show program's version number and exit
      --ref REF   reference comparison package

`swin` will create 'charts' folder (or use the existing one) in the current directory and put there one PNG file per input package with daily downloads chart and a trend over time.

`swin` will also print a sorted table with download statistics of the packages specified in the command line.

If `REF` package is specified then `swin` creates additional charts for the share of input packages in comparison with the reference comparison package (e.g. `modin` downloads as percentage of `pandas` downloads over time). These charts include a trendline as well and prefixed with `share-`.