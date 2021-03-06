"""
    urlresolver XBMC Addon
    Copyright (C) 2011 t0mm0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import re
import base64
import urllib
from urlresolver9 import common
from urlresolver9.resolver import UrlResolver

class TrollVidResolver(UrlResolver):
    name = 'trollvid.net'
    domains = ['trollvid.net', 'mp4edge.com']
    pattern = '(?://|\.)((?:trollvid\.net|mp4edge\.com))/(?:embed\.php.file=|embed/|stream/)([0-9a-zA-Z]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)

        html = self.net.http_GET(web_url).content

        try: stream_url = re.search('url\s*:\s*"(http.+?)"', html).group(1)
        except: pass

        try: stream_url = re.search('unescape\(\'(http.+?)\'', html).group(1)
        except: pass

        try: stream_url = base64.b64decode(re.search('atob\(\'(.+?)\'', html).group(1))
        except: pass

        stream_url = urllib.unquote_plus(stream_url)

        return stream_url

    def get_url(self, host, media_id):
        return 'http://trollvid.net/embed/%s' % media_id
