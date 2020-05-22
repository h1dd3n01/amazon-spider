import json
import os
import random
from operator import itemgetter


class HunterPipeline(object):

    def __init__(self):
        self.json_data = {'main': []}
        super(HunterPipeline, self).__init__()

    def process_item(self, item, spider):
        flag = False
        for i in self.json_data['main']:
            if item['main_item']['title'] in i['title']:
                i['lead'].append(item['secondary_item'])
                i['lead'] = sorted(i['lead'], key=itemgetter('price'))
                flag = True
                break
        if not flag:
            item['main_item']['lead'] = []
            item['main_item']['lead'].append(item['secondary_item'])
            self.json_data['main'].append(item['main_item'])
        return item

    def close_spider(self, spider):
        val = random.randrange(0, 999)
        filename = 'scrapedData{}.json'.format(val)
        while os.path.isfile(filename):
            val = random.randrange(0, 999)
            filename = 'scrapedData{}.json'.format(val)
        with open(filename, 'a+') as f:
            f.write(json.dumps(self.json_data))
            f.close()
