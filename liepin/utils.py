import hashlib
import re
import datetime


# def filter_repeatness(url):
#     # 待加密信息
#     # str01 = 'This is your md5 password!'
#     # 创建md5对象
#     md5_obj = hashlib.md5()
#     # 进行MD5加密前必须 encode(编码)，python里默认是unicode编码，必须转换成utf-8
#     # 否则报错：TypeError: Unicode-objects must be encoded before hashing
#     md5_obj.update(url.encode(encoding='utf-8'))
#
#     print('加密之前的url为 ：' + url)
#     # "this is your md5 password!"==>0a5f76e7b0f352e47fed559f904c9159
#     # url from liepin is :383588332b521e7368729169cd8f52a5  ==>383588332b521e7368729169cd8f52a5(在线的生成结果是这样的)
#     print('MD5加密后为 ：' + md5_obj.hexdigest())


# 传入需要加密的url串,返回md5加密后小写形式的32字节字符串


def get_md5(url: str) -> str:
    md5_obj = hashlib.md5()
    md5_obj.update(url.encode(encoding='utf-8'))
    md5_obj.digest()
    return md5_obj.hexdigest()


def convert_md5(origin):
    result = []
    s = ""
    for i in range(len(origin)):
        s += origin[i]
        if i % 2 != 0:
            int_hex = int(s, 16)
            result.append(int_hex)
            s = ""

    return result


def dec2str(dec_arr):
    s = ""
    for e in dec_arr:
        s += chr(e)

    return s


# if __name__ == "__main__":
# sum = get_md5("hello world")
# print(sum)
# print(len(sum))
# cv_sum = convert_md5(sum)
# print(cv_sum)
# print(len(cv_sum))
# hex_str = dec2str(cv_sum)
# print(hex_str)
# print(len(hex_str))

class LPUtils:
    @staticmethod
    def get_city_locale(dq: str) -> list:
        pattern = re.compile("[\u4e00-\u9fa5]+")
        return pattern.findall(dq)

    @staticmethod
    def get_salary_by_reg(salary: str) -> list:
        pattern = re.compile("[0-9]+")
        return pattern.findall(salary)

    @staticmethod
    def get_time_now_str():
        cur_time = datetime.datetime.now()
        cur_time_str = cur_time.strftime('%Y-%m-%d %H:%M:%S')
        return cur_time_str


if __name__ == '__main__':
    # print(LPUtils.get_time_now_str())
    # ds_str = LPUtils.get_datetime_str()
    # print(ds_str)
    # ds_str = LPUtils.get_datetime_str('time')
    # print(ds_str)
    # cur_time = datetime.datetime.now()
    # time1_str = cur_time.strftime('%Y-%m-%d %H:%M:%S')
    # print(time1_str)

# if __name__ == "__main__":
#     pos_class_arr = [
#         {"开发": ["Java", "Php", "Python", "Ruby", "Node.JS", ".NET", "ASP", "C#", "C++", "C", "Delphi", "Go",
#                 "Docker", "Hadoop", "Spark", "HBase", "Openstack", "数据挖掘", "自然语言处理", "推荐系统", "搜索引擎", "全栈工程师"]
#          }
#     ]
#     total_class = 400 * len(pos_class_arr) * len(pos_class_arr[0]["开发"])
#     print(len(pos_class_arr), len(pos_class_arr[0]["开发"]), total_class)
#
#     dq_str = "上海市-静安区"
#     locale_list = get_city_locale(dq_str)
#     print(locale_list)
#
    salary_list = LPUtils.get_salary_by_reg("18-20k·15薪")
    print(salary_list)
    print(LPUtils.get_salary_by_reg("19-20k"))
    if LPUtils.get_salary_by_reg("19-20k"):
        print("19-20k长度：", len(LPUtils.get_salary_by_reg("19-20k")))
    else:
        print("19-20k回结果为空")

    print(LPUtils.get_salary_by_reg("面议"))
#
#     print(get_salary_by_reg("面议"))
#     if get_salary_by_reg("面议"):
#         print("面议非空")
#     else:
#         print("面议返回结果为空")
# dq_str = unicode(dq_str, 'utf8')
# re_words = re.compile(r"[\x80-\xff]+")
# m = re_words.search(dq_str, 0)
#
# print(m)
# print(m.group())

# url = 'https://www.liepin.com/job/1946499083.shtml?d_sfrom=search_prime&amp;d_ckId=e750589681a4f44f67e92a4a617e50bf&amp;d_curPage=0&amp;d_pageSize=40&amp;d_headId=e750589681a4f44f67e92a4a617e50bf&amp;d_posi=0&amp;skId=6d94f4ef80dbeddd96d4182dcce1e78a&amp;fkId=6d94f4ef80dbeddd96d4182dcce1e78a&amp;ckId=6d94f4ef80dbeddd96d4182dcce1e78a&amp;sfrom=search_job_pc&amp;curPage=0&amp;pageSize=40&amp;index=0'
# print(url2md5_str(url))
