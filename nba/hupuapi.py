#coding=utf8


import json
import urllib
import urllib2
from lxml import html


class APIClient(object):

    def __init__(self):
        self.menu_url = 'http://v.opahnet.com/nba/tv/'
        self.basic_url = 'http://g.hupu.com/nba/homepage/getMatchBasicInfo?matchId={0}'
        self.live_url = ('http://g.hupu.com/node/playbyplay/matchLives?'
                's_count={0}&match_id={1}&homeTeamName={2}&awayTeamName={3}'
                )
        self.avail_matches = []
        self.match_id = None
        self.last_sid = 0
        self.home_team = ''
        self.away_team = ''

    def init_match(self, idx):
        self.match_id = self.avail_matches[idx]
        self.last_sid = 0
        self.set_basic()

    def get_menus(self):
        try:
            text = urllib2.urlopen(self.menu_url).read()
            text = text.decode('utf8', 'ignore')
            tree = html.fromstring(text)
        except Exception as e:
            return []

        match_list = tree.xpath('//div[@class="match-list"]/dl')
        menu_list = []
        self.avail_matches = []

        for match in match_list:
            date_span = match.xpath('./dt/span[@class="date"]')
            _date = date_span[0].text_content() if date_span else ''
            day_span = match.xpath('./dt/span[@class="day"]')
            _day = day_span[0].text_content()[:3] if day_span else ''

            info_spans = match.xpath('./dd/span')
            _time = info_spans[0].text_content().strip()
            _teams = info_spans[1].text_content().strip()
            _info = info_spans[2].text_content().strip()

            links = match.xpath('./dd/a[@class="link1"]')
            _match_id = int(links[0].get('href').rsplit('.', 1)[0].rsplit('_', 1)[1])

            _datetime = '%s %s %s' % (_date, _day, _time)
            menu = (_match_id, _datetime.encode('utf8'), _teams.encode('utf8'), '')
            menu_list.append(menu)
            self.avail_matches.append(_match_id)

        return menu_list

    def set_basic(self):
        url = self.basic_url.format(self.match_id)
        try:
            text = urllib2.urlopen(url).read()
            data = json.loads(text)
            tree = html.fromstring(data['html'])
        except Exception as e:
            return None

        team_a = tree.xpath('//div[@class="team_vs_box"]/div[@class="team_a"]/div[@class="message"]/p/a')
        self.home_team = team_a[0].text_content().strip().encode('utf8')
        team_b = tree.xpath('//div[@class="team_vs_box"]/div[@class="team_b"]/div[@class="message"]/p/a')
        self.away_team = team_b[0].text_content().strip().encode('utf8')
        return True

    def decode_messages(self, text):
        try:
            tree = html.fromstring(text)
        except Exception as e:
            return []

        item_list = tree.xpath('//tr[@sid]')
        msg_list = []

        for item in item_list:
            sid = float(item.get('sid'))
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
        return msg_list

    def get_messages(self, n=10):
        url = self.live_url.format(self.last_sid, self.match_id,
                urllib.quote(self.home_team),
                urllib.quote(self.away_team),
                )
        try:
            r = urllib2.urlopen(url)
            text = r.read().decode('utf8', 'ignore')
            msg_list = self.decode_messages(text)
        except Exception as e:
            return []

        if msg_list:
            self.last_sid = msg_list[0][0] - 3
        return msg_list[:n]


if __name__ == '__main__':
    api = APIClient()
    api.get_menus()
