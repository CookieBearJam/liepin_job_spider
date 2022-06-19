class Proxymodel(object):
    def __init__(self, proxy_dict):
        proxy = proxy_dict['data'][0]
        self.proxy_url = "https://" + proxy['ip'] + ":" + str(proxy['port'])
        self.is_blacked = False
