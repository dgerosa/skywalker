# skywalker

#### Things I like in Python

This is a module which contains some of the things I like in python. I was tired of copying the same snippets over and over, so I put them in a module to be imported from everywhere.

## Installation

    pip install skywalker

## Usage

### skywalker.plot

This is a decorator to handle various matplotlib options, including saving the file to pdf. Just add `@skywalker.plot` to a function that returns a matplotlib figure object. If a list of figure objects is returned, save a single pdf with many pages.
    @skywalker.plot
    def test_plot():
        import matplotlib.pyplot as plt
        x=range(100)
        y=range(100)
        fig = plt.figure(figsize=(6,6))
        ax=fig.add_axes([0,0,1,1])
        ax.plot(x,y)
        return fig

### skywalker.timer

Decorator to print a function execution time to screen.
    @skywalker.timer
    def test_timer():
        return range(int(1e7))

### skywalker.checkpoint

Decorator to checkpoint the output of a function to hdf5 files. Add `@skywalker.checkpoint(filename)` before a function and the output will be stored to file and computed only if necessary. Function's args and kwargs can be put into the filename as well. Deeply inspired by the [ediblepickle](https://github.com/mpavan/ediblepickle) module. 
    def test_checkpoint():
    
        import time
    
        @skywalker.checkpoint('checkpoint',argvals=True)
        def long_calculation(x,arg=10):
            time.sleep(5)
            return x,arg
    
        print(long_calculation(2,arg=10))
        print(long_calculation(2,arg=10))
        print(long_calculation(1,arg=20))

### skywalker.singleton

Decorator to implement the [singleton pattern](https://en.wikipedia.org/wiki/Singleton_pattern) in Python. A single instance of the decorated class can exist at any time. If multiple instances are initiated, identical pointers are returned.  Here I use the [singleton_decorator](https://pypi.org/project/singleton-decorator/) module.

    def test_singleton():
    
        @skywalker.singleton
        class simple(object):
            def simple(self,x):
                return x
    
        s1=simple()
        s2=simple()
        print(s1,s2, s1==s2)

### skywalker.processify

Decorator to spawn a new process every time a function is called. Full credit for this incredibly nice piece of code goes to [schlamar](https://gist.github.com/schlamar/2311116).

    def test_processify():
    
        @skywalker.processify
        def tricky():
            return os.getpid()
    
        print(os.getpid(), tricky(), tricky())

### skywalker.dontprint

A context manager to suppress all printouts, both stdout and stderr. Full credit goes to [randlet](https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functionsorator).

```
def test_dontprint():

    def message():
        print("Function is printing")

    print("Main is printing")
    message()
    with skywalker.dontprint():
        message()
```

## Cite me

If you want to cite this code: [![DOI](https://zenodo.org/badge/134632789.svg)](https://zenodo.org/badge/latestdoi/134632789)




