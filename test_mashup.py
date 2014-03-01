import unittest
import mashup
import json


class TestSteamParser(unittest.testCase):
    """When given a json-formatted Steam API, steam_parser should return
    a list of 2-item lists, containing title and time played.
    """
    def setUp(self):
        self.response = """
{
    "response": {
        "total_count": 8,
        "games": [
            {
                "appid": 242920,
                "name": "Banished",
                "playtime_2weeks": 267,
                "playtime_forever": 267,
                "img_icon_url": "1c499bc7d659ddde65a1cd3f2cd7b6122211b4b1",
                "img_logo_url": "2a62342148979d18e2b50ab8c5eebcfe6c99295c"
            },
            {
                "appid": 252030,
                "name": "Valdis Story: Abyssal City",
                "playtime_2weeks": 183,
                "playtime_forever": 183,
                "img_icon_url": "ac1d5be42d9ab19622df244c24edcf14857fdfba",
                "img_logo_url": "e747759692999a93f3eb267f48f4ef229b605595"
            },
            {
                "appid": 250260,
                "name": "Jazzpunk",
                "playtime_2weeks": 145,
                "playtime_forever": 145,
                "img_icon_url": "6c89bf1c426df1d53dc7b03986977c1693694679",
                "img_logo_url": "4d0aa51a082934215453d77f10b8a985151c37bc"
            },
            {
                "appid": 249590,
                "name": "Teslagrad",
                "playtime_2weeks": 22,
                "playtime_forever": 22,
                "img_icon_url": "5125c2952184a27097abd13bc5c97b6f07685b2e",
                "img_logo_url": "9f5866823d854ecfb37e5fd6718bfa2a65b871bb"
            },
            {
                "appid": 265690,
                "name": "NaissanceE",
                "playtime_2weeks": 16,
                "playtime_forever": 16,
                "img_icon_url": "54258e735824e583e2d8aebe3f72774f887b330f",
                "img_logo_url": "ecb5f1c34ae21f4b4d4f798df93ad211a0c0107d"
            },
            {
                "appid": 273580,
                "name": "Descent 2",
                "playtime_2weeks": 10,
                "playtime_forever": 10,
                "img_icon_url": "57d95b2f2b1f570e8f5a86a04d9cc01f9c58330b",
                "img_logo_url": "a4a20733bdc817e340fbc6cbe28ade2e2c617648"
            },
            {
                "appid": 250180,
                "name": "Metal Slug 3",
                "playtime_2weeks": 3,
                "playtime_forever": 3,
                "img_icon_url": "102c6efe9fc37ecdc929258c52dcaf3d445b873f",
                "img_logo_url": "885f8184221d56282a66da2f70fd3fc46a5eb363"
            },
            {
                "appid": 235210,
                "name": "Strider",
                "playtime_2weeks": 2,
                "playtime_forever": 2,
                "img_icon_url": "363d62e4943638e09dfbd991ffffb6d401859749",
                "img_logo_url": "dd5f5ed41ebc12d5c0b20ce8073dfd163bf83c90"
            }
        ]

    }
}"""
        self.expected = [
            ['Banished', 267],
            ['Valdis Story: Abyssal City', 183],
            ['Jazzpunk', 145],
            ['Teslagrad', 22],
            ['NaissanceE', 16],
            ['Descent 2', 10],
            ['Metal Slug 3', 3],
            ['Strider', 2],
        ]
        self.empty_response = """
{
    "response": {
        "total_count": 0
    }
}"""

    def test_parse_response(self):
        self.assertEqual(mashup.steam_parser(json.loads(self.response)),
            self.expected)

    def test_parse_empty_response(self):
        self.assertRaises(mashup.EmptyError, mashup.steam_parser,
            json.loads(self.empty_response))


class TestMetacriticParser(unittest.testCase):
    """When given a json-formatted metacritic API response, metacritic_parser
    should parse out the game's metascore and return it as an integer.
    """

    def setUp(self):
        self.metacritic_response = """
{
  "result": {
    "name": "Half-Life",
    "score": "96",
    "rlsdate": "1998-10-31",
    "genre": "Sci-Fi",
    "rating": "M",
    "platform": "PC",
    "publisher": "Sierra Entertainment",
    "developer": "Valve Software",
    "url": "http://www.metacritic.com/game/pc/half-life"
  }
}
"""
        self.expected = 96

    def test_metacritic_parser(self):


class TestDetermineTaste(unittest.testCase):
    pass


if __name__ == '__main__':
    unittest.main()
