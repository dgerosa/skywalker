import matplotlib.pyplot as plt
from skywalker import skywalker

@skywalker
def test():

    x=range(100)
    y=range(100)
    fig = plt.figure(figsize=(6,6))
    ax=fig.add_axes([0,0,1,1])
    ax.plot(x,y)

    return fig

if __name__ == "__main__":

    pass
    test()
