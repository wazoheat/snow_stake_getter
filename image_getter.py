import argparse
import datetime as dt
import pathlib as pl
import urllib.request
import yaml


def save_images(verbose,keep):
    nowstr=dt.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    nowstrm=dt.datetime.utcnow().strftime('%Y%m%d%H%M')
    conf = yaml.safe_load(pl.Path('stakes.yml').read_text())

    # Trick opensnow into thinking we're a browser, thanks Tonny Xu on StackOverflow!
    # https://stackoverflow.com/questions/2364593/urlretrieve-and-user-agent-python/43501438#43501438 
    proxy = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy)
    opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/603.1.30 (KHTML, like Gecko) Version/10.1 Safari/603.1.30')]
    urllib.request.install_opener(opener)

    for entry in conf:
        pl.Path(entry).mkdir(parents=True, exist_ok=True)
        # If you don't include this "?datestring", the server feeds you an old/cached image
        url=f"{conf[entry]['url']}?{nowstrm}"
        localname = f"{entry}/{nowstr}.jpg"
        if verbose:
            print(f"getting {localname} from {url}")
        _,result = urllib.request.urlretrieve(url, localname)
        if verbose:
            print(f"{result.as_string(unixfrom=True)=}")
        if not keep:
            if verbose:
                print("Checking if latest image is new or not")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                     description="Script for saving snowstake images locally")

    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Script will be run with more verbose output')
    parser.add_argument('-k', '--keep_duplicates', action='store_true',
                        help='Script will be run with more verbose output')


    pargs = parser.parse_args()
    save_images(pargs.verbose,pargs.keep_duplicates)
