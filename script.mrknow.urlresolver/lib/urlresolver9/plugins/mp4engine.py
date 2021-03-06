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
from lib import jsunpack
from urlresolver9 import common
from urlresolver9.resolver import UrlResolver, ResolverError


class Mp4EngineResolver(UrlResolver):
    name = "mp4engine"
    domains = ["mp4engine.com"]
    pattern = '(?://|\.)(mp4engine\.com)/(?:embed-)?([0-9a-zA-Z]+)(?:-[0-9]x[0-9].html)?'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url).content

        js_data = re.findall('(eval\(function.*?)</script>', html.replace('\n', ''))

        for i in js_data:
            try: html += jsunpack.unpack(i)
            except: pass

        match = re.search('''file:(?:\s+|\v+)?['|"]([^'"]+)['|"]''', html)

        if match:
            return match.group(1).replace(" ", "%20")

        raise ResolverError('File Not Found or removed')

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id)
