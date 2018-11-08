# skywalker

Here below is a list of tools in `skywalker`.

## checkpoint
```python
checkpoint(key, argvals=False, tempdir=False, refresh=False, verbose=True)
```

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

## dontprint
```python
dontprint(self)
```

A context manager to suppress all printouts, both stdout and stderr. Full credit goes to [randlet](https://stackoverflow.com/questions/11130156/suppress-stdout-stderr-print-from-python-functionsorator). Example:

    def test_dontprint():
        def message():
            print("Function is printing")

        print("Main is printing")
        message()
        with skywalker.dontprint():
            message()

## plot
```python
plot(function)
```

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

## processify
```python
processify(func)
```

Decorator to spawn a new process every time a function is called. Full credit for this incredibly nice piece of code goes to [schlamar](https://gist.github.com/schlamar/2311116); for a nice description see [here](https://ys-l.github.io/posts/2015/10/03/processifying-bulky-functions-in-python).

    def test_processify():

        @skywalker.processify
        def tricky():
            return os.getpid()

        print(os.getpid(), tricky(), tricky())

## singleton
```python
singleton(*args, **kwargs)
```

Decorator to implement the [singleton pattern](https://en.wikipedia.org/wiki/Singleton_pattern) in Python. A single instance of the decorated class can exist at any time. If multiple instances are initiated, identical pointers are returned.  Here I use the [singleton_decorator](https://pypi.org/project/singleton-decorator/) module.

    def test_singleton():

        @skywalker.singleton
        class simple(object):
            def simple(self,x):
                return x

        s1=simple()
        s2=simple()
        print(s1,s2, s1==s2)

## timer
```python
timer(function)
```

Decorator to print a function execution time to screen. Example:

    @skywalker.timer
    def test_timer():
        x = range(int(1e7))

