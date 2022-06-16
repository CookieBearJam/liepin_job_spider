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

    # pos_class_dict = {
    #     "后端开发":
    #         ["Java", "Php", "Python", "Ruby", "Node.JS", ".NET", "ASP", "C#", "C++", "C", "Delphi",
    #          "Go", "Docker", "Hadoop", "Spark", "HBase", "Openstack", "全栈工程师"],
    #     "前端开发": ["U3D", "COCOS2D-X", "html5", "Web前端", "Flash", "Javascript"],
    #     "移动端开发": ["iOS", "Android"],
    #     "人工智能": ["数据挖掘", "自然语言处理", "推荐系统", "搜索引擎"],
    #     "测试运维": ["测试工程师", "自动化测试", "功能测试", "性能测试", "测试开发", "硬件测试", "运维工程师", "系统工程师",
    #              "网络工程师", "运维开发"],
    #     "数据库": ["DBA"]
    # }
    #
    # pos_dqs_dict = {'全国': '410', '北京': '010', '上海': '020', '天津': '030', '重庆': '040', '广州': '050020', '深圳': '050090',
    #                 '苏州': '060080', '南京': '060020', '杭州': '070020', '大连': '210040', '成都': '280020', '武汉': '170020',
    #                 '西安': '270020'}

    pos_class_arr = [
        {"后端开发": ["Java", "Php", "Python", "Ruby", "Node.JS", ".NET", "ASP", "C#", "C++", "C", "Delphi",
                  "Go", "Docker", "Hadoop", "Spark", "HBase", "Openstack", "全栈工程师"]
         },
        {"前端开发": ["U3D", "COCOS2D-X", "html5", "Web前端", "Flash", "Javascript"]},
        {"移动端开发": ["iOS", "Android"]},
        {"人工智能": ["数据挖掘", "自然语言处理", "推荐系统", "搜索引擎"]},
        {"测试运维": ["测试工程师", "自动化测试", "功能测试", "性能测试", "测试开发", "硬件测试", "运维工程师", "系统工程师",
                  "网络工程师", "运维开发"]},
        {"数据库": ["DBA"]}
    ]

    # pos_dqs_arr = ["全国", "北京", "上海", "天津", "重庆", "广州", "深圳", "苏州", "南京", "杭州", "大连", "成都", "武汉", "西安"]
    pos_dqs_arr = [{'全国': '410'}, {'北京': '010'}, {'上海': '020'}, {'天津': '030'}, {'重庆': '040'}, {'广州': '050020'},
                   {'深圳': '050090'}, {'苏州': '060080'}, {'南京': '060020'}, {'杭州': '070020'}, {'大连': '210040'},
                   {'成都': '280020'}, {'武汉': '170020'}, {'西安': '270020'}]

    # 总共需要爬取的domain数量
    total_class_num = len(pos_class_arr)
    # 总共需要爬取的热门城市数量
    total_city_num = len(pos_dqs_arr)

    # 总共需要爬取的起始页面的数量（没有与城市组合之前）
    total_cate_num = 0
    for each in pos_class_arr:
        for key in each.keys():
            cate_list = each[key]
            total_cate_num += len(cate_list)

    total_items = 500 * total_cate_num * total_city_num

    print("total_class_num:", total_class_num)
    print("total_city_num:", total_city_num)
    print("total_cate_num:", total_cate_num)
    print("total_items_count:", total_items)

    # 当前正在访问的大分类的下标
    cur_domain_index = 0
    # # 访问过的大分类的数量
    # visited_domain_num = 0
    # 当前的分类是：pos_class_arr第n个元素的字典中，第一个key
    cur_domain = list(pos_class_arr[cur_domain_index].keys())[0]
    # print("cur_domain:", cur_domain)

    # 当前大分类中，访问到第几个小分类
    cur_cate_index = 0
    # # 在当前的大分类中，访问过的小分类的数量
    # visited_cate_num = 0
    # 当前查询条件中的分类具体的值：pos_class_arr第n个元素的字典中，第一个key对应的value的list中第n个值，
    cur_cate_list = pos_class_arr[cur_domain_index].get(cur_domain)
    # print("cur_cate_list:", cur_cate_list)
    cur_cate = cur_cate_list[cur_cate_index]
    # print("cur_cate:", cur_cate)

    # 当前大分类+小分类组合下，访问到第几个城市了
    cur_dq_index = 0
    # # 当前大分类+小分类组合下，访问过的地区的数量
    # visited_dq_num = 0
    # 当前正在查询的城市名：城市列表中的第n个元素的value
    cur_dq = list(pos_dqs_arr[cur_dq_index].values())[0]

    '''工具'''
    # 创建一个布隆过滤器，用于所有的url去重
    bf = BloomFilter(capacity=total_items)

    # 创建工具类
    lp_utils = LPUtils()

    def parse(self, response):

        # if self.cur_class_visited_num == len(self.pos_class_arr[""]):
        # # 首先根据当前正在爬取的分类，

        # cur_dq = "410"
        # cur_category = "Java"

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
                # Todo：经过映射后的岗位分类

                pos_keyword_num = len(pos_keywords_list)
                if pos_keyword_num >= 2:
                    item['exp'] = str(pos_keywords_list[0].extract())
                    item['degree'] = str(pos_keywords_list[1].extract())
                    for i in range(2, pos_keyword_num):
                        item['pos_keyword'].append(str(pos_keywords_list[i].extract()))
                else:
                    print("职位标签中不包含学历要求和经验要求：pos_name:", item['pos_name'])

                # 5.岗位招聘人信息：名称和职称
                charge_person = each.xpath(
                    './/div[@class="recruiter-name ellipsis-1"]//text()').extract_first()
                charge_pos = each.xpath('.//div[@class="recruiter-title ellipsis-1"]//text()').extract_first()
                if charge_person:
                    item['person_in_charge'] = charge_person
                if charge_pos:
                    item['charge_pos'] = charge_pos

                # 6. 岗位所在公司的情况
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

                print("job_detail_link:", job_detail_link)
                print("crawling details page,link:", item['url'])
                details_request = scrapy.Request(url=item['url'], callback=self.details,
                                                 meta={'base_item': copy.deepcopy(item)})
                print("Calling detail scrape!")
                yield details_request

        # 1.判断当前是否为当前大分类+小分类+地区的最后一页
        # 不是的话：
        #   2.获取当前页面的数字
        #   3.构造下一页的链接
        # https://www.liepin.com/zhaopin/?sfrom=search_job_pc&key=python&currentPage=5&scene=page
        last_page_class = selector.xpath('//li[@title="下一页"]/@class').extract_first()
        print("last_page_class:", last_page_class)
        if last_page_class == "ant-pagination-next":
            current_page_num = selector.xpath(
                '//div[@class="list-pagination-box"]/ul/li[@class="ant-pagination-item '
                'ant-pagination-item-active"]/a/text()').extract_first()
            print("当前页面序号：", current_page_num)  # pagenum = 5的话当前访问的url参数其实是第4页
            nextLink = self.liepin_base_url + "&key=" + self.cur_cate + "&dqs=" + self.cur_dq + "&currentPage=" + current_page_num + "&scene=page"
            # 构造下一页的链接
            print("下一个要访问的页面url为：", nextLink)
            yield Request(nextLink, callback=self.parse, dont_filter=True)  # 循环访问链接。
        elif last_page_class == "ant-pagination-next ant-pagination-disabled":
            print("某个条件的搜索结果爬取已经到达最后一页，需要切换url了")
            """切换爬取的url"""

            # 如果上一个分类的页面爬完了：应该是还需要爬其他的地区：大分类还没有爬完(0~self.total_class_num-1)
            if self.cur_domain_index < self.total_class_num:
                cur_cate_list = self.pos_class_arr[self.cur_domain_index].get(self.cur_domain)
                # 如果当前大分类下的小分类还没爬完
                if self.cur_cate_index < len(cur_cate_list):
                    # 如果当前小分类底下的地区列表还没爬完
                    if self.cur_dq_index < self.total_city_num:
                        self.cur_dq_index += 1
                        self.cur_dq = list(self.pos_dqs_arr[self.cur_dq_index].values())[0]
                    else:
                        # 需要重新爬取小的分类
                        self.cur_dq_index = 0
                        # 重置self.cur_dq
                        self.cur_dq = list(self.pos_dqs_arr[self.cur_dq_index].values())[0]
                        print("大分类：", self.cur_domain, "的小分类：", self.cur_cate, "底下的所有地区已经遍历完")

                        self.cur_cate_index += 1
                        self.cur_cate = self.pos_class_arr[self.cur_domain_index].get(self.cur_domain)[
                            self.cur_cate_index]
                        print("切换小分类为：", self.cur_cate, ",此时的地区为：", self.cur_dq)
                else:
                    print("大分类:", self.cur_domain, "底下的所有小分类已经遍历完")
                    self.cur_domain_index += 1
                    self.cur_domain = list(self.pos_class_arr[self.cur_domain_index].keys())[0]
                    print("切换大分类为：", self.cur_domain)

                    self.cur_cate_index = 0
                    self.cur_cate = self.pos_class_arr[self.cur_domain_index].get(self.cur_domain)[0]

                    self.cur_dq_index = 0
                    self.cur_dq = list(self.pos_dqs_arr[self.cur_dq_index].values())[0]

                    print("此时的小分类为：", self.cur_cate, ",地区为：", self.cur_dq)

                # 构造新的url：
                # start_urls = ['https://www.liepin.com/zhaopin/?imscid=R000000035&key=Java&dqs=410']
                new_cond_url = self.liepin_base_url + "&key=" + self.cur_cate + "&dqs=" + self.cur_dq
                new_cond_request = scrapy.Request(url=new_cond_url, callback=self.parse)
                print("Calling new condition scrape!")
                yield new_cond_request
            else:
                print("所有的分类都爬完了！", "大分类：", self.cur_domain, "小分类：", self.cur_cate, "地区:", self.cur_dq)
        else:
            print("无法识别的标签类别属性")

    def copy_item(self, item_to, item_from):
        keys = ['pos_name', 'salary_low_bound', 'salary_high_bound', 'salary_fee_months',
                'pos_keyword', 'pos_domain', 'city', 'location', 'degree',
                'exp', 'person_in_charge', 'charge_pos', 'pos_detail', 'enterprise',
                'enterprise_scale', 'create_time', 'url', 'pos_source'
                ]
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
            if pos_res:
                detail_item['pos_detail'] = pos_res
            yield detail_item
        else:
            print("Bad calling of job_detail_handler!!!Base item is null!")
            return
