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
                print('Added item')
                break
        if not flag:
            print('Added new item')
            item['main_item']['lead'] = []
            item['main_item']['lead'].append(item['secondary_item'])
            self.json_data['main'].append(item['main_item'])
        return item

    def close_spider(self, spider):
        print('Spider in closing phase')
        val = random.randrange(0, 999)
        filename = 'scrapedData{}.json'.format(val)
        while os.path.isfile(filename):
            val = random.randrange(0, 999)
            filename = 'scrapedData{}.json'.format(val)
        with open(filename, 'a+') as f:
            print('File was opened')
            f.write(json.dumps(self.json_data))
            f.close()


    # def process_item(self, item, spider):
    #
    #     flag = False
    #     if os.path.isfile('scrapedData.json'):
    #         with open('scrapedData.json', 'r+') as f:
    #             file = f.read()
    #             json_file = json.loads(file)
    #             for i in json_file['main']:
    #                 if item['main_item']['title'] in i['title']:
    #                     i['lead'].append(item['secondary_item'])
    #                     # json_file['main'].append(i)
    #                     f.seek(0)
    #                     f.write(json.dumps(json_file))
    #                     f.close()
    #                     flag = True
    #                     break
    #             if not flag:
    #                 item['main_item']['lead'] = []
    #                 item['main_item']['lead'].append(item['secondary_item'])
    #                 json_file['main'].append(item['main_item'])
    #                 f.seek(0)
    #                 f.write(json.dumps(json_file))
    #                 f.close()
    #
    #     else:
    #         with open('scrapedData.json', 'a+') as f:
    #             json_file = {'main': []}
    #             item['main_item']['lead'] = []
    #             item['main_item']['lead'].append(item['secondary_item'])
    #             json_file['main'].append(item['main_item'])
    #             f.write(json.dumps(json_file))
    #             f.close()
    #     return item
