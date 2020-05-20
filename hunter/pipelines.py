import json
import os


class HunterPipeline(object):
    def process_item(self, item, spider):
        if os.path.isfile('scrapedData.json'):
            with open('scrapedData.json', 'r+') as f:
                file = f.read()
                json_file = json.loads(file)
                for i in json_file:
                    if i['title'] == item['main_item']['title']:
                        i['title']['lead'].append(item['secondary_item'])
                        json_file['main'].append(i)
                        f.seek(0)
                        f.write(json.dumps(json_file))
                        f.close()
        else:
            with open('scrapedData.json', 'a+') as f:
                json_file = dict()
                json_file['main'] = []
                item['main_item']['lead'] = []
                item['main_item']['lead'].append(item['secondary_item'])
                json_file['main'].append(item['main_item'])
                f.write(json.dumps(json_file))
                f.close()
        return item




