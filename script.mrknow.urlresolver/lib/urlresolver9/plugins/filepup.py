"""
    urlresolver XBMC Addon
    Copyright (C) 2015 tknorris

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
import urllib
from urlresolver9 import common
from urlresolver9.resolver import UrlResolver, ResolverError
from lib import helpers
import xbmcgui

class FilePupResolver(UrlResolver):
    name = "filepup"
    domains = ["filepup.net"]
    pattern = '(?://|\.)(filepup.(?:net))/(?:play|files)/([0-9a-zA-Z]+)'
    headers = {'User-Agent': common.SMU_USER_AGENT}

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        html = self.net.http_GET(web_url, headers=self.headers).content
        default_url = self.__get_def_source(html)
        if default_url:
            qualities = self.__get_qualities(html)
            def_quality = self.__get_default(html)
            if len(qualities) <= 1:
                pick_quality = def_quality
            elif self.get_setting('auto_pick') == 'true':
                pick_quality = ''
                best_height = 0
                for quality in qualities:
                    height = int(quality[:-1])
                    if height > best_height:
                        pick_quality = quality
            else:
                result = xbmcgui.Dialog().select('Choose the link', qualities)
                if result == -1:
                    raise ResolverError('No link selected')
                else:
                    pick_quality = qualities[result]

            if not def_quality or pick_quality == def_quality:
                return default_url
            else:
                return default_url.replace('.mp4?', '-%s.mp4?' % (pick_quality))
        else:
            raise ResolverError('Unable to location download link')

    def __get_def_source(self, html):
        default_url = ''
        match = re.search('sources\s*:\s*\[(.*?)\]', html, re.DOTALL)
        if match:
            match = re.search('src\s*:\s*"([^"]+)', match.group(1))
            if match:
                default_url = match.group(1) + helpers.append_headers(self.headers)
        return default_url

    def __get_default(self, html):
        match = re.search('defaultQuality\s*:\s*"([^"]+)', html)
        if match:
            return match.group(1)
        else:
            return ''

    def __get_qualities(self, html):
        qualities = []
        match = re.search('qualities\s*:\s*\[(.*?)\]', html)
        if match:
            qualities = re.findall('"([^"]+)"', match.group(1))
        return qualities

    def get_url(self, host, media_id):
        return 'http://www.filepup.net/play/%s' % (media_id)

    @classmethod
    def get_settings_xml(cls):
        xml = super(cls, cls).get_settings_xml()
        xml.append('<setting id="%s_auto_pick" type="bool" label="Automatically pick best quality" default="false" visible="true"/>' % (cls.__name__))
        return xml
