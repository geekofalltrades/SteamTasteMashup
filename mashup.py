import requests
import json
import re
from urlparse import parse_qs


class SteamError(BaseException):
    pass


class MetaError(BaseException):
    pass


class EmptyError(BaseException):
    pass


def dispatcher(environ, start_response):
    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        query = environ.get('QUERY_STRING', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path, query)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except SteamError:
        status = "404 Not Found"
        body = draw_error_page("""Either this Steam ID doesn't exist, or this user has made their profile private or friends-only.""")
    except MetaError:
        status = "404 Not Found"
        body = draw_error_page("""Metacritic doesn't have information on any of the games this user has played over the last two weeks.""")
    except EmptyError:
        status = "200 OK"
        body = draw_error_page("""This player hasn't played any games at all over the last couple weeks.""")
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body]


def resolve_path(path, query):
    urls = [(r'^$', draw_home_page),
            (r'^id', lookup)]
    matchpath = path.lstrip('/')
    for regexp, func in urls:
        match = re.match(regexp, matchpath)
        if match is None:
            continue
        #args = match.groups([])
        args = parse_qs(query)
        if args:
            args = [args.get('id', [''])[0]]
        return func, args

    raise NameError


def home_page_contents():
    return """
<h1>Steam Taste Finder</h1>
<h3>Objectively and scientifically determine your taste in videogames.</h3>
<p>To begin, enter your Steam ID.</p>
<form action="id" method="GET">
    <input type="text" id="idfield" name="id" />
    <input type="submit" id="submitbutton" />
</form>
<p>If you don't know your Steam ID, find it using the <a href="http://steamidfinder.com/">Steam ID Finder.</a></p>
"""


def privacy_policy_contents():
    """A privacy policy, as required by Valve for use of the Steam API."""
    return """
<p><b>Privacy Policy:</b> Neither the information entered here nor the information accessed in the process of determining your taste are stored in any place or form, nor are these data used to any other end."""


def draw_home_page():
    """Print the homepage."""
    return home_page_contents() + privacy_policy_contents()


def draw_error_page(error):
    page = """
<h1>Whoops</h1>
<p>%s</p>
""" % error

    return home_page_contents() + page + privacy_policy_contents()


def draw_response_page(taste=None, steam_resp=None):
    """Print the response page."""
    page = home_page_contents()
    page += """
<h1>Your taste is %s/100.</h1>
""" % taste
    if taste >= 90:
        page += "<h2>You are a true connoisseur.</h2>"
    elif taste >= 80:
        page += "<h2>8/10, would game with.</h2>"
    elif taste >= 70:
        page += "<h2>We can agree to disagree.</h2>"
    elif taste >= 60:
        page += "<h2>There's no accounting for taste.</h2>"
    elif taste >= 50:
        page += "<h2>Why?</h2>"
    else:
        page += "<h2>Just leave.</h2>"

    page += """
<h4>Your playtime over the last couple of weeks breaks down as follows:</h4>
<table>
    <tr>
        <td>Game</td>
        <td>Time Played</td>
        <td>Metascore</td>
    </tr>"""

    for game, hours, score in steam_resp:
        page += """
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    </tr>""" % (game, hours, score)

    page += """
</table>"""

    return str(page + privacy_policy_contents())


def lookup(steam_id):
    """Look up the given steamid and call steam_parser to get a list of
    games they play and how long they've played them. Then look up each game
    on metacritic and call metacritic_parser to get the score associated
    with that game. Then call determine_taste to calculate an objective and
    scientific summarization of the given steamid's taste. Finally, print
    out a webpage summarizing the results.
    """
    with open('keys.txt') as keyfile:
        steam_key = keyfile.readline().rstrip()
        meta_key = keyfile.readline().rstrip()

    steam_url = \
        'http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/'

    meta_url = 'https://byroredux-metacritic.p.mashape.com/find/game'
    meta_header = {'X-Mashape-Authorization': meta_key}

    steam_params = {'key': steam_key, 'steamid': str(steam_id),
        'format': 'json'}
    try:
        resp = requests.get(steam_url, params=steam_params)
        resp.raise_for_status()
        steam_resp = steam_parser(json.loads(resp.text))
    except:
        raise SteamError

    found = 0
    for i in xrange(len(steam_resp)):
        meta_data = {'title': steam_resp[i][0], 'platform': 3}
        try:
            resp = requests.post(meta_url, data=meta_data, headers=meta_header)
            resp.raise_for_status()
        except:
            steam_resp[i].append('N/A')
        else:
            steam_resp[i].append(metacritic_parser(json.loads(resp.text)))
            found += 1

    if not found:
        raise MetaError

    taste = determine_taste(steam_resp)

    return draw_response_page(taste, steam_resp)


def steam_parser(payload):
    if not int(payload['response']['total_count']):
        raise EmptyError

    payload = payload['response']['games']

    response = []
    for game in payload:
        sub_response = []
        sub_response.append(game['name'])
        sub_response.append(int(game['playtime_2weeks']))

        response.append(sub_response)

    return response


def metacritic_parser(payload):
    return int(payload['result'].get('score', 0))


def determine_taste(data):
    taste = 0
    total_hours = 0
    for game, hours, score in data:
        if not isinstance(score, int):
            continue
        taste += hours * score
        total_hours += hours

    if not total_hours:
        raise EmptyError

    return taste / (total_hours if total_hours else 1)


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, dispatcher)
    srv.serve_forever()
