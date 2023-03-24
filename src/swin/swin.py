#!python

'''
Software Insights main script.
'''

from datetime import timedelta
from prettytable import PrettyTable
import swin.opts as opts
from input import packages

def _print_summary():
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
    for p in packages:
        p.plot_downloads_with_trend()
        if p.ref:
            p.plot_downloads_share_with_trend()

    packages.sort(key=lambda package: package.total_downloads, reverse=True)
    _print_summary()
