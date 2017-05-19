# instagram-download
This async script can help you to download Instagram photos.

## How to Use?
Example

``` python
#!/usr/bin/env python
from ins_download import InsDownload
from pprint import pprint

a = InsDownload("https://www.instagram.com/p/BRfGLzsDAFe/?taken-by=mr.mo.2017")
pprint(a.start())
```
Downloaded photo will be saved in the folder