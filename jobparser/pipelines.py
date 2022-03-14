# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_NAME = 'vacancies'


class JobparserPipeline:
    def __init__(self):
        self.client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.db = self.client[DB_NAME]

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['domain'] = item['domain'][0]
            match = re.fullmatch(
                r'(\w+)\s*(\d+\s*\d+)\s*(\w+)\s*(\d+\s\d+)\s*(\w+)\W+(\D+)',
                self.convert_str(item['salary']))
            if match:
                item['min_salary'] = match.group(2).replace(' ', '')
                item['max_salary'] = match.group(4).replace(' ', '')
                item['currency'] = match.group(5)
                item['invoice_type'] = match.group(6)
            else:
                match = re.fullmatch(r'(\w+)\s*(\d+\s*\d+)\s*(\w+)\W+(\D+)',
                                     self.convert_str(item['salary']))
                if match:
                    if match.group(1) == 'от':
                        item['min_salary'] = match.group(2).replace(' ', '')
                        item['currency'] = match.group(3)
                        item['invoice_type'] = match.group(4)
                    elif match.group(1) == 'до':
                        item['max_salary'] = match.group(2).replace(' ', '')
                        item['currency'] = match.group(3)
                        item['invoice_type'] = match.group(4)
            del item['salary']
            collection = self.db[spider.name]
            collection.update_one({'link': item['link']}, {"$set": item},
                                  upsert=True)
            # так не работает! придется добавить random поле!
            # item["random"] = -1
            # print()
            # пример
            # if len(item["salary"]) > 1:
            #     item["salary_max"] = item["salary"][1]
            # collection.insert_one(item)
            # collection.update_one(item, {"$set": item}, upsert=True)
            # чтобы удалить поле нужно делать то же, что и в обычном словаре
            # item.pop("title")
        return item

    @staticmethod
    def convert_str(convert_object):
        conv_str = "".join(convert_object)
        return " ".join(re.findall(r'[.,–a-zA-Zа-яА-Я0-9]+', conv_str))
