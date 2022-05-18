import threading
import os
import shutil
import time
import urllib.request

if not os.path.isfile('links.txt'):
    print('please create a "links.txt" file with the links')
    exit()

def list_splitter(links, n=None):
    if n == None:
        return links
    l = []
    for x in range(0,len(links),n):
        l.append(links[x:x+n])
    return l

class Downloader:
    def __init__(self, links=[], path='', debug = False):
        self._links = links
        self._use_threads = False
        self._path = path
        self._debug = debug
        if self._path and not os.path.isdir(self._path):
            os.makedirs(self._path)
    
    def _download_link(self, url):
        if self._debug:
            print('downloading %s' % url)
        with urllib.request.urlopen(url) as response, open(os.path.join(self._path, url.split('/')[-1]), 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
    
    def download(self):
        if self._use_threads:
            for current_links in self._links:
                for current_link in current_links:
                    threads = []
                    t = threading.Thread(target=self._download_link, args=(current_link,))
                    t.start()
                    threads.append(t)
                for thread in threads:
                    thread.join()
        else:
            for d in self._links:
                self._download_link(d)
            
        
    def use_threads(self, simultaneous_downloads=5):
        self._links = list_splitter(self._links, simultaneous_downloads)
        self._simultaneous_downloads = simultaneous_downloads
        self._use_threads = True
        
if __name__ == "__main__":
    t1 = time.time()
    links = open('links.txt', 'r').read().splitlines()
    my_downloader = Downloader(links=links, path='output', debug=True)
    my_downloader.use_threads()
    my_downloader.download()
    print()
    print(time.time()-t1)
