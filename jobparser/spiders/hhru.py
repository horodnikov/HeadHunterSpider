import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = [
        'https://hh.ru/search/vacancy?&fromSearchLine=true&text=python'
    ]

    def parse(self, response: HtmlResponse):
        vacancy_links = response.xpath(
            '//div[contains(@class, "vacancy-serp-item")]'
            '//a[contains(@data-qa, "vacancy-title")]/@href').getall()
        for link in vacancy_links:
            yield response.follow(link, callback=self.parse_vacancies)

        next_page = response.xpath(
            '//a[contains(@data-qa, "pager-next")]/@href').get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_vacancies(self, response: HtmlResponse):
        domain = self.allowed_domains
        link = response.url
        title = response.xpath(
            "//h1[contains(@data-qa, 'title')]//text()").get()
        salary = response.xpath(
            "//div[contains(@data-qa, 'salary')]//text()").getall()
        yield JobparserItem(domain=domain, link=link, title=title, salary=salary)
