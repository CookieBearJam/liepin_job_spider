# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class LiepinPipeline:
    def process_item(self, item, spider):
        return item


# 将爬到的数据存储到csv文件里
class savefileTongscrapyPipeline(object):
    def __init__(self):
        # self.item_list = []
        pass

    def process_item(self, item, spider):
        # self.item_list.append(item)
        print("job_title:", item['job_title'])
        return item

    def close_spider(self, spider):
        print("sort")


from .models.es_types import liepinType


class ElasticsearchPipeline:

    def process_item(self, item, spider):
        sn = liepinType(item)
        sn.save()
        return item
