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

    # 5. 主要采用技术
    # main_tech = scrapy.Field()
    # 6. 岗位查找所用的关键词
    pos_keyword = scrapy.Field()
    # 7. 岗位所属领域（来自我们内部的映射）
    pos_domain = scrapy.Field()

    # 8. 职位所在城市
    city = scrapy.Field()
    # 9. 岗位所在地：职位所在地区或者具体地址
    location = scrapy.Field()

    # 10. 学历要求
    degree = scrapy.Field()
    # 11. 经验要求
    exp = scrapy.Field()

    """ 二、负责人相关信息 """
    # 12.  负责人名称
    person_in_charge = scrapy.Field()
    # 13. 岗位负责人的职位
    charge_pos = scrapy.Field()

    # # 14. 岗位详情：职位责任
    # pos_responsibility = scrapy.Field()
    # # 15. 岗位详情：职位要求
    # pos_requirement = scrapy.Field()
    # 16. 岗位详情：爬不到岗位的详情页面，所以只能放在detail字段里，为空
    pos_detail = scrapy.Field()

    """ 三、职位所在公司的相关信息 """
    # 17. 公司名称
    enterprise = scrapy.Field()
    # company = scrapy.Field()
    # 公司相关领域
    # company_field = scrapy.Field()
    # 18. 公司规模
    enterprise_scale = scrapy.Field()
    # company_size = scrapy.Field()

    # 19. 创建时间
    create_time = scrapy.Field()

    # 20.含有岗位详情和招聘人的信息的url
    url = scrapy.Field()

    pos_source = scrapy.Field()
