'''skywalker: Things I like in python
This is a module which contains some of the things I like in python. I was tired of copying the same snippets over and over, so I put them in a module to be imported from everywhere. See: https://github.com/dgerosa/skywalker
'''

from __future__ import print_function
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
import os
from tqdm import tqdm
from functools import wraps
from contexttimer import Timer
import datetime
import deepdish


if __name__!="__main__":
    __name__            = "skywalker"
__version__             = "0.0.12"
__description__         = "Things I like in python"
__license__             = "MIT"
__author__              = "Davide Gerosa"
__author_email__        = "dgerosa@caltech.edu"
__url__                 = "https://github.com/dgerosa/skywalker"


def plot(function):
    '''Decorator to handle various matplotlib options, including saving the file to pdf. Just add @skywalker.plot to a function that returns a matplotlib figure object. If a list of figure objects is returned, save a single pdf with many pages.'''

    def wrapper(*args, **kwargs):
        print("[skywalker.plot] "+function.__name__+".pdf")

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
    @wraps(function)
    def wrapper(*args, **kwargs):

        with Timer() as t:
            out =function(*args, **kwargs)

        print("[skywalker.timer] "+function.__name__+" "+str(datetime.timedelta(seconds=t.elapsed)))

        return out

    return wrapper



def checkpoint(key, argvals=False, tempdir=False, refresh=False,verbose=True):
    '''Decorator to checkpoint the output of a function to hdf5 files. Add @skywalker.checkpoint(key=filename) before a function and the output will be stored to file and computed only if necessary. Function's args and kwargs can be put into the filename as well. Deeply inspired by https://github.com/mpavan/ediblepickle.'''

    def decorator(func):

        if tempdir:
            if not os.path.exists('tmp'):
                os.makedirs('tmp')
            work_dir='./tmp'
        else:
            work_dir='.'


        def wrapped(*args, **kwargs):


            save_file = work_dir+"/"+key
            if argvals and args:
                save_file += "_"+"_".join(str(x) for x in args)
            if argvals and kwargs:
                save_file+="_"+"_".join(str(kwargs[x]) for x in kwargs)
            save_file=save_file+'.h5'

            if refresh or not os.path.exists(path=save_file):  # Otherwise compute it save it and return it.
                # If the program fails, don't checkpoint.
                try:
                    out = func(*args, **kwargs)
                except: # a blank raise re-raises the last exception.
                    raise
                else:  # If the program is successful, then go ahead and call the save function.
                    if verbose:
                        print('[skywalker.checkpoint] Save: '+save_file)
                    deepdish.io.save(save_file,out)
                    return out
            # Otherwise, load the checkpoint file and send it.
            else:
                if verbose:
                    print('[skywalker.checkpoint] Load: '+save_file)
                return deepdish.io.load(save_file)

        return wrapped

    return decorator


class dontprint(object):
    '''
    A context manager for doing a "deep suppression" of both stdout and stderr in
    Python. Credits: https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functions
    '''
    def __init__(self):
        # Open a pair of null files
        self.null_fds =  [os.open(os.devnull,os.O_RDWR) for x in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        self.save_fds = [os.dup(1), os.dup(2)]

    def __enter__(self):
        # Assign the null pointers to stdout and stderr.
        os.dup2(self.null_fds[0],1)
        os.dup2(self.null_fds[1],2)

    def __exit__(self, *_):
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(self.save_fds[0],1)
        os.dup2(self.save_fds[1],2)
        # Close all file descriptors
        for fd in self.null_fds + self.save_fds:
            os.close(fd)
