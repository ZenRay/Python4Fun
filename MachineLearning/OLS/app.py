#coding:utf8
import numpy as np
from scipy.stats import norm

from bokeh.io import push_notebook, show, output_notebook, curdoc
from bokeh.layouts import row, column, widgetbox, layout, gridplot
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import CustomJS, Select, Slider, TextInput, Spinner
from bokeh.models.glyphs import MultiLine
from bokeh.models.widgets import Div
from bokeh import palettes



size = 20
X = norm.rvs(size=(size, 2), random_state=42) * 2
X = np.dot(X, np.linalg.cholesky([[1, .8], [.8, .8]]))


x = X[:, 0]
y = X[:, 1]

index = np.argsort(x)
# import ipdb; ipdb.set_trace()
x = np.sort(x)
y = y[index]

pred = np.nan*np.zeros(len(X))
error = np.nan*np.zeros(len(X))
# 表示的是残差间的点
error_0s = [np.array(np.nan*np.zeros(2)) for i in range(0,len(X))]
error_1s = [np.array(np.nan*np.zeros(2)) for i in range(0,len(X))]
error_index = np.nan*np.zeros(len(X))
error_value = np.zeros(len(X))

error_colors = palettes.turbo(size)

# create datasource
source = ColumnDataSource(data=dict(x=x, y=y, pred=pred, error_0s=error_0s, \
    error_1s=error_1s, error_index=error_index, error_value=error_value, \
        color=error_colors))

# 显示原始点信息
plot = figure(plot_height=800, plot_width=800, title="不同参数变化残差变化", \
    x_range=[min(min(x)*.1, min(x) * 1.5), max(max(x) * .2, max(x)*1.5)], \
        y_range=[min(min(y)*.1, min(y) * 1.5), max(max(y) * .2, max(y)*1.5)])
plot.grid.visible = False

# 方差变化信息
var_plot = figure(plot_width=600, title="方差变化")


# 原始点
plot.scatter("x", "y", source=source, size=7, alpha=.6)
# 预测点
plot.scatter('x', 'pred', source=source, size=7, alpha=.8, color="#F8D90F")
plot.line("x", "pred", source=source, line_width=3, line_alpha=.6, line_color="#6A8372")

# 绘制残差线
glyph = MultiLine(xs="error_0s", ys="error_1s", line_color="color", line_width=2)
plot.add_glyph(source, glyph=glyph)

# 绘制方差信息
var_plot.vbar(x="error_index", top="error_value", width=.9, source=source, color="color")


# setup widgets
slope_slider = Slider(start=0, end=180, value=0, step=.05, title="斜率调整(角度)")

intercept_slider = Slider(title="截距", start=-10, end=10, value=0, step=.25)

def update_data(attrname, old, new):
    slope_angle = float(slope_slider.value)
    slope =  np.tan(slope_angle / 180 * np.pi)
    intercept = intercept_slider.value
    x = source.data['x']
    y = source.data['y']
    
    error_colors = source.data['color']
    # print(slope)

    # 更新预测信息和残差线
    pred = slope * x + intercept
    error_0s = list(zip(x, x))
    error_1s = list(zip(y, pred))

    # 更新方差信息
    error_index = range(len(X))
    error_value = np.power((pred - y), 2)

    source.data.update(dict(x=x, y=y, pred=pred, error_0s=error_0s, \
        error_1s=error_1s, error_index=error_index, error_value=error_value, \
            color=error_colors))

for w in [slope_slider, intercept_slider]:
    w.on_change("value", update_data)

# setup layouts and add to documents
inputs = column(slope_slider, intercept_slider, height=200)

curdoc().add_root(row(plot, column(inputs, var_plot, height=600), width=800))
