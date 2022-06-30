# import
class little_spiders:
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

    # 1. 总共需要爬取的domain数量
    total_class_num = len(pos_class_arr)
    # 2. 总共需要爬取的热门城市数量
    total_city_num = len(pos_dqs_arr)

    # 3. 总共需要爬取的起始页面的数量（没有与城市组合之前）
    total_cate_num = 0
    for each in pos_class_arr:
        for key in each.keys():
            cate_list = each[key]
            total_cate_num += len(cate_list)

    # 4. 总共可能出现的条目数量
    total_items = 500 * total_cate_num * total_city_num

    print("total_class_num:", total_class_num)
    print("total_city_num:", total_city_num)
    print("total_cate_num:", total_cate_num)
    print("total_items_count:", total_items)

    # 1.1当前正在访问的大分类的下标
    cur_domain_index = 0
    # 1.2访问过的大分类的数量
    visited_domain_num = 0
    # 1.3当前的分类是：pos_class_arr第n个元素的字典中，第一个key
    cur_domain = list(pos_class_arr[cur_domain_index].keys())[0]
    # print("cur_domain:", cur_domain)

    # 当前大分类中，访问到第几个小分类
    cur_cate_index = 0
    # 在当前的大分类中，访问过的小分类的数量
    visited_cate_num = 0
    # 当前查询条件中的分类具体的值：pos_class_arr第n个元素的字典中，第一个key对应的value的list中第n个值，
    cur_cate_list = pos_class_arr[cur_domain_index].get(cur_domain)
    # print("cur_cate_list:", cur_cate_list)
    cur_cate = cur_cate_list[cur_cate_index]
    print("cur_cate:", cur_cate)

    # 当前大分类+小分类组合下，访问到第几个城市了
    cur_dq_index = 0
    # 当前大分类+小分类组合下，访问过的地区的数量
    visited_dq_num = 0
    # 当前正在查询的城市名：城市列表中的第n个元素的key
    cur_dq = list(pos_dqs_arr[cur_dq_index].values())[0]
    print("cur_dq:", cur_dq)


def heyooo(self: little_spiders):
    if self.cur_class_visited_num == self.total_class:
        print("本大类下的小类及区域都已经访问完了，继续下一个区域")
    else:
        print("访问")


if __name__ == '__main__':
    li = little_spiders()
    # heyooo(li)
    # # 首先根据当前正在爬取的分类，
