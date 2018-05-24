# skywalker
Things I like in python

This is a module which contains some of the things I like in python. I was tired of copying the same snippets over and over, so I put them in a module to be imported from everywhere.

### Installation

pip install skywalker

### Usage

#### skywalker.plot

This is a decorator to handle various matplotlib options, including saving the file to pdf. Just add @skywalker.plot to a function that returns a matplotlib figure object. If a list of figure objects is returned, save a single pdf with many pages.

    import matplotlib.pyplot as plt
    import skywalker

    @skywalker.plot
    def test_plot():

        x=range(100)
        y=range(100)
        fig = plt.figure(figsize=(6,6))
        ax=fig.add_axes([0,0,1,1])
        ax.plot(x,y)

        return fig


### Updates
If you want to cite this code:

**v0.0.1**  [![DOI](https://zenodo.org/badge/134632789.svg)](https://zenodo.org/badge/latestdoi/134632789)




