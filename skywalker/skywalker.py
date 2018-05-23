'''plotme: Python decorator to handle matplotlib options
See: https://github.com/dgerosa/plotme
'''

__author__ = "Davide Gerosa"
__email__ = "dgerosa@caltech.edu"
__license__ = "MIT"
__version__ = "0.0.1"
__doc__+="\n\n"+"Authors: "+__author__+"\n"+\
        "email: "+__email__+"\n"+\
        "Licence: "+__license__+"\n"+\
        "Version: "+__version__

from tqdm import tqdm
import warnings

def skywalker(function):
    '''Python decorator to handle plotting, including defining all defaults and storing the final pdf. Just add @plotme before a function and return the matplotlib figure object(s).'''

    def wrapper():
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

        fig = function()
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
