'''
Software package descriptors.
'''

import os
import statistics
from numpy.polynomial.polynomial import Polynomial
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from numerize import numerize
import pandas as pd
import pypistats
import swin.opts as opts

# Using synodic month which is the most common definition.
MONTHS = (opts.end_date-opts.start_date).days / 29.53059

PYPI = 'PyPI'

class Package:
    '''
    Base software package descriptor.
    This is a superclass for actual registry-specific imlementations.
    There should be no objects of this class itself.
    '''

    @property
    def registry(self):
        '''
        To keep Pylint happy.
        '''
        raise AssertionError('There should be no objects of base Package class')

    def compute_downloads(self):
        '''
        To keep Pylint happy.
        '''
        raise AssertionError('There should be no objects of base Package class')

    def __init__(self, pid, title, *, ref=None):
        '''
        Create a software package descriptor.
        'pid'   is an engineering package name (e.g., its name on a registry).
        'title' is a user-friendly description (e.g., for putting on charts).
        'ref'   is the reference comparison package.
        '''
        self.__pid = pid
        self.__title = title
        self.__ref = ref
        self.__downloads = self.compute_downloads()

        self.__total_downloads = sum(self.__downloads)
        self.__trend = Polynomial(Polynomial.fit(opts.ticks, self.__downloads, 1).convert().coef)

    @property
    def pid(self):
        '''
        Get package engineering name.
        '''
        return self.__pid

    @property
    def title(self):
        '''
        Get package user-friendly description.
        '''
        return self.__title

    @property
    def ref(self):
        '''
        Get package's reference comparison package.
        '''
        return self.__ref

    @property
    def downloads(self):
        '''
        Get package downloads over time.
        '''
        return self.__downloads

    @property
    def total_downloads(self):
        '''
        Get total number of package downloads.
        '''
        return self.__total_downloads

    def compute_average_downloads(self, start_date, end_date):
        '''
        Compute average daily number of package downloads between two dates (end date included).
        '''
        index = (start_date - opts.start_date).days
        count = (end_date - start_date).days + 1
        return round(statistics.mean(self.__downloads[index:index+count]))

    def compute_monthly_trend(self):
        '''
        Compute montly package downloads trend in percents.
        '''
        growth_ratio = self.__trend(opts.ticks[-1]) / self.__trend(opts.ticks[0])
        return (growth_ratio ** (1 / MONTHS) - 1) * 100

    def plot_downloads_with_trend(self):
        '''
        Draw a chart of package downloads over time (with a linear trend).
        '''
        fig, axes = plt.subplots()
        axes.set_title(self.__title + ' / ' + self.registry)
        axes.set_ylabel('daily downloads')
        axes.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, pos: numerize.numerize(x)))

        axes.scatter(opts.dates, self.__downloads)
        axes.plot(opts.dates, self.__trend(opts.ticks), color='r')

        fig.savefig(os.path.join(opts.CHART_FOLDER, self.pid))

    def plot_downloads_share_with_trend(self):
        '''
        Draw a chart of package downloads over time as a percentage of
        the reference comparison package downloads (with a linear trend).
        '''
        fig, axes = plt.subplots()
        axes.set_title(self.__title + ' as % of ' + self.__ref.title + ' / ' + self.registry)
        axes.yaxis.set_major_formatter(mtick.PercentFormatter())

        # Protect from glitches of having zero downloads on a particular day.
        share = list(map(lambda p,r: (p/r if r else p) * 100, self.downloads, self.__ref.downloads))

        axes.plot(opts.dates, share)
        trend = Polynomial(Polynomial.fit(opts.ticks, share, 1).convert().coef)
        axes.plot(opts.dates, trend(opts.ticks), color='r')

        fig.savefig(os.path.join(opts.CHART_FOLDER, 'share-'+self.pid))

class PyPIPackage(Package):
    '''
    PyPI package descriptor.
    '''

    @property
    def registry(self):
        '''
        Get the package registry that this package associates with (i.e., PyPI).
        '''
        return PYPI

    def compute_downloads(self):
        '''
        Get PyPI package download numbers.
        '''
        # May want to fix pypistats 'mirrors=False' bug and rewrite the below.
        print('Loading data for', self.title)
        data = pypistats.overall(self.pid,
            start_date=str(opts.start_date), end_date=str(opts.end_date),
            total=True, format='pandas')
        data = data.groupby('category').get_group('without_mirrors')

        # Add missing dates that have zero number of downloads and sort by date along the way.
        data['date'] = pd.to_datetime(data['date'])
        data.set_index('date', inplace=True)
        data = data.reindex(pd.date_range(opts.start_date, opts.end_date), fill_value=0)
        return list(data['downloads'])

class PackageSet(Package):
    '''
    Descriptor for a set of packages that require combined statistics.
    '''

    def __init__(self, pid, title, packages, *, ref=None):
        '''
        Create a descriptor for a set of packages that require combined statistics.
        'pid'      is an engineering ID for the set of packages.
        'title'    is a user-friendly description (e.g., for putting on charts).
        'packages' is a list of packages that form the set.
        'ref'      is the reference comparison package.
        '''
        self.packages = packages
        super().__init__(pid, title, ref=ref)

    @property
    def registry(self):
        '''
        Get the package registry that this set of packages associates with.
        '''
        return self.packages[0].registry

    def compute_downloads(self):
        '''
        Get combined download numbers for this set of packages.
        '''
        res = []
        for i in range(len(self.packages[0].downloads)):
            res.append(sum((p.downloads[i] for p in self.packages)))
        return res
