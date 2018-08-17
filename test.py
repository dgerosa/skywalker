from __future__ import print_function
import skywalker

@skywalker.plot
def test_plot():
    import matplotlib.pyplot as plt
    x=range(100)
    y=range(100)
    fig = plt.figure(figsize=(6,6))
    ax=fig.add_axes([0,0,1,1])
    ax.plot(x,y)
    return fig

#@skywalker.timer

@skywalker.timer
def test_timer():
    return range(int(1e7))

def test_checkpoint():

    @skywalker.checkpoint('checkpoint_{0}_${arg}')
    def long_calculation(x,arg=10):
        return range(int(1e7))

    long_calculation(2,arg=10)
    long_calculation(2,arg=10)
    long_calculation(1,arg=20)

if __name__ == "__main__":

    pass
    test_plot()
    test_timer()
    test_checkpoint()
