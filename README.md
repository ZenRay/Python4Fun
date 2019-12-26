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

Use configuration file to setup logger. There are some default FORMATTERS and HANDLERS configuration file that parse the `conf` file with [HOCON](https://github.com/lightbend/config/blob/master/HOCON.md) .

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

