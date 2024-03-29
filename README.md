**Description:**

There are some fun exercise done, and those are Python.

**Table Of Content:**

[TOC]

## 1. [ImgToChar](./ImgToChar)

Convert the image pixel information to char.

### 1.1 File

```bash
├── imgToChar.py
├── result
└── test
    └── dora.png
```

There are two directors, one is `result` that stores the result, the other is `test` that stores the test image file.

### 1.2 Description

Run the python script file `imgToChar.py` directly, like `python imgToChar.py -f test/dora.png --width 80 --height 80`.

## 2. [ScrapyGitHubRepo](./CrawlWeb)

Crawl the user's repo information, like repo name and latest update time. Run the crawl project, likes:

```bash
cd CrawlWeb
scrapy crawl github
```

Besides, there is some interactive information.

### 2.1 Requirements

There are some packages required:

* scrapy
* time
* pandas

## 3. [movieCrawl](./movieCrawl)

Crawl the DouBan Top250 movie, you can run the script, like `python douban.py`.

## 4. [loggerConfig](./loggerConfig)

Use configuration file to setup logger. There are some default FORMATTERS and HANDLERS configuration `conf` file that can be parsed with [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) .

### 4.1 Requirements

There are some packages required:

* pyhocon

### 4.2 Usage Case

There is a [example](./loggerConfig/__init__.py): 

```python
import logging
import logging.config

conf = create_logger_conf(log_path="log.log")
logger_conf = {
    "loggerss": {
        "sample": {
            "handlers": ["console", "file"],
            "level": "INFO"
        }
    }
}
conf.update(logger_conf)
logging.config.dictConfig(conf)

# now can set logger `sample`
sample = logging.getLogger("sample")
sample.info("This is test message")
```

## 4. [PytorchVisualization](./PytorchVisualization)

It’s a customize script([visualize](./PytorchVisualization/visualize.py)) to display **pytorch** training progress, which is used the package `visdom`.

**Caution:** it does plot line.

**TODO:**

- [x] Line plot
  - [x] Single Line plot
  - [x] Multi-line plot
- [ ] Text plot
- [ ] Image 
- [ ] Video

### 4.1 Tutorial

Right now, it can plot one single line, multi-line on one figure, multi-line on different figure. When plot train and validate result, the train value is forehead.

```python
# import package
from utils import visualize
import numpy as np

# Initialization 
vis = visualize.Visualizer2(report_format="{time}:{epoch}")

# plot train and validate result
for _ in range(4):
    data = {
        "accuracy": [np.random.randint(-20, 3000), np.random.randint(-20, 3000)],
        "f1": [np.random.randint(-200, 150), np.random.randint(-200, 230)]
    }
    vis.multi_plot(data)

# plot single result with plot method
for _ in range(4):
  data = np.random.randint(-5, 10)
  vis.plot(data, "accuracy")

# plot single result with multi_plot method
for _ in range(4):
    data = {"accuracy": np.random.randint(-5, 10)}
    vis.multi_plot(data)

# plot more result with multi_plot method, like accuracy and f1
for _ in range(4):
    data = {
        "accuracy": np.random.randint(-5, 5),
        "f1": np.random.randint(-5, 4)
    }
    vis.multi_plot(data)
```

### 5. [multiThreadExample](./multiThreadExample)

Multi-threading example, there are two thread: one is used to extract data item `ExtractorThread`, the other is predict sentiment item `PredictThread`. The thread class example:

```python
class NamedThread(threading.Thread):
    def __init__(self, filename, mode, **kwargs):
      	"""Initalize Property"""
        self.filename = filename
        self.mode = mode
        super().__init__(**kwargs)

    def deal_method(self):
      	"""Deal With Data Item Method"""
        global ITEM_QUEUE, RETRY_TIME
        retry = 0 # retry times
        logger.info(f"Start predict thread")
        while retry <= RETRY_TIME:
            try:
                item = ITEM_QUEUE.get(timeout=3)
                
                text = item["clean_text"]
                tokens = model.prepross(text)
                item["predict"]  = model.predict(tokens) if len(tokens) else (1, 0, 0, 0)

                # write data
                fhandler = FileWriter(self.filename, mode=self.mode)
                with fhandler as writer:
                    writer.write(json.dumps(item, ensure_ascii=False) + "\n")

                logger.debug(f"Predict item id is {item['id']}")
                
                # if get item right, re_initial retry
                retry = 0
            except queue.Empty:
                logger.debug(f"Queue is empty, wait 1 seconds.")
                retry -= 1
                time.sleep(1)
        
        # exhausted RETRY_TIME
        logger.info(f"Data item is exhausted")


    def run(self):
      	"""Overide Method From Thread"""
        self.predict()
```

