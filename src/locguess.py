#!/usr/bin/python

import ConfigParser
import sys
import codecs
import re
import sqlite3 as lite
from sqlite3 import IntegrityError

config = ConfigParser.ConfigParser()
config.read("config.ini")
dbpath = config.get("main", "dbpath")

# wheee global db variables (traditional)
con = lite.connect(dbpath)
con.text_factory = str
cur = con.cursor()

def guessFromStringWithMapping(string, mapping):
    # re.search('test', 'TeSt', re.IGNORECASE)
    for m in mapping:
        if re.search(m['r'], string):
            return m['l']
    return None

def guessLocation(title, location):
    # use map of regex->location_string to guess?
    mapping = [
        {'r': re.compile("Kitsilano", re.IGNORECASE), 'l': "Kitsilano"},
        {'r': re.compile("yaletown", re.IGNORECASE), 'l': "Yaletown"},
        {'r': re.compile("smithe st", re.IGNORECASE), 'l': "Yaletown"},
        {'r': re.compile("coal harbour", re.IGNORECASE), 'l': "Coal Harbour"},
        {'r': re.compile("coal harbor", re.IGNORECASE), 'l': "Coal Harbour"},
        {'r': re.compile("false creek", re.IGNORECASE), 'l': "False Creek"},
        {'r': re.compile("olympic vil", re.IGNORECASE), 'l': "False Creek"},
        {'r': re.compile("point grey", re.IGNORECASE), 'l': "Point Grey"},
        {'r': re.compile("west end", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("westend", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("jervis", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("Broughton", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("Davie", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("west van", re.IGNORECASE), 'l': "West Vancouver"},
        {'r': re.compile("Dundarave", re.IGNORECASE), 'l': "West Vancouver"},
        {'r': re.compile("Ambleside", re.IGNORECASE), 'l': "West Vancouver"},
        {'r': re.compile("gastown", re.IGNORECASE), 'l': "Gastown"},
        {'r': re.compile("woodwards", re.IGNORECASE), 'l': "Gastown"},
        {'r': re.compile("lion.*bay", re.IGNORECASE), 'l': "West Vancouver"},
        {'r': re.compile("east van", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("Commercial Drive", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("east\s\w+street", re.IGNORECASE), 'l': "East Vancouver"}, # not sure about this one
        {'r': re.compile("Van.East", re.IGNORECASE), 'l': "East Vancouver"}, # not sure about this one
        {'r': re.compile("south van", re.IGNORECASE), 'l': "South Vancouver"},
        {'r': re.compile("south granville", re.IGNORECASE), 'l': "South Vancouver"},
        #{'r': re.compile("\d+th and \w+", re.IGNORECASE), 'l': "South Vancouver"}, # or this one 
        {'r': re.compile("marpole", re.IGNORECASE), 'l': "South Vancouver"},
        {'r': re.compile("south.*oak.*street", re.IGNORECASE), 'l': "South Vancouver"},
        {'r': re.compile("richmond", re.IGNORECASE), 'l': "Richmond"},
        {'r': re.compile("steveston", re.IGNORECASE), 'l': "Richmond"},
        {'r': re.compile("brighouse", re.IGNORECASE), 'l': "Richmond"},
        {'r': re.compile("Bridgeport", re.IGNORECASE), 'l': "Richmond"},
        {'r': re.compile("south.*cambie", re.IGNORECASE), 'l': "South Vancouver"},
        {'r': re.compile("cambie", re.IGNORECASE), 'l': "Cambie"},
        {'r': re.compile("north vancouver", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("canyon height", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("Capilano", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("lonsdale", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("joyce.*skytrain", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("collingwood", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("joyce st", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("westside", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("west side", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("vancouver west", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("SHAUGHNESSY", re.IGNORECASE), 'l': "Shaughnessy"},
        {'r': re.compile("Arbutus", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("trafalgar", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("kerisdale", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("kerrisdale", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("dunbar", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("danbar", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("Marinaside Cr", re.IGNORECASE), 'l': "Yaletown"},
        {'r': re.compile("new west", re.IGNORECASE), 'l': "New Westminster"},
        {'r': re.compile("sapperton", re.IGNORECASE), 'l': "New Westminster"},
        {'r': re.compile("delta", re.IGNORECASE), 'l': "Delta"},
        {'r': re.compile("surrey", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("fleetwood", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("newton", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("bridgeview", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("panorama ridge", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("King George", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("white rock", re.IGNORECASE), 'l': "White Rock"},
        {'r': re.compile("burnaby", re.IGNORECASE), 'l': "Burnaby"},
        {'r': re.compile("cloverdale", re.IGNORECASE), 'l': "Cloverdale"},
        {'r': re.compile("maple ridge", re.IGNORECASE), 'l': "Maple Ridge"},
        {'r': re.compile("Abbotsford", re.IGNORECASE), 'l': "Abbotsford"},
        {'r': re.compile("Port Coquitlam", re.IGNORECASE), 'l': "Port Coquitlam"},
        {'r': re.compile("Coquitlam", re.IGNORECASE), 'l': "Coquitlam"},
        {'r': re.compile("Burke m", re.IGNORECASE), 'l': "Coquitlam"},
        {'r': re.compile("Coq", re.IGNORECASE), 'l': "Coquitlam"},
        {'r': re.compile("downtown", re.IGNORECASE), 'l': "Downtown"},
        {'r': re.compile("dt van", re.IGNORECASE), 'l': "Downtown"},
        {'r': re.compile("howe st", re.IGNORECASE), 'l': "Downtown"},
        {'r': re.compile("ubc", re.IGNORECASE), 'l': "UBC"},
        {'r': re.compile("squamish", re.IGNORECASE), 'l': "Squamish"},
        {'r': re.compile("Tsawwassen", re.IGNORECASE), 'l': "Tsawwassen"},
        {'r': re.compile("Port Moody", re.IGNORECASE), 'l': "Port Moody"},
        {'r': re.compile("portmoody", re.IGNORECASE), 'l': "Port Moody"},
        {'r': re.compile("langley", re.IGNORECASE), 'l': "Langley"},
        {'r': re.compile("ladner", re.IGNORECASE), 'l': "Ladner"},
        {'r': re.compile("Mission", re.IGNORECASE), 'l': "Mission"},
        {'r': re.compile("Pitt Meadows", re.IGNORECASE), 'l': "Pitt Meadows"},
        {'r': re.compile("Aldergrove", re.IGNORECASE), 'l': "Aldergrove"},

        {'r': re.compile("chinatown", re.IGNORECASE), 'l': "Chinatown"},
        {'r': re.compile("crosstown", re.IGNORECASE), 'l': "Crosstown"},

        {'r': re.compile("english bay", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("haro ", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("robson", re.IGNORECASE), 'l': "Downtown"},
        {'r': re.compile("hornby", re.IGNORECASE), 'l': "Downtown"},
        {'r': re.compile("hamilton", re.IGNORECASE), 'l': "Yaletown"},
        {'r': re.compile("richards", re.IGNORECASE), 'l': "Yaletown"},
        {'r': re.compile("homer st", re.IGNORECASE), 'l': "Yaletown"},
        {'r': re.compile("mt\. seymour", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("mount seymour", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("seymour", re.IGNORECASE), 'l': "Yaletown"},
        {'r': re.compile("maple", re.IGNORECASE), 'l': "Vancouver West Side"},
        {'r': re.compile("vgh", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("city hall", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("Killarney", re.IGNORECASE), 'l': "South Vancouver"},
        {'r': re.compile("Kilarney", re.IGNORECASE), 'l': "South Vancouver"},
        {'r': re.compile("mount pleasant", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("mt\. pleasant", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("Mt Pleasant", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("fir", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("hastings.*sunrise", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("Lynn Valley", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("Pemberton", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("Edgemont", re.IGNORECASE), 'l': "North Vancouver"},
        {'r': re.compile("oakridge", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("hastings", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("fraser", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("renfrew", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("earles", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("Kensingston", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("cedar cottage", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("harwood", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("Alberni", re.IGNORECASE), 'l': "Downtown"},
        {'r': re.compile("Melville st", re.IGNORECASE), 'l': "Downtown"},

        {'r': re.compile("denman", re.IGNORECASE), 'l': "West End"},
        {'r': re.compile("stanley park", re.IGNORECASE), 'l': "West End"},

        {'r': re.compile("scott", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("Guildford", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("chimney heights", re.IGNORECASE), 'l': "Surrey"},
        {'r': re.compile("Metropolis", re.IGNORECASE), 'l': "Burnaby"},
        {'r': re.compile("Lougheed", re.IGNORECASE), 'l': "Burnaby"},
        {'r': re.compile("Brentwood", re.IGNORECASE), 'l': "Burnaby"},
        {'r': re.compile("Metrotown", re.IGNORECASE), 'l': "Burnaby"},
        {'r': re.compile("cariboo hill", re.IGNORECASE), 'l': "Burnaby"},
        {'r': re.compile("riverwood", re.IGNORECASE), 'l': "Port Coquitlam"},
        {'r': re.compile("chester", re.IGNORECASE), 'l': "Port Coquitlam"},
        {'r': re.compile("rosamond", re.IGNORECASE), 'l': "Richmond"},
        {'r': re.compile("Richmomd", re.IGNORECASE), 'l': "Richmond"},
        {'r': re.compile("lansdowne", re.IGNORECASE), 'l': "Richmond"},

        {'r': re.compile("kits", re.IGNORECASE), 'l': "Kitsilano"},
        {'r': re.compile("bby", re.IGNORECASE), 'l': "Burnaby"},
        {'r': re.compile("King Ed", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("main and", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("quebec", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("Granville St", re.IGNORECASE), 'l': "South Vancouver"},
        {'r': re.compile("commercial", re.IGNORECASE), 'l': "East Vancouver"},
        {'r': re.compile("vancouver", re.IGNORECASE), 'l': "Vancouver"},
        {'r': re.compile("beach ave", re.IGNORECASE), 'l': "West End"},
    ]
    return guessFromStringWithMapping(title + " " + location, mapping)


def guessBedrooms(title):
    mapping = {}
    return guessFromStringWithMapping(title, mapping)

def guessSquarefoot(title):
    mapping = {}
    return guessFromStringWithMapping(title, mapping)


def store_guess_loc(con, aid, guessloc):
    cur = con.cursor()
    cur.execute('update ad set loc1=? where id=?', (guessloc, aid))

def process_ads(con):
    cur = con.cursor()
    cur.execute('select a.id,a.title,a.loctext from ad as a order by a.id;');
    
    rows = cur.fetchall()
    for ad in rows:
        aid = ad[0]
        atitle = ad[1]
        aloc = ad[2]
        guessloc = guessLocation(atitle, aloc)

        if guessloc:
            store_guess_loc(con, aid, guessloc)


process_ads(con)

con.commit()
con.close()
