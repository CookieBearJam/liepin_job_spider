# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .models.es_types import liePinJavaType


class LiepinPipeline:
    def process_item(self, item, spider):
        return item


# 将爬到的数据存储到csv文件里
class savefileTongscrapyPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        print("pos_name:", item['pos_name'])
        return item

    def close_spider(self, spider):
        print("spider closed")


class ElasticsearchPipeline:
    def process_item(self, item, spider):
        sn = liePinJavaType(item)
        sn.save()
        return item
