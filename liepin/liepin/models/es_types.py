# -*- codeing: utf-8 -*-
from elasticsearch_dsl import Document, Keyword, Text, Double
from elasticsearch_dsl.connections import connections

es = connections.create_connection(host="127.0.0.1")


# class suningType(Document):
class liepinType(Document):
    # 设置index名称和document名称
    class Index:
        name = "liepin"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }
        mappings = {
            "properties": {
                "job_title": {
                    "type": "text"
                },
                "jod_dq": {
                    "type": "keyword"
                },
                "job_tag": {
                    "type": "keyword"
                },
                "job_salary": {
                    "type": "text"
                },
                "job_labels": {
                    "type": "text"
                },
                "company": {
                    "type": "text"
                },
                "company_field": {
                    "type": "text"
                },
                "company_size": {
                    "type": "text"
                },
                "hr": {
                    "type": "text"
                },
                "hr_pos": {
                    "type": "text"
                }
            }
        }

    job_title = Text(analyzer="ik_max_word")
    job_dq = Keyword()
    job_tag = Keyword()
    job_salary = Text(analyzer="ik_smart")
    job_labels = Text(analyzer="ik_smart")
    company = Text(analyzer="ik_max_word")
    company_field = Text(analyzer="ik_smart")
    company_size = Text(analyzer="ik_smart")
    hr = Text(analyzer="ik_smart")
    hr_pos = Text(analyzer="ik_smart")


    def __init__(self, item):
        super(liepinType, self).__init__()
        self.assignment(item)

    # 将item转换为es的数据
    def assignment(self, item):
        keys = ['job_title',
                'job_dq',
                'job_tag',
                'job_salary',
                'job_labels',
                'company',
                'company_field',
                'company_size',
                'hr',
                'hr_pos']
        for key in keys:
            try:
                item[key]
            except:
                item[key] = ''
        # 将字段值转换为es的数据
        # 虽然只是将原来的item值赋给了成员变量，但这个过程中会执行数据格式转换操作，
        # 比如url本来在item是python的字符串类型，转换后变为es的keyword类型
        self.job_title = item['job_title']
        self.job_dq = item['job_dq']
        self.job_tag = item['job_tag']
        self.job_salary = item['job_salary']
        self.job_labels = item['job_labels']
        self.company = item['company']
        self.company_field = item['company_field']
        self.company_size = item['company_size']
        self.hr = item['hr']
        self.hr_pos = item['hr_pos']
