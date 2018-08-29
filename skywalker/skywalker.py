'''skywalker: Things I like in python
This is a module which contains some of the things I like in python. I was tired of copying the same snippets over and over, so I put them in a module to be imported from everywhere. See: https://github.com/dgerosa/skywalker
'''

from __future__ import print_function
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")



if __name__!="__main__":
    __name__            = "skywalker"
__version__             = "0.0.5"
__description__         = "Things I like in python"
__license__             = "MIT"
__author__              = "Davide Gerosa"
__author_email__        = "dgerosa@caltech.edu"
__url__                 = "https://github.com/dgerosa/skywalker"


def plot(function):
    '''Decorator to handle various matplotlib options, including saving the file to pdf. Just add @skywalker.plot to a function that returns a matplotlib figure object. If a list of figure objects is returned, save a single pdf with many pages.'''

    def wrapper(*args, **kwargs):
        print("[skywalker.plot] "+function.__name__+".pdf")

        from tqdm import tqdm

        # Before function call
        global plt,AutoMinorLocator,MultipleLocator,LogLocator,NullFormatter,LogNorm
        with warnings.catch_warnings():
            warnings.simplefilter(action='ignore', category=UserWarning)
            from matplotlib import use #Useful when working on SSH
            use('Agg')
        from matplotlib import rc
        font = {'family':'serif','serif':['cmr10'],'weight' : 'medium','size' : 16}
        rc('font', **font)
        rc('text',usetex=True)
        #rc.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
        #rc('text.latex',preamble=r"\usepackage{amsmath}")
        import matplotlib
        matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
        rc('figure',max_open_warning=1000)
        rc('xtick',top=True)
        rc('ytick',right=True)
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from matplotlib.backends.backend_pdf import PdfPages
        from matplotlib.ticker import AutoMinorLocator,MultipleLocator,LogLocator,NullFormatter
        from matplotlib.colors import LogNorm
        pp= PdfPages(function.__name__+".pdf")

        fig = function(*args, **kwargs)
        # Handle multiple figures
        try:
            len(fig)
        except:

            fig=[fig]
        for f in tqdm(fig):

            # Filter our annoying "elementwise comparison failed" warning (something related to the matplotlib backend and future versions)
            with warnings.catch_warnings():
                warnings.simplefilter(action='ignore', category=FutureWarning)

                f.savefig(pp, format='pdf',bbox_inches='tight')
            f.clf()
        pp.close()
    return wrapper



def timer(function):
    from functools import wraps
    @wraps(function)
    def wrapper(*args, **kwargs):
        from contexttimer import Timer
        import datetime

        with Timer() as t:
            function(*args, **kwargs)

        print("[skywalker.timer] "+function.__name__+" "+str(datetime.timedelta(seconds=t.elapsed)))

    return wrapper


def checkpoint(key,tempdir=False,prefix=None,refresh=False):
    '''Decorator to checkpoint the output of a function to hdf5 files. Add @skywalker.checkpoint(key=filename) before a function and the output will be stored to file and computed only if necessary. Filename can be dynamic, see options of the ediblepickle module.'''

    import ediblepickle
    import deepdish
    import string

    def _checkpoint_pickler(object,f):
        deepdish.io.save(f.name,object)
        pass

    def _checkpoint_unpickler(f):
        object = deepdish.io.load(f.name)
        return object


    if tempdir:
        if not os.path.exists('tmp'):
            os.makedirs('tmp')
        work_dir='./tmp'
    else:
        work_dir='.'

    if prefix:
        key=str(prefix)+"_"+key
    key=key+'.h5'

    return ediblepickle.checkpoint(key = string.Template(key), work_dir=work_dir, refresh=refresh, pickler=_checkpoint_pickler, unpickler=_checkpoint_unpickler)


import singleton_decorator
singleton = singleton_decorator.singleton
'''Decorator to implement the singleton pattern. A single instance of a the decorated class can exist at any time. If multiple instances are initiated, identical pointers are return.  Here I use the singleton_decorator module.'''
