import urllib2

def DownloadFileFromHttp(url):
    filename = url.split('/')[-1]
    urlobj = urllib2.urlopen(url)
    f = open(filename, 'w')
    meta = urlobj.info()
    filesz = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s bytes: %s" % (filename, filesz)
    
    filesz_dl = 0
    blocksz = 8192
    while True:
        buffer = urlobj.read(blocksz)
        if not buffer:
            break
        filesz_dl += blocksz
        f.write(buffer)
        status = r"%10d [%3.2f%%]" % (filesz_dl, filesz_dl * 100. / filesz)
        status = status + chr(8)*(len(status)+1)
        print status
    f.close()