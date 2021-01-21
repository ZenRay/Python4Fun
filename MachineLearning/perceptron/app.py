#coding:utf8
import numpy as np
from scipy.stats import norm


from bokeh.plotting import figure, output_file, show, curdoc, ColumnDataSource
from bokeh.layouts import row, column, widgetbox, layout, gridplot
from bokeh import palettes

size = 20
X = norm.rvs(size=(size, 3), random_state=42) * 2
# import ipdb; ipdb.set_trace()
X = np.dot(X, np.linalg.cholesky([[2, -1, 0], [-1, 2, -1], [0, -1, 2]]))


x = X[:, 0]
y = X[:, 1]
z = X[:, 2]

index = np.argsort(x)

x = x[index]
y = y[index]
z = z[index]
# 创建网格点
grid_x, grid_y = np.meshgrid(x, y)
value = np.nan * np.zeros(size)

space_colors = np.nan * np.zeros(size) # palettes.OrRd3[:2] # 超平面分隔颜色
dot_colors = np.nan * np.zeros(size) # palettes.Paired3[:2] # 区分正负例的颜色
# create datasource
source = ColumnDataSource(data=dict(x=x, y=y, z=z, value=value, grid_x=grid_x, \
    grid_y=grid_y, space_colors=space_colors, dot_colors=dot_colors))


# 创建制图对象
plot = figure(plot_height=800, plot_width=800, title="不同参数变化残差变化", \
    x_range=[min(min(x)*.1, min(x) * 1.5), max(max(x) * .2, max(x)*1.5)], \
    y_range=[min(min(y)*.1, min(y) * 1.5), max(max(y) * .2, max(y)*1.5)], \
    tooltips=[("x", "$x"), ("y", "$y"), ("value", "@contour")])

plot.scatter(x="x", y="y", color="navy", size=3, source=source)

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

# N = 500
# x = np.linspace(0, 10, N)
# y = np.linspace(0, 10, N)
# xx, yy = np.meshgrid(x, y)
# d = np.sin(xx)*np.cos(yy)

# p = figure(tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
# p.x_range.range_padding = p.y_range.range_padding = 0

# must give a vector of image data for image parameter
# p.image(image=[d], x=0, y=0, dw=10, dh=10, palette="Spectral11", level="image")
# p.grid.grid_line_width = 0.5

# output_file("image.html", title="image.py example")

curdoc().add_root(row(plot, width=800))