## 5. [RegexNLP](./RegexNLP)

Compress word information about Weibo. Use regular expression to sub unified token, like:

```python
BOS = "<BOS/>"
EOS = "</EOS>"
UNK = "<UNK>"
DATE = "#DATE"
TIME = "#TIME"
NUMBER = "#NUM"
LINK = "#URL"
IMAG = "#IMG"
USER = "#USER"
FEE = "#FEE"
PHONE = "#PHONE"
```

Caution ⚠️: the regex is not perfect, there are so many things could being done!



## 6. [InterchangeUnicodeString](./CharEncode&Decode)

There are two functions to deal with string:

```python
# string to unicode
>>> string = "这个是一个测试字符串"
>>> text2unicode(string) # 默认情况是直接得到 16 进制字符串
    '\u8FD9\u4E2A\u662F\u4E00\u4E2A\u6D4B\u8BD5\u5B57\u7B26\u4E32'
>>> print("\u8FD9\u4E2A\u662F\u4E00\u4E2A\u6D4B\u8BD5\u5B57\u7B26\u4E32")
    这个是一个测试字符串
>>> print(text2unicode(string), True) # 转换为字节型字符
    b'\\u8fd9\\u4e2a\\u662f\\u4e00\\u4e2a\\u6d4b\\u8bd5\\u5b57\\u7b26\\u4e32'
   
# unicode to string
>>> string = b'\\u8fd9\\u4e2a\\u662f\\u4e00\\u4e2a\\u6d4b\\u8bd5\\u5b57\\u7b26\\u4e32'
>>> unicode2text(string) # 字节型数据转换
    '这个是一个测试字符串'
>>> string = '\\u8fd9\\u4e2a\\u662f\\u4e00\\u4e2a\\u6d4b\\u8bd5\\u5b57\\u7b26\\u4e32'
>>> unicode2text(string) # 字符串型数据转换
    '这个是一个测试字符串'
```

## 7. [Naive RNN](./DeepLearning/naiveRNN.py)

使用 Numpy 实现简单的 RNN cell，包含了三个属性: `weight_io` 是输入到输出权重 $W$，`weight_ho` 是上一个输出  $U$。当个 RNN cell 结构是 
$$
\text{result}_i=\text{tanh}(\text{dot}(W, \text{input}_i) + \text{dot}(U, \text{hidden}_{i-1}) + \text{bias})
$$
得到的最终结果是把输出整合为一个序列，但实际情况下输出结果长度可以为 1，即只保留序列最后一个输入的结果。

## 8. [ConfigParse](./ConfigParse)

Python 的配置解析，可以分为两种情况：1. 解决 CMD 的方式交互的配置解析，这种主要是在命令行的情况下使用；2. 解决从文件中解析的情况，这种情况主要的目的是从一个配置文件中去解析。

第一种情况下可以使用标准库中的 argparse 解决，第二种的话可以根据情况判断是否需要使用第三方库，第三方库包括 pyhocon（是由谷歌开发完成，集成了多个类型的配置方式，yaml、init、json 等多种类型）。如果不使用第三方库，可以使用标准库中的 configparser 解决。

### configparser 解析

configparser 解析的文件是与 Microsoft Windows INI 文件的类似:
```ini
[DEFAULT]
ServerAliveInterval = 45
Compression = yes
CompressionLevel = 9
ForwardX11 = yes

[bitbucket.org]
User = hg

[topsecret.server.com]
Port = 50022
ForwardX11 = no
```

`configparser` 可以直接解析文件，通过一个 `parser` 对象可以直接使用 `read` 等几种方法读取文件或者数据可以达到解析数据的情况。在文件 `parse.py` 是通过 `read` 方法读取文件，脚本的数据方式是:

```python
>>> from parse import Config
>>> config = Config("./database.ini")

# 获取 mysql 的配置信息
>>> config.mysql
{'host': '192.168.1.31',
 'port': '3306',
 'user': 'root',
 'charset': 'utf8mb4',
 'connect_timeout': '35',
 'database': 'test'}
```

## 9. [MachineLearning](./MachineLearning)

机器学习部分的有趣代码整理和总结

### 9.1 OLS

简单线性回归参数变化，方差和残差变化可视化。详情参考 [README](./MachineLearning/README.md)

## 10. [AutoEncoder 图像应用](./AutoEncoder)

通过 Keras 搭建 encoder 和 decoder 模型的方式，将 encoder 的结果作为特征表现的方式

