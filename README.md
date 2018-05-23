# skywalker
Python decorator to handle matplotlib options

This is a simple python decorator to take care of importing matplotlib, set various rc values and save the pdf

### Installation

pip install skywalker

### Usage

Just add @skywalker to a function that returns a matplotlib figure object to save it to pdf. If a list of figure objects is return, save a single pdf with many pages.


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






