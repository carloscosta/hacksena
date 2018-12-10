# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class FiledownloadItem(Item):
    contest_name = Field()
    file_url = Field()
    file_body = Field()
    file_path = Field()
    file_data = Field()

class ResultItem(Item):
    contest_name = Field()
    contest = Field() ## concurso
    draw_date = Field() ## data do sorteio
    dozens = Field() ## dezenas
    winners = Field() ## Ganhadores
