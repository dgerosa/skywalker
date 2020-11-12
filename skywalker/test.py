'''
Here are some functions to test the `skywalker` tools. Run with e.g. `skywalker.test_something`.
'''

from __future__ import print_function
import os,sys
#if sys.version_info[0] > 2: # relative imports are different in python 2 and 3
#    import skywalker.skywalker as skywalker
#else:
import skywalker

@skywalker.plot
def test_plot():
    '''
    Test of `skywalker.plot`.
    '''

    import matplotlib.pyplot as plt
    x=range(100)
    y=range(100)
    fig = plt.figure(figsize=(6,6))
    ax=fig.add_axes([0,0,1,1])
    ax.plot(x,y)
    return fig

@skywalker.timer
def test_timer():
    '''
    Test of `skywalker.timer`.
    '''
    x= range(int(1e7))

def test_checkpoint():
    '''
    Test of `skywalker.checkpoint`.
    '''

    import time

    @skywalker.checkpoint('checkpoint',argvals=True)
    def long_calculation(x,arg=10):
        time.sleep(5)
        return x,arg

    print(long_calculation(2,arg=10))
    print(long_calculation(2,arg=10))
    print(long_calculation(1,arg=20))


def test_singleton():
    '''
    Test of `skywalker.singleton`.
    '''

    @skywalker.singleton
    class simple(object):
        def simple(self,x):
            return x

    s1=simple()
    s2=simple()
    print(s1,s2, s1==s2)


def test_processify():
    '''
    Test of `skywalker.processify`.
    '''

    @skywalker.processify
    def tricky():
        return os.getpid()

    print(os.getpid(), tricky(), tricky())



def test_dontprint():
    '''
    Test of `skywalker.dontprint`.
    '''

    def message():
        print("Function is printing")

    print("Main is printing")
    message()
    with skywalker.dontprint():
        message()



if __name__ == "__main__":

    #pass
    test_plot()
    #test_timer()
    #test_checkpoint()
    #test_singleton()
    #test_dontprint()
