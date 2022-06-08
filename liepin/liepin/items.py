# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    # 职位名称
    job_title = scrapy.Field()
    # 职位地区
    job_dq = scrapy.Field()
    # 职位标签（急聘）
    job_tag = scrapy.Field()
    # 职位薪资
    job_salary = scrapy.Field()
    # 职位技术标签:不定长的数组类型
    job_labels = scrapy.Field()
    # 职位所在公司
    company = scrapy.Field()
    # 公司相关领域
    company_field = scrapy.Field()
    # 公司规模
    company_size = scrapy.Field()
    # hr
    hr = scrapy.Field()
    # hr的职位
    hr_pos = scrapy.Field()

