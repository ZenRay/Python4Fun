# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd
import os

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        repo_name = item["repo_name"]
        update_time = item["update_time"]
        
        tem = pd.DataFrame(
            [[repo_name, update_time]], columns=["repo_name", "update_time"]
        )

        self.df = pd.concat([self.df, tem], ignore_index=True)
        self.df = self.df.sort_values(by="update_time", ascending=False)
        return item

    def open_spider(self, spider):
        self.df = pd.DataFrame(columns=["repo_name", "update_time"])
        
    def close_spider(self, spider):
        file = input("Enter your report file name: ")
        if os.path.exists("~/Code"):
            pd.DataFrame.to_csv(self.df, "~/Code/{}.csv".format(file))
        else:
            pd.DataFrame.to_csv(self.df, "./{}.csv".format(file))