#-*-coding:utf8-*-
from __future__ import absolute_import
import visdom
import numbers
import numpy as np


class Visualizer(visdom.Visdom):
    """Visulaize Train Process

    """

    __line_opts = [
        "fillarea", 
        "markers", 
        "markersymbol", 
        "markersize", 
        "linecolor", 
        "dash", 
        "layoutopts", 
        "traceopts", 
        "webgl"
    ]
    def __init__(self, env="default", *, report_format=None, **kwargs):
        """

        Args:
        ------------
        env: string, it's Visdom env value
        report_format: format string, it's format the report text

        Properties:
        ------------
        xasix: store the x axis value, it's mapping value, key is window name,
            value is x axis ticks value that is updated, when plot done
        format_str: format string, it's the report text format that plot a text. 
            Default format is `{time}: {info}`
        """
        super().__init__(env=env, **kwargs)
        self.xaxis = {}
        self.format_str = "{time}: {info}" if report_format is None else report_format

    
    def reinit(self, env="default", **kwargs):
        """Adjust Configuration

        """
        self.close()
        super().__init__(env=env, **kwargs)
        self.xaxis = {}


    def _parse_kwargs(self, plot_type="line", **kwargs):
        """Parse Kwargs

        Parse the kwargs to get the different value of plot parameter env.

        Args:
        ---------
        plot_type: plot type, default line plot the line figure
        kwargs: plot keyword parameters

        Result:
        ---------
        opts: plot parameter opts values that is a dict
        kwargs: rest keyword parameters that can pass to the plot method
        """
        if plot_type == "line":
            args_list = self.__line_opts
        # TODO: Add another plot type option

        # parse opts arguments
        opts = {}
        for opt in args_list:
            if opt in kwargs:
                opts[opt] = kwargs.pop(opt)

        return opts, kwargs


    
    def plot(self, y, name, *, plot_type="line", **kwargs):
        """Plot Single Figure
        
        Plot the information, name is the Visdom window name, title.

        Args:
        -------
        y: numeric, it's a single value, then plot one line. If plot train line, 
            validate line on one figure, pass `(train_value, loss_value)`
        name: string, it's a import information, get and update the axix value 
            as key, specify the window name
        kwargs: it's Visdom parameter opts value and another parameter value
        """
        x = self.xaxis.get(name, -1)
        update = None if x == -1 else "append"

        plot_func = getattr(self, plot_type)
        # parse opts arguments
        opts, kwargs = self._parse_kwargs(plot_type, **kwargs)
        opts.update(title=name)
        
        # if the y length is one,  just plot one value; compare with the values 
        # if the y length is over one
        if isinstance(y, numbers.Number): # y is numeric value
            plot_func(Y=np.array([y]), X=np.array([x+1]),win=name, update=update, \
                opts=opts, **kwargs)
        elif len(y) == 1: # y is sequence
            plot_func(Y=np.array(y), X=np.array([x+1]),win=name, update=update, \
                opts=opts, **kwargs)
        else:
            Y = np.column_stack([[value] for value in y])
            X = np.column_stack([[x + 1] for _ in range(len(y))])

            # update opts with lengend value
            opts.update({"legend": ["Train", "Validate"]})
            plot_func(Y=Y, X=X, win=name, opts=opts, update=update, **kwargs)

        self.xaxis[name] = x + 1


    def multi_plot(self, data:dict, **kwargs):
        """Plot Multi-Figure

        Args:
        ----------
        data: dict, it's mapping data, key is name, value is y value. Then can 
            pass the key and value to plot function

        
        Examples:
        ----------
        If just plot train accuracy and f1 score:
        >>> data = {"accuracy": .2, "f1": .4}
        >>> multi_plot(data)

        If plots train and validate result, train value is forehead
        >>> data = {
                "accuracy": [np.random.randint(-20, 3000), np.random.randint(-20, 3000)],
                "f1": [np.random.randint(-200, 150), np.random.randint(-200, 230)]
            }
        >>> multi_plot(data)
        """
        for name, y in data.items():
            self.plot(y, name, **kwargs)

    
    def report(self, info, window="Log"):
        log = self.format_str.format(info)
        self.text(log, window)


    def __getattr__(self, name):
        return getattr(self, name)


"""Example
from utils import visualize
import numpy as np

vis = visualize.Visualizer2(report_format="{time}:{epoch}")

# plot train and validate result
data = {
    "accuracy": [np.random.randint(-20, 3000), np.random.randint(-20, 3000)],
    "f1": [np.random.randint(-200, 150), np.random.randint(-200, 230)]
}
vis.multi_plot(data)

# plot single result with plot method
data = .4
vis.plot(data, "accuracy")

# plot single result with multi_plot method
data = {"accuracy": np.random.randint(-5, 10)}
vis.multi_plot(data)

# plot more result with multi_plot method, like accuracy and f1
data = {
    "accuracy": np.random.randint(-5, 5),
    "f1": np.random.randint(-5, 4)
}
vis.multi_plot(data)
"""
