[![Build Status](https://travis-ci.org/geekofalltrades/SteamTasteMashup.png?branch=master)](https://travis-ci.org/geekofalltrades/SteamTasteMashup)

Steam Taste Mashup
------

####Overview
Given a Steam ID number, this web app will determine your taste in videogames.
Then it will _judge_ your taste.

####Approach
The mashup interfaces with the [Steam API](http://steamcommunity.com/dev)
and byroredux's [Unofficial Metatcritic API](https://www.mashape.com/byroredux/metacritic#!documentation)
to interface with Steam, retrieve stats on games played in the last two weeks for the given user,
then retrieve Metacritic scores for each of those games. It calculates a weighted Metascore average
for the time you've played over the last two weeks as an indicator of your taste. Then it _judges_.
It is quite judgemental.

####Requirements
To replicate my exact environment, see requirements.txt. In addition, however, you will need a Steam
API key and a Mashape key set to allow access to the Unofficial Metacritic API. These keys should be
placed in a file called "keys.txt", with the Steam key on the first line and the Mashape key on the
second.