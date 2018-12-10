# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
import zipfile
from scrapy.selector import Selector
from hacksena.items import FiledownloadItem, ResultItem
from scrapy.exporters import JsonItemExporter


class JsonWriterPipeline(object):
    """
        This pipeline effective write down the JSON output
    """
    def __init__(self):
        self.file = open('items-hacksena.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()
    
    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()
    
    def process_item(self, item, spider):
        for i in item:
            self.exporter.export_item(i)
        return item


class ResultsPipeline(object):
    """
        This pipeline grab the HTML extracted and 
        return ResultItem() preparing to write down 
        the JSON 
    """
    def results_item(self, contest_name, results_list):
        final_list = []
        for rl in results_list:
            ri = ResultItem()
            ri['contest_name'] = contest_name
            ri['contest'] = rl[0]
            ri['draw_date'] = rl[1]
            if contest_name == "Mega Sena":  
                ri['dozens'] = rl[2:8]
                ri['winners'] = rl[9]
            elif contest_name == "Super Quina":
                ri['dozens'] = rl[2:7]
                ri['winners'] = rl[8]
            elif contest_name == 'Loto Fácil':
                ri['dozens'] = rl[2:17]
                ri['winners'] = rl[18]
            elif contest_name == 'Dupla Sena':
                ri['dozens'] = rl[2:8]
                ri['winners'] = rl[9]
            elif contest_name == 'Loto Mania':
                ri['dozens'] = rl[2:22]
                ri['winners'] = rl[23]
            final_list.append(ri)
        return final_list


    def process_item(self, item, spider):
        final_list = []
        for line in item['file_data'].xpath('.//tr'):
            tmp_list =[]
            for col in line.xpath('.//td[@rowspan]/text()'):
                tmp_list.append(col.extract())
            if len(tmp_list) > 0:
                final_list.append(tmp_list)
        return self.results_item(item['contest_name'], final_list)


class HacksenaPipeline(object):
    """
        This pipeline extract zip files content HTML
        returning Item() with file_data = Selector()
    """
    def process_item(self, item, spider):
        with open(item['file_path'], "wb") as f:
            f.write(item['file_body'])
        ## remove body, keeping path as reference
        item['file_body'] = None; del item['file_body']
        with zipfile.ZipFile(item['file_path']) as zf:
            for i in zf.infolist():
                if "HTM" in i.filename:
                    try:
                        item['file_data'] = Selector(text=zf.read(i.filename))
                    except KeyError:
                        print('ERROR: Did not find {} in zip file'.format(i.filename))
        ## remove temp files and let item be processed by other pipelines
        os.remove(item['file_path'])
        return item
