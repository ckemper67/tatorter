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

import re
import logging
import requests
from bs4 import BeautifulSoup
from tatorterp import Episode

logger = logging.getLogger("tatorter")
logging.basicConfig()

WIKI_URL = "https://de.wikipedia.org/wiki/Liste_der_Tatort-Folgen"
HEADERS = {"User-Agent": "tatorter/0.1 (Tatort episode renamer)"}

# Maps detective team names to their home city. Crossover episodes (team string
# contains "/") are handled dynamically by lookup_location() -- no compound
# entries needed here.
team_to_location = {
    # Current active teams
    "Ballauf und Schenk":                                  "Köln",
    "Batic und Leitmayr":                                  "München",
    "Batu":                                                "Hamburg",
    "Berlinger und Rascher":                               "Freiburg",
    "Berlinger":                                           "Freiburg",
    "Blum und Perlmann":                                   "Konstanz",
    "Blum und Perlmann, Matteo Lüthi":                     "Konstanz",
    "Borowski und Brandt":                                 "Kiel",
    "Borowski und Sahin":                                  "Kiel",
    "Borowski":                                            "Kiel",
    "Eisner und Fellner":                                  "Wien",
    "Eisner":                                              "Wien",
    "Faber und Bönisch":                                   "Dortmund",
    "Faber, Bönisch und Dalay":                            "Dortmund",
    "Faber, Bönisch, Dalay und Kossik":                    "Dortmund",
    "Faber, Bönisch, Dalay und Pawlak":                    "Dortmund",
    "Faber, Bönisch, Pawlak und Herzog":                   "Dortmund",
    "Faber, Pawlak und Herzog":                            "Dortmund",
    "Falke und Grosz":                                     "Hamburg",
    "Falke und Lorenz":                                    "Hamburg",
    "Flückiger und Lanning":                               "Luzern",
    "Flückiger und Ritschard":                             "Luzern",
    "Funck, Schaffert und Grewel":                         "Erfurt",
    "Gorniak, Winkler und Schnabel":                       "Dresden",
    "Grandjean und Ott":                                   "Zürich",
    "Janneke und Brix":                                    "Frankfurt",
    "Kappl und Deininger":                                 "Saarbrücken",
    "Karow":                                               "Berlin",
    "Lannert und Bootz":                                   "Stuttgart",
    "Lessing und Dorn":                                    "Weimar",
    "Lindholm und Schmitz":                                "Hannover",
    "Lindholm":                                            "Hannover",
    "Lürsen und Stedefreund":                              "Bremen",
    "Moormann und Selb":                                   "Bremen",
    "Moormann, Andersen und Selb":                         "Bremen",
    "Murot und Wächter":                                   "Wiesbaden",
    "Murot":                                               "Wiesbaden",
    "Odenthal und Kopper":                                 "Ludwigshafen",
    "Odenthal und Stern":                                  "Ludwigshafen",
    "Ritter und Stark":                                    "Berlin",
    "Rubin und Karow":                                     "Berlin",
    "Saalfeld und Keppler":                                "Leipzig",
    "Schimanski und Thanner":                              "Duisburg",
    "Schürk und Hölzer":                                   "Saarbrücken",
    "Schürk und Hölzer, Baumann und Heinrich":             "Saarbrücken",
    "Sieland, Gorniak und Schnabel":                       "Dresden",
    "Sieland, Gorniak, Mohr und Schnabel":                 "Dresden",
    "Stark":                                               "Berlin",
    "Steier und Mey":                                      "Frankfurt",
    "Steier":                                              "Frankfurt",
    "Stellbrink und Marx":                                 "Saarbrücken",
    "Thiel und Boerne":                                    "Münster",
    "Tobler und Berg":                                     "Freiburg",
    "Tschiller und Gümer":                                 "Hamburg",
    "Voss und Ringelhahn":                                 "Franken",
    "Voss, Ringelhahn, Goldwasser, Fleischer und Schatz":  "Franken",

    # NDR = Hamburg
    "Beck":                          "Hamburg",
    "Brammer":                       "Hamburg",
    "Casstorff und Holicek":         "Hamburg",
    "Delius":                        "Hamburg",
    "Delius a. D.":                  "Hamburg",
    "Falke":                         "Hamburg",
    "Falke und Schmitt":             "Hamburg",
    "Finke":                         "Hamburg",
    "Greve":                         "Hamburg",
    "Nagel":                         "Hamburg",
    "Piper":                         "Hamburg",
    "Ronke":                         "Hamburg",
    "Schnoor":                       "Hamburg",
    "Sommer":                        "Hamburg",
    "Stoever":                       "Hamburg",
    "Stoever und Brockmöller":       "Hamburg",
    "Trimmel":                       "Hamburg",
    "Borowski und Jung":             "Kiel",

    # BR = München
    "Brandenburg":                   "München",
    "Lenz":                          "München",
    "Riedmüller":                    "München",
    "Scherrer":                      "München",
    "Veigl":                         "München",
    "Voss":                          "Franken",

    # SWR/SDR = Stuttgart / Konstanz / Freiburg
    "Bienzle":                       "Stuttgart",
    "Bienzle und Gächter":           "Stuttgart",
    "Lutz":                          "Stuttgart",
    "Lutz und Schreitle":            "Stuttgart",
    "Schreitle":                     "Stuttgart",
    "Blum":                          "Konstanz",
    "Blum, Perlmann und Flückiger":  "Konstanz",
    "Blum, Perlmann und Lüthi":      "Konstanz",
    "Tobler":                        "Freiburg",

    # WDR = Köln / Duisburg / Dortmund
    "Enders und Kreutzer":           "Duisburg",
    "Faber und Herzog":              "Dortmund",
    "Flemming und Koch":             "Köln",
    "Flemming, Koch und Ballauf":    "Köln",
    "Haferkamp und Kreutzer":        "Duisburg",
    "Kressin":                       "Köln",
    "Kreutzer":                      "Duisburg",

    # MDR = Leipzig / Dresden
    "Ehrlicher und Kain":            "Leipzig",
    "Winkler und Schnabel":          "Dresden",

    # HR = Frankfurt / Wiesbaden
    "Azadi und Kulina":              "Frankfurt",
    "Bergmann":                      "Frankfurt",
    "Brinkmann":                     "Frankfurt",
    "Dellwo":                        "Frankfurt",
    "Dellwo und Sänger":             "Frankfurt",
    "Dietze":                        "Frankfurt",
    "Felber":                        "Frankfurt",
    "Konrad":                        "Frankfurt",
    "Rolfs":                         "Frankfurt",
    "Rullmann":                      "Frankfurt",
    "Sander":                        "Frankfurt",
    "Sänger":                        "Frankfurt",

    # SR = Saarbrücken
    "Liersdahl und Schäfermann":     "Saarbrücken",
    "Palu":                          "Saarbrücken",
    "Schäfermann":                   "Saarbrücken",
    "Schürk, Hölzer, Baumann und Heinrich": "Saarbrücken",

    # SFB/RBB = Berlin
    "Behnke":                        "Berlin",
    "Bülow":                         "Berlin",
    "Hellmann und Ritter":           "Berlin",
    "Kasulke":                       "Berlin",
    "Karow und Bonard":              "Berlin",
    "Markowitz":                     "Berlin",
    "Roiter und Zorowski":           "Berlin",
    "Schmidt":                       "Berlin",
    "Walther":                       "Berlin",

    # ORF = Wien
    "Becker":                        "Wien",
    "Fichtl":                        "Wien",
    "Hirth":                         "Wien",
    "Kant und Varanasi":             "Wien",
    "Marek":                         "Wien",
    "Marek a. D.":                   "Wien",
    "Pfeifer":                       "Wien",

    # SF/SRF = Zürich
    "Carlucci":                      "Zürich",
    "Carlucci und Gertsch":          "Zürich",
    "Howald":                        "Zürich",
    "von Burg und Gertsch":          "Zürich",

    # Radio Bremen = Bremen
    "Böck":                          "Bremen",
    "Lürsen":                        "Bremen",

    # SWF = Ludwigshafen
    "Buchmüller":                    "Ludwigshafen",
    "Gerber":                        "Ludwigshafen",
    "Odenthal":                      "Ludwigshafen",
    "Odenthal, Kopper und Stern":    "Ludwigshafen",
    "Pflüger":                       "Ludwigshafen",
    "Wiegand":                       "Ludwigshafen",
}


