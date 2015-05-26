#coding=utf8


import urllib
import urllib2
from lxml import html


class APIClient(object):

    def __init__(self):
        self.menu_url = 'http://v.opahnet.com/nba/tv/'
        self.base_url = ('http://g.hupu.com/node/playbyplay/matchLives?'
                's_count={0}&match_id={1}&homeTeamName={2}&awayTeamName={3}'
                )
        self.match_id = 150115
        self.last_sid = 0
        self.home_team = '火箭'
        self.away_team = '勇士'

    def get_menu(self):
        try:
            text = urllib2.urlopen(self.menu_url).read()
            text = text.decode('utf8', 'ignore')
            tree = html.fromstring(text)
        except Exception as e:
            return []

        match_list = tree.xpath('//div[@class="match-list"]')
        menu_list = []

        for match in match_list:
            date_span = match.xpath('./dl/dt/span[@class="date"]')
            _date = date_span[0].text_content() if date_span else ''
            day_span = match.xpath('./dl/dt/span[@class="day"]')
            _day = day_span[0].text_content() if day_span else ''

            info_spans = match.xpath('./dl/dd/span')
            _time = info_spans[0].text_content()
            _teams = info_spans[1].text_content()
            _info = info_spans[2].text_content()

            _datetime = '%s %s %s' % (_date, _day, _time)
            menu = (_datetime, _teams, _info)
            menu_list.append(menu)

        return menu_list

    def decode_messages(self, text):
        try:
            tree = html.fromstring(text)
        except Exception as e:
            return []

        item_list = tree.xpath('//tr[@sid]')
        msg_list = []

        # DEBUG
        #item_list = item_list[-10:]
        for item in item_list:
            sid = int(item.get('sid'))
            tabs = item.xpath('.//td')
            if item.get('class') == 'pause' and len(tabs) == 1:
                content = tabs[0].text_content().encode('utf8', 'ignore')
                msg = (sid, '--', '----', '--', content)
            elif len(tabs) == 4:
                residual = tabs[0].text_content()
                team = tabs[1].text_content().encode('utf8', 'ignore')
                content = tabs[2].text_content().encode('utf8', 'ignore')
                scores = tabs[3].text_content()
                msg = (sid, residual, scores, team, content)
            else:
                continue
            msg_list.append(msg)

        # sorted by sid desc
        msg_list.sort(key=lambda x:-x[0])
        # debug
        return msg_list[-20:]
        return msg_list

    def get_messages(self, n=10):
        url = self.base_url.format(self.last_sid, self.match_id,
                urllib.quote(self.home_team),
                urllib.quote(self.away_team),
                )
        try:
            r = urllib2.urlopen(url)
            text = r.read().decode('utf8', 'ignore')
            msg_list = self.decode_messages(text)
        except Exception as e:
            print e
            return []

        if msg_list:
            self.last_sid = msg_list[0][0] - 3
        return msg_list[:n]


if __name__ == '__main__':
    api = APIClient()
    msgs = api.get_messages()
    for msg in msgs:
        print msg

    menus = api.get_menu()
    print menus
