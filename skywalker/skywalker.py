'''plotme: Python decorator to handle matplotlib options
See: https://github.com/dgerosa/plotme
'''

__author__ = "Davide Gerosa"
__email__ = "dgerosa@caltech.edu"
__license__ = "MIT"
__version__ = "0.0.3"
__doc__+="\n\n"+"Authors: "+__author__+"\n"+\
        "email: "+__email__+"\n"+\
        "Licence: "+__license__+"\n"+\
        "Version: "+__version__

from tqdm import tqdm
import warnings

def plot(function):
    '''Decorator to handle various matplotlib options, including saving the file to pdf. Just add @skywalker.plot to a function that returns a matplotlib figure object. If a list of figure objects is returned, save a single pdf with many pages.'''

    def wrapper(*args, **kwargs):
        print("skywalker: "+function.__name__+".pdf")

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
    '''Decorator to print a function execution time to screen.'''
    import contexttimer
    return contexttimer.timer()(function)



def checkpoint(key,tempdir=False,prefix=None,refresh=False):
    '''Python decorator to checkpointing to hdf5 files. Add @skywalker.checkpoint(key=filename) before a function and the output will be stored to file and computed only if necessary. Filename can be dynamic, see options of the ediblepickle module.'''

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