def lookup_location(team):
    """Return city for a detective team, deriving compound cities on the fly.

    For crossover episodes where the team string contains "/" (e.g.
    "Ballauf und Schenk / Saalfeld und Keppler"), each part is looked up
    independently and the results joined with "-".
    """
    if team in team_to_location:
        return team_to_location[team]
    if "/" in team:
        parts = [p.strip() for p in team.split("/", 1)]
        locs = [team_to_location.get(p, "") for p in parts]
        locs = [l for l in locs if l]
        if len(locs) == 2 and locs[0] != locs[1]:
            return "{}-{}".format(locs[0], locs[1])
        if locs:
            return locs[0]
    return None


class WikipediaDEGrabber(object):
    def __init__(self):
        try:
            resp = requests.get(WIKI_URL, headers=HEADERS, timeout=30)
            resp.raise_for_status()
        except requests.RequestException as e:
            raise RuntimeError("Could not fetch episode list from Wikipedia: {}".format(e))

        soup = BeautifulSoup(resp.text, "html.parser")

        # Find the episode table by looking for a wikitable whose header row
        # contains "Folge". This is more robust than asserting exactly N tables.
        tables = soup.find_all("table", class_=lambda c: c and "wikitable" in c)
        episode_table = None
        for t in tables:
            headers = [th.get_text(strip=True) for th in t.find_all("th")]
            if any("Folge" in h for h in headers):
                episode_table = t
                break
        if episode_table is None:
            raise RuntimeError("Could not find episode table on Wikipedia page.")

        trs = episode_table.find_all("tr")
        logger.info("Parsing {} episode rows from {}.".format(len(trs), WIKI_URL))

        self.episodes = []
        season = 1969
        first_episode = 1

        for tr in trs[1:]:
            tds = tr.find_all("td")
            if len(tds) < 8:
                continue  # header rows, colspan rows, future extra columns

            raw = [td.get_text(strip=True) for td in tds]

            try:
                episode_index = int(re.sub(r"[^\d]", "", raw[0]))
            except (ValueError, IndexError):
                continue
            if episode_index <= 0:
                continue

            title       = raw[1]
            broadcaster = raw[2]
            # Strip footnote references like [1] from the premiere date.
            premiere    = raw[3].split("[")[0].strip()
            # Strip "(Gastauftritt ...)" annotations only from the team column.
            team        = raw[4].split("(")[0].strip()
            case_index  = raw[5]
            author      = raw[6]
            director    = raw[7]

            try:
                year = int(premiere[-4:])
            except (ValueError, IndexError):
                continue

            if year > season:
                season = year
                first_episode = episode_index

            location = lookup_location(team)
            if location is None:
                logger.warning("Location for team '{}' unknown. Script should be updated!".format(team))
                location = "[{}]".format(team)

            episode = Episode(
                episode_index=episode_index,
                location=location,
                title=title,
                broadcaster=broadcaster,
                premiere=premiere,
                team=team,
                case_index=case_index,
                author=author,
                director=director,
                episode=episode_index - first_episode + 1,
                season=season,
            )
            self.episodes.append(episode)


# Keep the old name as an alias for backward compatibility with any cached imports.
WikipdediaDEGrabber = WikipediaDEGrabber
