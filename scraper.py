import scrapy
import os
import re
import sys
import json
class SmogonSpider(scrapy.Spider):
    name = "smogon_spider"
    custom_settings = {
    "AUTOTHROTTLE_ENABLED": True
    }
    def start_requests(self):
        #self.settings.set("AUTOTHROTTLE_ENABLED", True)
        print(self.settings["AUTOTHROTTLE_ENABLED"])
        #sys.exit(1)
        self.download_delay = 0.69
        #urls = ["https://www.smogon.com/forums/forums/past-generation-analyses.148/"]
        urls = [
            "https://www.smogon.com/forums/forums/contributions-corrections.388/",
            "https://www.smogon.com/forums/forums/smogon-metagames.249/"
        ]
        self.WRITE_CT = 0
        self.subforums = []
        self.dir = 'scraped_content'
        for url in urls:
            self.current_page = 1
            yield scrapy.Request(url=url, callback=self.get_subforums, meta={"parent":self.dir})
            #yield scrapy.Request(url=url, callback=self.get_titles, dont_filter=True, meta={"parent":self.dir, "current_page": 1})

    def get_subforums(self, response):
        #page = response.url.split("/")[-2]
        dirname = response.request.url.split("/")
        if dirname[-1] == "":
            dirname = dirname[:-1]
        dirname = ".".join(dirname[-1].split(".")[:-1])
        new_dir = os.path.join(response.meta["parent"], dirname)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        if len(response.css('.block-container')) == 1:
            print("This forum only has subforums?", response.request.url )
        else:
            links_in_first_block = response.css('.block-container')[0].css('a::attr(href)')
            subforums_to_pass_on = []
            for link in links_in_first_block:
                if 'forums/forums' in link.get() and link.get() not in self.subforums and link.get() not in subforums_to_pass_on:
                    subforums_to_pass_on.append(link.get())
            for subforum_url in subforums_to_pass_on:
                print("!!!!!!!!!!", subforum_url)
                self.subforums.append(subforum_url)
                #if
                yield scrapy.Request(url=response.urljoin(subforum_url), callback=self.get_subforums, meta={"parent":new_dir})
                yield scrapy.Request(url=response.urljoin(subforum_url), dont_filter=True, callback=self.get_titles, meta={"parent":new_dir, "current_page": 1})


    def get_titles(self, response):
        #page = response.url.split("/")[-2]
        if not response.request.url in ["https://www.smogon.com/forums/forums/smogon-metagames.249/", "https://www.smogon.com/forums/forums/contributions-corrections.388/"]:
            print("GETTING TITLES", response.meta["parent"])
            if len(response.css('.block-container')) == 1:
                links_in_second_block = response.css('.block-container')[0].css('a::attr(href)')
            else:
                links_in_second_block = response.css('.block-container')[1].css('a::attr(href)')
            titles_to_pass_on = []
            num_links = 0
            for link in links_in_second_block:
                link_url = link.get()
                if 'forums/threads' in link_url and not (link_url.split("/")[-1][:5] == "page-" or link_url.split("/")[-2][:5] == "page-") and not (link_url.split("/")[-1] == 'latest' or link_url.split("/")[-2] == 'latest'):
                    thread_path = re.sub('\/forums\/threads\/', '', link_url)
                    if thread_path[-1] == "/":
                        thread_path = thread_path[:-1]
                    #if not os.path.exists(os.path.join(response.meta["parent"],thread_path)):
                    num_links += 1
                    #with open(os.path.join(response.meta["parent"],thread_path), "w+") as wf:
                    #    wf.close()
                    #    self.WRITE_CT += 1
                    print(response.request.url, link_url)
                    yield scrapy.Request(response.urljoin(link_url), callback=self.parse_thread, meta = {"parent": os.path.join(response.meta["parent"],thread_path), "current_page":1, "current_post":1,"writefile": os.path.join(response.meta["parent"],thread_path)})
            if not num_links == 0:
                next_page = response.urljoin("page-{}".format(response.meta["current_page"] + 1))
                try:
                    yield scrapy.Request(next_page, callback=self.get_titles, meta = {"parent": response.meta["parent"], "current_page":response.meta["current_page"] + 1})
                except Exception:
                    0

    def parse_thread(self, response):
        #page = response.url.split("/")[-2]
        print("PARSING", response.request.url)
        if response.meta["writefile"][-1] == "/":
            wf = response.meta["writefile"][:-1]
        else:
            wf = response.meta["writefile"]
        wf = wf + ".page-{}.json".format(response.meta["current_page"])
        print("PARSING2", response.request.url)
        current_post = response.meta["current_post"]
        with open(wf, "w+") as wf2:
            json.dump({ 'title': response.css("title::text").get(), "page": response.meta["current_page"]}, wf2)
            wf2.write("\n")
            wf2.flush()
            #wf.write()
            num_posts = 0
            for post in response.css(".bbWrapper"):
                json.dump({'post':post.get(), "post-id": current_post}, wf2)#wf.write({
                wf2.write("\n")
                wf2.flush()
                current_post += 1
                num_posts += 1
            #'post':post.get()})
        wf2.close()
        print("COMPLETED PARSING", response.request.url)
        if not num_posts == 0:
            next_page = response.urljoin("page-{}".format(response.meta["current_page"] + 1))
            try:
                yield scrapy.Request(next_page, callback=self.parse_thread, meta={"parent": response.meta["parent"], "current_page":response.meta["current_page"] + 1, "writefile": response.meta["writefile"], "current_post": current_post})
            except Exception:
                0



'''
class SmogonSpider(scrapy.Spider):
    name = "smogon_spider"

    def start_requests(self):
        urls = [
            'https://www.smogon.com/forums/threads/ultra-sun-ultra-moon-battle-mechanics-research-read-post-2.3620030/',
        ]
        for url in urls:
            self.current_page = 1
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        #page = response.url.split("/")[-2]
        yield { 'title': response.css("title::text").get()}
        for post in response.css(".bbWrapper"):
            yield {
            'post':post.get(),
            'post-id'
            }
        self.current_page += 1
        next_page = response.urljoin("page-{}".format(self.current_page))
        try:
            yield scrapy.Request(next_page, callback=self.parse)
        except Exception:
            pass'''
