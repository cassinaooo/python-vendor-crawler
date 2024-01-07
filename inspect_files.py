import os

from scrapy.downloadermiddlewares.httpauth import HttpAuthMiddleware


def start_crawl():
    with open("./data/in/top-100-vendors.csv", "r") as f:
        vendors = [l.strip() for l in f.readlines()]

    with open("./data/in/urls.csv", "r") as f:
        vendors_to_url = dict([tuple(l.strip().split(",")) for l in f.readlines()])

    for v in vendors:
        # remove historic file
        f_name = v.replace(" ", "_").lower()

        scrap_file_location = f"data/out/scrap_output/{f_name}"

        if (
            os.path.exists(scrap_file_location)
            and os.path.getsize(scrap_file_location) > 0
        ):  # existing, non-empty file
            continue
        else:
            print("scrap_file_location", scrap_file_location)

            print("vendor", v)
            print("f_name", f_name)
            print("will scrap")


if __name__ == "__main__":
    start_crawl()
