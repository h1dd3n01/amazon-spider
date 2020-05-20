import json
import os
import bisect


class HunterPipeline(object):
    count = 0

    def process_item(self, item, spider):
        self.count += 1
        print('-' * 20)
        print('-' * 20)
        print(self.count)
        print('-' * 20)
        print('-' * 20)
        flag = False
        if os.path.isfile('scrapedData.json'):
            with open('scrapedData.json', 'r+') as f:
                file = f.read()
                json_file = json.loads(file)
                for i in json_file['main']:
                    if item['main_item']['title'] in i['title']:
                        i['lead'].append(item['secondary_item'])
                        # json_file['main'].append(i)
                        f.seek(0)
                        f.write(json.dumps(json_file))
                        f.close()
                        flag = True
                        break
                if not flag:
                    item['main_item']['lead'] = []
                    item['main_item']['lead'].append(item['secondary_item'])
                    json_file['main'].append(item['main_item'])
                    f.seek(0)
                    f.write(json.dumps(json_file))
                    f.close()

        else:
            with open('scrapedData.json', 'a+') as f:
                json_file = {'main': []}
                item['main_item']['lead'] = []
                item['main_item']['lead'].append(item['secondary_item'])
                json_file['main'].append(item['main_item'])
                f.write(json.dumps(json_file))
                f.close()
        return item
