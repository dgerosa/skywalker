'''
Here below is a list of tools in `skywalker`.
'''

from __future__ import print_function
import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
import os, sys, traceback
from tqdm import tqdm
from functools import wraps
from contexttimer import Timer
import datetime
import deepdish
import singleton_decorator
from functools import wraps
from multiprocessing import Process, Queue



if __name__!="__main__":
    __name__            = "skywalker"
__version__             = "0.0.17"
__description__         = "Things I like in python"
__license__             = "MIT"
__author__              = "Davide Gerosa"
__author_email__        = "dgerosa@caltech.edu"
__url__                 = "https://github.com/dgerosa/skywalker"


def plot(function):
    '''
    This is a decorator to handle various matplotlib options, including saving the file to pdf. Just add `@skywalker.plot` to a function that returns a matplotlib figure object. If a list of figure objects is returned, save a single pdf with many pages. Example:

        @skywalker.plot
        def test_plot():
            import matplotlib.pyplot as plt
            x=range(100)
            y=range(100)
            fig = plt.figure(figsize=(6,6))
            ax=fig.add_axes([0,0,1,1])
            ax.plot(x,y)
            return fig
    '''

    @wraps(function)
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
        matplotlib.rcParams['text.latex.preamble']=r"\usepackage{amsmath}"
        rc('figure',max_open_warning=1000)
        rc('xtick',top=True)
        rc('ytick',right=True)
        rc('ytick',right=True)
        rc("axes", grid=False)
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
    '''
    Decorator to print a function execution time to screen. Example:

        @skywalker.timer
        def test_timer():
            x = range(int(1e7))
    '''

    @wraps(function)
    def wrapper(*args, **kwargs):

        with Timer() as t:
            out =function(*args, **kwargs)

        print("[skywalker.timer] "+function.__name__+" "+str(datetime.timedelta(seconds=t.elapsed)))

        return out

    return wrapper



def checkpoint(key, argvals=False, tempdir=False, refresh=False,verbose=True):
    '''
    Decorator to checkpoint the output of a function to hdf5 files. Add `@skywalker.checkpoint(filename)` before a function and the output will be stored to file and computed only if necessary. Deeply inspired by the [ediblepickle](https://github.com/mpavan/ediblepickle) module. Example:

        def test_checkpoint():
            import time
            @skywalker.checkpoint('checkpoint',argvals=True)
            def long_calculation(x,arg=10):
                time.sleep(5)
                return x,arg

            print(long_calculation(2,arg=10))
            print(long_calculation(2,arg=10))
            print(long_calculation(1,arg=20))

    Options are:

    - `argvals`. If True all args will be listed in the file name. If False (default), none of them will. If, e.g., [0,3] only the first and the fourth arg/kwarg will be listed.
    - `refresh`. If True, disable checkpointing
    - `tempdir`. If True, store in `./tmp`
    '''

    def decorator(func):

        if tempdir:
            if not os.path.exists('tmp'):
                os.makedirs('tmp')
            work_dir='./tmp'
        else:
            work_dir='.'

        @wraps(func)
        def wrapped(*args, **kwargs):


            save_file = work_dir+"/"+key

            if argvals==False:
                pass

            elif argvals==True:
                if args:
                    save_file += "_"+"_".join(str(x) for x in args)
                if kwargs:
                    save_file+="_"+"_".join(str(kwargs[x]) for x in kwargs)

            else:
                for x in argvals: # this is in args
                    if len(args)>x:
                        save_file += "_"+str(args[x])
                    else:
                        save_file += "_"+str(kwargs[list(kwargs.keys())[x-len(args)]])

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
    A context manager to suppress all printouts, both stdout and stderr. Full credit goes to [randlet](https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functionsorator). Example:

        def test_dontprint():
            def message():
                print("Function is printing")

            print("Main is printing")
            message()
            with skywalker.dontprint():
                message()
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


def processify(func):
    '''
    Decorator to spawn a new process every time a function is called. Full credit for this incredibly nice piece of code goes to [schlamar](https://gist.github.com/schlamar/2311116); for a nice description see [here](https://ys-l.github.io/posts/2015/10/03/processifying-bulky-functions-in-python).

        def test_processify():

            @skywalker.processify
            def tricky():
                return os.getpid()

            print(os.getpid(), tricky(), tricky())
    '''

    def process_func(q, *args, **kwargs):
        try:
            ret = func(*args, **kwargs)
        except Exception:
            ex_type, ex_value, tb = sys.exc_info()
            error = ex_type, ex_value, ''.join(traceback.format_tb(tb))
            ret = None
        else:
            error = None

        q.put((ret, error))

    # register original function with different name
    # in sys.modules so it is pickable
    process_func.__name__ = func.__name__ + 'processify_func'
    setattr(sys.modules[__name__], process_func.__name__, process_func)

    @wraps(func)
    def wrapper(*args, **kwargs):
        q = Queue()
        p = Process(target=process_func, args=[q] + list(args), kwargs=kwargs)
        p.start()
        ret, error = q.get()
        p.join()

        if error:
            ex_type, ex_value, tb_str = error
            message = '%s (in subprocess)\n%s' % (ex_value.message, tb_str)
            raise ex_type(message)

        return ret
    return wrapper



def singleton(*args, **kwargs):
    '''
    Decorator to implement the [singleton pattern](https://en.wikipedia.org/wiki/Singleton_pattern) in Python. A single instance of the decorated class can exist at any time. If multiple instances are initiated, identical pointers are returned.  Here I use the [singleton_decorator](https://pypi.org/project/singleton-decorator/) module.

        def test_singleton():

            @skywalker.singleton
            class simple(object):
                def simple(self,x):
                    return x

            s1=simple()
            s2=simple()
            print(s1,s2, s1==s2)
    '''

    return singleton_decorator.singleton(*args, **kwargs)
