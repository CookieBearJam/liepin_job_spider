import scrapy
import copy

from liepin.items import LiepinItem
from scrapy import Selector
from scrapy.http import Request
from pybloom_live import BloomFilter
from liepin.utils import LPUtils


class LiepinSpiderSpider(scrapy.Spider):
    name = 'liepin_spider'
    allowed_domains = ['liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?imscid=R000000035&key=Java&dqs=410']
    liepin_base_url = "https://www.liepin.com/zhaopin/?imscid=R000000035"

    # 最新使用的url如下（第6页）：https://www.liepin.com/zhaopin/?imscid=R000000035&key=Java&dqs=410&currentPage=5&scene=page
    # 之前使用的url是这个：https://www.liepin.com/zhaopin/?sfrom=search_job_pc&key=python&currentPage=5&scene=page

    # start_urls = ['https://www.liepin.com/zhaopin/?sfrom=search_job_pc&key=java&currentPage=0&scene=page']
    # 武汉java开发岗位的首页：
    # https://www.liepin.com/zhaopin/?imscid=R000000035&key=Java&dqs=170020
    # 全国的java开发岗位首页：
    # https://www.liepin.com/zhaopin/?imscid=R000000035&key=Java&dqs=410

    # pos_dict = [{"开发": ["Java", "Php", "Python", "Ruby", "Node.JS", ".NET", "ASP", "C#", "C++", "C", "Delphi",
    # "Go", "Docker", "Hadoop", "Spark", "HBase", "Openstack", "数据挖掘", "自然语言处理", "推荐系统", "搜索引擎", "全栈工程师"]},
    # {"移动端开发及前端": ["iOS", "Android", "U3D", "COCOS2D-X", "HTML5", "Web前端", "Flash", "Javascript"]}, {"测试": ["测试工程师",
    # "自动化测试", "功能测试", "性能测试", "测试开发", "硬件测试"]}, {"运维": ["运维工程师", "系统工程师", "网络工程师", "运维开发", "DBA"]},
    # {"高端职位": ["技术经理", "架构师", "技术总监", "CTO", "技术合伙人", "运维总监", "安全专家", "项目总监"]} ]

    pos_class_arr = [
        {"后端开发": ["Java", "Php", "Python", "Ruby", "Node.JS", ".NET", "ASP", "C#", "C++", "C", "Delphi", "Go",
                  "Docker", "Hadoop", "Spark", "HBase", "Openstack", "全栈工程师"],
         "前端开发": ["U3D", "COCOS2D-X", "html5", "Web前端", "Flash", "Javascript"],
         "移动端开发": ["iOS", "Android"],
         "人工智能": ["数据挖掘", "自然语言处理", "推荐系统", "搜索引擎"],
         "测试运维": ["测试工程师", "自动化测试", "功能测试", "性能测试", "测试开发", "硬件测试", "运维工程师", "系统工程师",
                  "网络工程师", "运维开发"],
         "数据库": ["DBA"],
         # "硬件开发": [""]这里没有硬件开发
         # "其他":[]
         }
    ]
    pos_dqs_arr = ["全国", "北京", "上海", "天津", "重庆", "广州", "深圳", "苏州", "南京", "杭州", "大连", "成都", "武汉", "西安", "其他"]

    # total_class = 400 * len(pos_class_arr) * len(pos_class_arr[0]["后端开发"])
    total_class = 500
    # 创建一个布隆过滤器
    bf = BloomFilter(capacity=total_class)

    lp_utils = LPUtils()

    # class_num = len(pos_class_arr)
    # visited_num = 0

    def parse(self, response):

        # if self.visited_num <= 0:
        #     return
        cur_dq = "410"
        cur_category = "Java"

        print("Starting to crawl...")
        items = response.xpath('//div[@class="left-list-box"]/ul/li')  # 得到所有元素的list
        selector = Selector(response)

        for each in items:
            # 1. 获取该item的岗位详情页面url
            job_detail_link = each.xpath(
                './/div[@class="job-detail-box"]/a[@data-nick="job-detail-job-info"]/@href').extract_first()
            # print("job detail:", job_detail_link)
            # 详情页不是重复的url
            if job_detail_link and (job_detail_link not in self.bf):
                # 创建一个需要提交的item
                item = LiepinItem()

                self.bf.add(job_detail_link)
                # 详情页面的url
                item['url'] = job_detail_link
                item['pos_source'] = "猎聘"
                item['pos_domain'] = "后端开发"

                # 2. 职位名称、所在城市、地区
                pos_header = each.xpath('.//div[@class="job-detail-header-box"]')
                pos_name_box = pos_header.xpath('.//div[@class="job-title-box"]')
                item['pos_name'] = pos_name_box.xpath('./div[1]//text()').extract()

                # 类似“上海-闵行区”这样的格式
                job_dq = pos_name_box.xpath('./div[2]//span[@class="ellipsis-1"]//text()').extract_first()
                # 城市：如果有分隔符，那就分割，否则只保存城市信息，没有具体位置信息
                dq_list = self.lp_utils.get_city_locale(str(job_dq))
                # item['city'] = ""
                # item['location'] = ""
                if dq_list and (len(dq_list) > 1):
                    item['city'] = dq_list[0]
                    item['location'] = dq_list[1]
                elif len(dq_list) == 1:
                    item['city'] = dq_list[0]
                else:
                    print("此岗位职位名称中，没有包含（中文）地区信息")

                # 3. 岗位薪资上限、下限、计费月份(默认是12)
                salary = pos_header.xpath('./span[@class="job-salary"]//text()').extract_first()
                salary_list = self.lp_utils.get_salary_by_reg(str(salary))
                print(len(salary_list))
                item['salary_low_bound'] = "0"
                item['salary_high_bound'] = "0"
                item['salary_fee_months'] = "0"

                if len(salary_list) == 3:
                    item['salary_low_bound'] = float(salary_list[0])
                    item['salary_high_bound'] = float(salary_list[1])
                    item['salary_fee_months'] = int(salary_list[2])
                elif len(salary_list) == 2:
                    item['salary_low_bound'] = float(salary_list[0])
                    item['salary_high_bound'] = float(salary_list[1])
                    item['salary_fee_months'] = 12

                # 4. 经验、学历、关键词
                # 数组类型的职位技术标签
                pos_keywords_list = each.xpath('.//div[@class="job-labels-box"]//span[@class="labels-tag"]//text()')

                # 岗位查找关键词
                item['pos_keyword'] = []
                # item['main_tech'] = []
                # Todo：经过映射后的岗位分类
                # item['pos_domain'] = ""

                pos_keyword_num = len(pos_keywords_list)
                if pos_keyword_num >= 2:
                    item['exp'] = str(pos_keywords_list[0].extract())
                    item['degree'] = str(pos_keywords_list[1].extract())
                    for i in range(2, pos_keyword_num):
                        item['pos_keyword'].append(str(pos_keywords_list[i].extract()))
                        # item['main_tech'].append(str(pos_keywords_list[i].extract()))
                else:
                    print("职位标签中不包含学历要求和经验要求：pos_name:", item['pos_name'])

                # 5.岗位招聘人信息：名称和职称
                # item['person_in_charge'] = ""
                # item['charge_pos'] = ""
                charge_person = each.xpath(
                    './/div[@class="recruiter-name ellipsis-1"]//text()').extract_first()
                charge_pos = each.xpath('.//div[@class="recruiter-title ellipsis-1"]//text()').extract_first()
                if charge_person:
                    item['person_in_charge'] = charge_person
                if charge_pos:
                    item['charge_pos'] = charge_pos

                # 6. 岗位所在公司的情况
                # item['enterprise'] = ""
                # item['enterprise_scale'] = ""
                enterprise = each.xpath('.//span[@class="company-name ellipsis-1"]//text()').extract_first()
                enterprise_scale = each.xpath(
                    './/div[@class="company-tags-box ellipsis-1"]/span[2]//text()').extract_first()
                if enterprise:
                    item['enterprise'] = enterprise
                if enterprise_scale:
                    item['enterprise_scale'] = enterprise_scale

                # 7.创建时间为我们爬取岗位的时间
                item['create_time'] = LPUtils.get_time_now_str()

                # 初始化这个item的详情页面
                """8.爬取详情页面的职位详情、职位要求"""
                # 8.1 初始化
                # item['pos_responsibility'] = ""
                # item['pos_requirement'] = ""
                # item['pos_detail'] = ""

                print("job_detail_link:", job_detail_link)
                print("crawling details page,link:", item['url'])
                details_request = scrapy.Request(url=item['url'], callback=self.details,
                                                 meta={'base_item': copy.deepcopy(item)})
                print("hey calling!")
                yield details_request

        # 判断当前是否为最后一页
        # 获取当前页面的数字
        # 构造下一页的链接
        # https://www.liepin.com/zhaopin/?sfrom=search_job_pc&key=python&currentPage=5&scene=page
        last_page_class = selector.xpath('//li[@title="下一页"]/@class').extract_first()
        print("last_page_class:", last_page_class)
        if last_page_class == "ant-pagination-next":
            current_page_num = selector.xpath(
                '//div[@class="list-pagination-box"]/ul/li[@class="ant-pagination-item '
                'ant-pagination-item-active"]/a/text()').extract_first()
            print("当前页面序号：", current_page_num)  # pagenum = 5的话当前访问的url参数其实是第4页
            nextLink = self.liepin_base_url + "&key=" + cur_category + "&dqs=" + cur_dq + "&currentPage=" + current_page_num + "&scene=page"
            # 构造下一页的链接
            print("下一个要访问的页面url为：", nextLink)
            yield Request(nextLink, callback=self.parse, dont_filter=True)  # 循环访问链接。
        elif last_page_class == "ant-pagination-next ant-pagination-disabled":
            print("搜索结果爬取已经到达最后一页")
        else:
            print("无法识别的标签类别属性")

    def copy_item(self, item_to, item_from):
        keys = ['pos_name', 'salary_low_bound', 'salary_high_bound', 'salary_fee_months',
                'pos_keyword', 'pos_domain', 'city', 'location', 'degree',
                'exp', 'person_in_charge', 'charge_pos', 'pos_detail', 'enterprise',
                'enterprise_scale', 'create_time', 'url', 'pos_source'
                ]
        # for key in keys:
        for key in item_from.keys():
            item_to[key] = item_from[key]
            # if (key == 'main_tech') or (key == 'pos_domain') or (key == 'pos_keyword'):
            #     item_to[key] = []
            # for e in item_from[key]:
            #     item_to[key].append(e)
            # else:
            # if item_from[key]:
            #     item_to[key] = item_from[key]
            # else:
            #     # 没有爬到的数据字段设置为空即可
            #     item_to[key] = None

    def details(self, response):
        print("Callback of details link")
        base_item = response.meta['base_item']
        if base_item:
            detail_item = LiepinItem()
            self.copy_item(detail_item, base_item)

            # 1. 获取岗位内容（职责）
            pos_res = response.xpath('//section[@class="job-intro-container"]//dd['
                                     '@data-selector="job-intro-content"]/text()').extract_first()
            # print("pos_res:", pos_res)
            # 2. 获取岗位要求 pos_req = response.xpath('//section[@class="job-intro-container"]//dd[
            # @data-selector="job-intro-content"]/text()').extract_first() if pos_res and pos_req:
            if pos_res:
                # detail_item['pos_responsibility'] = pos_res
                # detail_item['pos_requirement'] = pos_res
                detail_item['pos_detail'] = pos_res
            yield detail_item
        else:
            print("Bad calling of job_detail_handler!!!Base item is null!")
            return
