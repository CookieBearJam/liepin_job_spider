import scrapy
from liepin.items import LiepinItem
from scrapy import Selector
from scrapy.http import Request


class LiepinSpiderSpider(scrapy.Spider):
    name = 'liepin_spider'
    allowed_domains = ['liepin.com/zhaopin']
    start_urls = ['https://www.liepin.com/zhaopin/?sfrom=search_job_pc&key=java&currentPage=0&scene=page']
    liepin_base_url = 'https://www.liepin.com/zhaopin/'

    def parse(self, response):
        print("start to crawl")
        # items = response.xpath('//ol[@class="grid_view"]//li')
        items = response.xpath('//div[@class="left-list-box"]/ul/li')  # 这里得到一个list
        item = LiepinItem()
        selector = Selector(response)
        for each in items:
            job_header = each.xpath('.//div[@class="job-detail-header-box"]')
            job_title_box = job_header.xpath('.//div[@class="job-title-box"]')

            item['job_title'] = job_title_box.xpath('./div[1]//text()').extract()
            # print("job_title", item['job_title'])
            item['job_dq'] = job_title_box.xpath('./div[2]//span[@class="ellipsis-1"]//text()').extract()
            # print("job_dq", item['job_dq'])
            item['job_tag'] = job_header.xpath('./span[@class="job-tag"]//text()').extract()
            # print("job_tag", item['job_tag'])
            item['job_salary'] = job_header.xpath('./span[@class="job-salary"]//text()').extract_first()

            # 数组类型的职位技术标签
            job_labels_lists = each.xpath('.//div[@class="job-labels-box"]//span[@class="labels-tag"]//text()')
            item['job_labels'] = []
            # print(each.xpath('.//div[@class="job-labels-box"]/span/text()'))
            for label in job_labels_lists:
                item['job_labels'].append(str(label.extract()))

            print("job_labels",item['job_labels'])

            # # 职位所在公司
            company_info = each.xpath('.//div[@class="job-company-info-box"]')
            item['company'] = company_info.xpath('.//span[@class="company-name ellipsis-1"]/text()').extract_first()

            company_labels = company_info.xpath('.//div[@class="company-tags-box ellipsis-1"]')
            # 公司相关领域
            item['company_field'] = company_labels.xpath('./span[1]/text()').extract_first()
            # 公司规模
            item['company_size'] = company_labels.xpath('./span[2]/text()').extract_first()

            # hr
            hr_info = each.xpath('.//div[@class="recruiter-info-text-box"]')
            item['hr'] = hr_info.xpath('.//div[@class="recruiter-name ellipsis-1"]/text()').extract_first()
            # hr的职位
            item['hr_pos'] = hr_info.xpath('.//div[@class="recruiter-title ellipsis-1"]/text()').extract_first()

            yield item

        # 判断当前是否为最后一页
        # 获取当前页面的数字
        # 构造下一页的链接
        last_page_class = selector.xpath('//li[@title="下一页"]/@class').extract_first()
        print("last_page_class", last_page_class)
        if last_page_class == "ant-pagination-next":
            current_page_num = selector.xpath(
                '//div[@class="list-pagination-box"]/ul/li[@class="ant-pagination-item ant-pagination-item-active"]/a/text()').extract_first()
            print("当前页面数字：", current_page_num)  # pagenum = 5的话当前访问的url参数其实是第4页
            nextLink = self.liepin_base_url + "?sfrom=search_job_pc&key=java&currentPage=" + current_page_num + "&scene=page"  # 构造下一页的链接
            print("下一个要访问的页面url为：", nextLink)
            yield Request(nextLink, callback=self.parse, dont_filter=True)  # 循环访问链接。
        elif last_page_class == "ant-pagination-next ant-pagination-disabled":
            print("搜索结果爬取已经到达最后一页")
        else:
            print("无法识别的标签类别属性")
    # https: // www.liepin.com / zhaopin /?sfrom = search_job_pc & key = python & currentPage = 5 & scene = page