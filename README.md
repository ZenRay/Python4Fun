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