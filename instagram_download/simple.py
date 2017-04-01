#!/usr/bin/env python
from ins_download import InsDownload
from pprint import pprint

a = InsDownload("https://www.instagram.com/p/BP675G0FsWy/?taken-by=ruiazhou&hl=en")
pprint(a.start())
