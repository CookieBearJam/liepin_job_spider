# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LiepinItem(scrapy.Item):
    """ 一、职位相关信息 """
    # 1.职位名称
    pos_name = scrapy.Field()

    # 2. 职位薪资下限
    salary_low_bound = scrapy.Field()
    # 3. 职位薪资上限
    salary_high_bound = scrapy.Field()
    # 4. 薪资计数月份
    salary_fee_months = scrapy.Field()

    # 5. 岗位查找所用的关键词（主要技术或者相关领域）
    pos_keyword = scrapy.Field()
    # 6. 岗位所属领域（来自我们内部的映射）
    pos_domain = scrapy.Field()

    # 7. 职位所在城市
    city = scrapy.Field()
    # 8. 岗位所在地：职位所在地区或者具体地址
    location = scrapy.Field()

    # 9. 学历要求
    degree = scrapy.Field()
    # 10. 经验要求
    exp = scrapy.Field()

    """ 二、负责人相关信息 """
    # 11.  负责人名称
    person_in_charge = scrapy.Field()
    # 12. 岗位负责人的职位
    charge_pos = scrapy.Field()

    # 13. 岗位详情：爬不到岗位的详情页面放url到url字段中
    pos_detail = scrapy.Field()

    """ 三、职位所在公司的相关信息 """
    # 14. 公司名称
    enterprise = scrapy.Field()
    # 15. 公司规模
    enterprise_scale = scrapy.Field()
    scale_mapping = scrapy.Field()

    # 16. 爬取时间
    create_time = scrapy.Field()

    # 17.含有岗位详情和招聘人的信息的url
    url = scrapy.Field()

    # 18.岗位的来源网站
    pos_source = scrapy.Field()
