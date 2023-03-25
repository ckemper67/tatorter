# -*- coding: utf-8 -*-
# tatorter
# Copyright (C) 2018  Daniel Llin Ferrero
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
Created on 04.02.2018

@author: DLF
'''

import mechanicalsoup as ms
import logging
from tatorterp import Episode
logger = logging.getLogger("tatorter")
logging.basicConfig()

team_to_location = {
    "Ballauf und Schenk /Saalfeld und Keppler":"Köln-Leipzig",
    "Ballauf und Schenk":"Köln",
    "Batic und Leitmayr / Faber": "München-Dortmund",
    "Batic und Leitmayr":"München",
    "Batu":"Hamburg",
    "Berlinger und Rascher":"Freiburg",
    "Berlinger":"Freiburg",
    "Blum und Perlmann":"Konstanz",
    "Blum und Perlmann, Matteo Lüthi":"Konstanz",
    "Borowski /Lindholm":"Kiel-Hannover",
    "Borowski und Brandt":"Kiel",
    "Borowski und Sahin":"Kiel",
    "Borowski":"Kiel",
    "Eisner und Fellner":"Wien",
    "Eisner":"Wien",
    "Faber und Bönisch":"Dortmund",
    "Faber, Bönisch und Dalay":"Dortmund",
    "Faber, Bönisch, Dalay und Kossik":"Dortmund",
    "Faber, Bönisch, Dalay und Pawlak / Batic und Leitmayr": "Dortmund-München",
    "Faber, Bönisch, Dalay und Pawlak":"Dortmund",
    "Faber, Bönisch, Pawlak und Herzog":"Dortmund",
    "Faber, Pawlak und Herzog":"Dortmund",
    "Falke und Grosz":"Hamburg",
    "Falke und Lorenz":"Hamburg",
    "Flückiger und Lanning":"Luzern",
    "Flückiger und Ritschard":"Luzern",
    "Funck, Schaffert und Grewel":"Erfurt",
    "Gorniak, Winkler und Schnabel": "Dresden",
    "Grandjean und Ott": "Zürich",
    "Janneke und Brix":"Frankfurt",
    "Kappl und Deininger":"Saarbrücken",
    "Karow":"Berlin",
    "Lannert und Bootz":"Stuttgart",
    "Lessing und Dorn":"Weimar",
    "Lindholm und Schmitz":"Hannover",
    "Lindholm":"Hannover",
    "Lürsen und Stedefreund":"Bremen",
    "Moormann und Selb":"Bremen",
    "Moormann, Andersen und Selb": "Bremen",
    "Murot und Wächter":"Wiesbaden",
    "Murot":"Wiesbaden",
    "Odenthal und Kopper":"Ludwigshafen",
    "Odenthal und Stern":"Ludwigshafen",
    "Ritter und Stark":"Berlin",
    "Rubin und Karow":"Berlin",
    "Saalfeld und Keppler /Ballauf und Schenk":"Leipzig-Köln",
    "Saalfeld und Keppler":"Leipzig",
    "Schimanski und Thanner":"Duisburg",
    "Schürk und Hölzer":"Saarbrücken",
    "Schürk und Hölzer, Baumann und Heinrich":"Saarbrücken",
    "Sieland, Gorniak und Schnabel":"Dresden",
    "Sieland, Gorniak, Mohr und Schnabel":"Dresden",
    "Stark":"Berlin",
    "Steier und Mey":"Frankfurt",
    "Steier":"Frankfurt",
    "Stellbrink und Marx":"Saarbrücken",
    "Thiel und Boerne":"Münster",
    "Tobler und Berg":"Freiburg",
    "Tschiller und Gümer":"Hamburg",
    "Voss und Ringelhahn":"Franken",
    "Voss, Ringelhahn, Goldwasser, Fleischer und Schatz":"Franken",
}

class WikipdediaDEGrabber(object):
    url = "https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen"
    def __init__(self):
        browser = ms.StatefulBrowser()
        browser.open(WikipdediaDEGrabber.url)
        tables = browser.get_current_page().find_all(name='table',
                                                     attrs={'class':'wikitable sortable tabelle-kopf-fixiert'})
        assert len(tables) == 3, "Page content unexpected, not exactly three wikitables. Cannot parse it."
        tbodys = tables[0].find_all("tbody")
        assert len(tbodys) == 1, "Page content unexpected, more than one tbody in wikitable. Cannot parse it."
        trs = tbodys[0].find_all("tr")
        logger.info("Parsing {} epsiode rows from {}.".format(len(trs), WikipdediaDEGrabber.url))
        self.episodes = []
        last_epsiode = None
        last_values = None
        season = 1969
        for tr in trs[1:]:
            tds = tr.find_all('td')
            values = [td.text.split('(')[0].strip() for td in tds]
            episode_index = int(values[0].replace('a*','').replace('b*',''))
            team = values[4]
            if team not in team_to_location:
                if episode_index > 1400:
                    logger.warning("Location for team {} unknown and episode later than 1100. Script should be updated!".format(team))
                location = "[{}]".format(team)
            else:
                location = team_to_location[team]
            # strip of trailing [footnote]
            premiere = values[3].split('[')[0]
            year = int(premiere[-4:])
            if year > season:
                season = year
                first_episode = episode_index
            episode = Episode(
                episode_index = episode_index,
                location = location,
                title = values[1],
                broadcaster = values[2],
                premiere = premiere,
                team = team,
                case_index = values[5],
                author = values[6],
                director = values[7],
                episode = episode_index - first_episode + 1,
                season = season
            )
            self.episodes.append(episode)
            last_epsiode = episode
            last_values = values
            
                
        
        
#print (WikipdediaDEGrabber().episodes)

    
