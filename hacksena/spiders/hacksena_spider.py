
import os
import scrapy
import posixpath
from hacksena.items import FiledownloadItem
from urllib.parse import urlsplit, unquote

class QuotesSpider(scrapy.Spider):
    name = "hacksena"

    def start_requests(self):
        urls = [
            'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_megase.zip',
            'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_quina.zip',
            'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotfac.zip',
            'http://www1.caixa.gov.br/loterias/_arquivos/loterias/d_dplsen.zip',            
            'http://www1.caixa.gov.br/loterias/_arquivos/loterias/D_lotoma.zip'
        ]
        for u in urls:
            yield scrapy.Request(url=u, callback=self.parse)


    def url2filename(self, url):
        "Return basename corresponding to url"
        urlpath = urlsplit(url).path
        basename = posixpath.basename(unquote(urlpath))
        if (os.path.basename(basename) != basename or
            unquote(posixpath.basename(urlpath)) != basename):
            raise ValueError
        return basename


    def parse(self, response):
        i = FiledownloadItem()
        i['file_body'] = response.body
        i['file_url'] = response.url
        i['file_path'] = self.url2filename(i['file_url'])
        if i['file_path'] == 'D_megase.zip':
            i['contest_name'] = 'Mega Sena'
        elif i['file_path'] == 'D_quina.zip':
            i['contest_name'] = 'Super Quina'
        elif i['file_path'] == 'D_lotfac.zip':
            i['contest_name'] = 'Loto Fácil'
        elif i['file_path'] == 'd_dplsen.zip':
            i['contest_name'] = 'Dupla Sena'
        elif i['file_path'] == 'D_lotoma.zip':
            i['contest_name'] = 'Loto Mania'
        yield i

