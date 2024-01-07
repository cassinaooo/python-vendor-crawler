from twisted.internet import reactor
from pipelines import MyCrawlerRunner
from settings import WebsiteSettings
from spider import GenericSpider
import os
from urls import URLFinder
from twisted.internet.defer import TimeoutError


def printResult(result):
    for page in result:
        print(
            page["company_name"],
            page["company_url"],
        )


def errorCallback(err, *args, **kwargs):
    if type(err.value) == TimeoutError:
        print(kwargs["company_name"], "timed out")
    else:
        print(err)


def start_crawl():
    with open("./data/in/top-100-vendors.csv", "r") as f:
        vendors = [l.strip() for l in f.readlines()]

    with open("./data/in/urls.csv", "r") as f:
        vendors_to_url = dict([tuple(l.strip().split(",")) for l in f.readlines()])

    runner = MyCrawlerRunner(settings=WebsiteSettings().generate_settings_dict())

    for v in vendors:
        # remove historic file
        f_name = v.replace(" ", "_").lower()

        print("vendor", v)
        print("f_name", f_name)

        scrap_file_location = f"data/out/scrap_output/{f_name}"

        print("scrap_file_location", scrap_file_location)

        if (
            os.path.exists(scrap_file_location)
            and os.path.getsize(scrap_file_location) > 0
        ):
            print("skipping")
            continue
            # os.remove(scrap_file_location)

        if v not in vendors_to_url:
            print("Finding URL...")
            url = URLFinder().run(company=v)
            print("URL ->", url)
        else:
            print("found url in list", vendors_to_url[v])
            url = vendors_to_url[v]

        print("Starting Crawl from", url)

        dfd = runner.crawl(GenericSpider().create(url, scrap_file_location), reactor)

        dfd.addCallback(printResult)
        dfd.addErrback(errorCallback, company_name=v)


if __name__ == "__main__":
    start_crawl()
    reactor.run()
