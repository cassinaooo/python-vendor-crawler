#### Setup:
Put your Bing Key into `config.py`.

#### Running:

```sh
$ python __main__.py
```

The script will load `data/in/top-100-vendors.csv` and `data/in/urls.csv`.

If a vendor URL is found, it will crawl that page and save the data in `./data/out/{vendor_name}`.

If a vendor URL is not found, it will first use the Bing API to fetch the first result and proceed from there.

