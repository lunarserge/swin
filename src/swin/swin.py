#!python

'''
Software Insights main script.
'''

from argparse import ArgumentParser
from datetime import timedelta
from prettytable import PrettyTable
from swin import opts
from swin.package import PyPIPackage

VERSION = '0.0.4'

def _print_summary(packages):
    '''
    Prints a summary across packages.
    '''
    print('\nSummary for ', opts.start_date, ' - ', opts.end_date, ':\n', sep='')
    print(packages[0].registry, 'packages by download number:')
    table = PrettyTable([
        'Package',
        'Total',
        'Daily (last month)',
        'Daily (pre-last month)',
        'Daily (6 months back)',
        'Average Monthly Growth'])
    for package in packages:
        table.add_row([
            package.title, package.total_downloads,
            package.compute_average_downloads
                (opts.end_date-timedelta(29), opts.end_date),
            package.compute_average_downloads
                (opts.end_date-timedelta(59), opts.end_date-timedelta(30)),
            package.compute_average_downloads
                (opts.start_date, opts.start_date+timedelta(29)),
            f'{package.compute_monthly_trend():.2f}%'])
    table.align = 'r'
    print(table)

def main():
    '''
    CLI entry
    '''
    parser = ArgumentParser(description='Simple analytics for PyPI packages based on `pypistats`')
    parser.add_argument('--version', action='version', version='%(prog)s '+VERSION)
    parser.add_argument('package', nargs='+', help='PyPI package names for processing')
    packages = [PyPIPackage(p) for p in parser.parse_args().package]

    for package in packages:
        package.plot_downloads_with_trend()
# Will add CLI for ref packages later
#       if package.ref:
#           package.plot_downloads_share_with_trend()

    packages.sort(key=lambda package: package.total_downloads, reverse=True)
    _print_summary(packages)
