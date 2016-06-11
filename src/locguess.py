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
        if re.search(m['r'], string, re.IGNORECASE):
            return m['l']
    return ""

def guessLocation(title, location):
    # use map of regex->location_string to guess?
    mapping = [
        {'r': "Kitsilano", 'l': "Kitsilano"},
        {'r': "yaletown", 'l': "Yaletown"},
        {'r': "smithe st", 'l': "Yaletown"},
        {'r': "coal harbour", 'l': "Coal Harbour"},
        {'r': "coal harbor", 'l': "Coal Harbour"},
        {'r': "false creek", 'l': "False Creek"},
        {'r': "olympic vil", 'l': "False Creek"},
        {'r': "point grey", 'l': "Point Grey"},
        {'r': "west end", 'l': "West End"},
        {'r': "westend", 'l': "West End"},
        {'r': "jervis", 'l': "West End"},
        {'r': "Broughton", 'l': "West End"},
        {'r': "Davie", 'l': "West End"},
        {'r': "west van", 'l': "West Vancouver"},
        {'r': "Dundarave", 'l': "West Vancouver"},
        {'r': "Ambleside", 'l': "West Vancouver"},
        {'r': "gastown", 'l': "Gastown"},
        {'r': "woodwards", 'l': "Gastown"},
        {'r': "lion.*bay", 'l': "West Vancouver"},
        {'r': "east van", 'l': "East Vancouver"},
        {'r': "Commercial Drive", 'l': "East Vancouver"},
        {'r': "east\s\w+street", 'l': "East Vancouver"}, # not sure about this one
        {'r': "Van.East", 'l': "East Vancouver"}, # not sure about this one
        {'r': "south van", 'l': "South Vancouver"},
        {'r': "south granville", 'l': "South Vancouver"},
        #{'r': "\d+th and \w+", 'l': "South Vancouver"}, # or this one 
        {'r': "marpole", 'l': "South Vancouver"},
        {'r': "south.*oak.*street", 'l': "South Vancouver"},
        {'r': "richmond", 'l': "Richmond"},
        {'r': "steveston", 'l': "Richmond"},
        {'r': "brighouse", 'l': "Richmond"},
        {'r': "Bridgeport", 'l': "Richmond"},
        {'r': "south.*cambie", 'l': "South Vancouver"},
        {'r': "cambie", 'l': "Cambie"},
        {'r': "north vancouver", 'l': "North Vancouver"},
        {'r': "canyon height", 'l': "North Vancouver"},
        {'r': "Capilano", 'l': "North Vancouver"},
        {'r': "lonsdale", 'l': "North Vancouver"},
        {'r': "joyce.*skytrain", 'l': "East Vancouver"},
        {'r': "collingwood", 'l': "East Vancouver"},
        {'r': "joyce st", 'l': "East Vancouver"},
        {'r': "westside", 'l': "Vancouver West Side"},
        {'r': "west side", 'l': "Vancouver West Side"},
        {'r': "vancouver west", 'l': "Vancouver West Side"},
        {'r': "SHAUGHNESSY", 'l': "Shaughnessy"},
        {'r': "Arbutus", 'l': "Vancouver West Side"},
        {'r': "trafalgar", 'l': "Vancouver West Side"},
        {'r': "kerisdale", 'l': "Vancouver West Side"},
        {'r': "kerrisdale", 'l': "Vancouver West Side"},
        {'r': "dunbar", 'l': "Vancouver West Side"},
        {'r': "danbar", 'l': "Vancouver West Side"},
        {'r': "Marinaside Cr", 'l': "Yaletown"},
        {'r': "new west", 'l': "New Westminster"},
        {'r': "sapperton", 'l': "New Westminster"},
        {'r': "delta", 'l': "Delta"},
        {'r': "surrey", 'l': "Surrey"},
        {'r': "fleetwood", 'l': "Surrey"},
        {'r': "newton", 'l': "Surrey"},
        {'r': "bridgeview", 'l': "Surrey"},
        {'r': "panorama ridge", 'l': "Surrey"},
        {'r': "King George", 'l': "Surrey"},
        {'r': "white rock", 'l': "White Rock"},
        {'r': "burnaby", 'l': "Burnaby"},
        {'r': "cloverdale", 'l': "Cloverdale"},
        {'r': "maple ridge", 'l': "Maple Ridge"},
        {'r': "Abbotsford", 'l': "Abbotsford"},
        {'r': "Port Coquitlam", 'l': "Port Coquitlam"},
        {'r': "Coquitlam", 'l': "Coquitlam"},
        {'r': "Burke m", 'l': "Coquitlam"},
        {'r': "Coq", 'l': "Coquitlam"},
        {'r': "downtown", 'l': "Downtown"},
        {'r': "dt van", 'l': "Downtown"},
        {'r': "howe st", 'l': "Downtown"},
        {'r': "ubc", 'l': "UBC"},
        {'r': "squamish", 'l': "Squamish"},
        {'r': "Tsawwassen", 'l': "Tsawwassen"},
        {'r': "Port Moody", 'l': "Port Moody"},
        {'r': "portmoody", 'l': "Port Moody"},
        {'r': "langley", 'l': "Langley"},
        {'r': "ladner", 'l': "Ladner"},
        {'r': "Mission", 'l': "Mission"},
        {'r': "Pitt Meadows", 'l': "Pitt Meadows"},
        {'r': "Aldergrove", 'l': "Aldergrove"},

        {'r': "chinatown", 'l': "Chinatown"},
        {'r': "crosstown", 'l': "Crosstown"},

        {'r': "english bay", 'l': "West End"},
        {'r': "haro ", 'l': "West End"},
        {'r': "robson", 'l': "Downtown"},
        {'r': "hornby", 'l': "Downtown"},
        {'r': "hamilton", 'l': "Yaletown"},
        {'r': "richards", 'l': "Yaletown"},
        {'r': "homer st", 'l': "Yaletown"},
        {'r': "mt\. seymour", 'l': "North Vancouver"},
        {'r': "mount seymour", 'l': "North Vancouver"},
        {'r': "seymour", 'l': "Yaletown"},
        {'r': "maple", 'l': "Vancouver West Side"},
        {'r': "vgh", 'l': "Vancouver"},
        {'r': "city hall", 'l': "Vancouver"},
        {'r': "Killarney", 'l': "South Vancouver"},
        {'r': "Kilarney", 'l': "South Vancouver"},
        {'r': "mount pleasant", 'l': "Vancouver"},
        {'r': "mt\. pleasant", 'l': "Vancouver"},
        {'r': "Mt Pleasant", 'l': "Vancouver"},
        {'r': "fir", 'l': "Vancouver"},
        {'r': "hastings.*sunrise", 'l': "East Vancouver"},
        {'r': "Lynn Valley", 'l': "North Vancouver"},
        {'r': "Pemberton", 'l': "North Vancouver"},
        {'r': "Edgemont", 'l': "North Vancouver"},
        {'r': "oakridge", 'l': "Vancouver"},
        {'r': "hastings", 'l': "Vancouver"},
        {'r': "fraser", 'l': "East Vancouver"},
        {'r': "renfrew", 'l': "East Vancouver"},
        {'r': "earles", 'l': "East Vancouver"},
        {'r': "Kensingston", 'l': "East Vancouver"},
        {'r': "cedar cottage", 'l': "East Vancouver"},
        {'r': "harwood", 'l': "West End"},
        {'r': "Alberni", 'l': "Downtown"},
        {'r': "Melville st", 'l': "Downtown"},

        {'r': "denman", 'l': "West End"},
        {'r': "stanley park", 'l': "West End"},

        {'r': "scott", 'l': "Surrey"},
        {'r': "Guildford", 'l': "Surrey"},
        {'r': "chimney heights", 'l': "Surrey"},
        {'r': "Metropolis", 'l': "Burnaby"},
        {'r': "Lougheed", 'l': "Burnaby"},
        {'r': "Brentwood", 'l': "Burnaby"},
        {'r': "Metrotown", 'l': "Burnaby"},
        {'r': "cariboo hill", 'l': "Burnaby"},
        {'r': "riverwood", 'l': "Port Coquitlam"},
        {'r': "chester", 'l': "Port Coquitlam"},
        {'r': "rosamond", 'l': "Richmond"},
        {'r': "Richmomd", 'l': "Richmond"},
        {'r': "lansdowne", 'l': "Richmond"},

        {'r': "kits", 'l': "Kitsilano"},
        {'r': "bby", 'l': "Burnaby"},
        {'r': "King Ed", 'l': "Vancouver"},
        {'r': "main and", 'l': "Vancouver"},
        {'r': "quebec", 'l': "Vancouver"},
        {'r': "Granville St", 'l': "South Vancouver"},
        {'r': "commercial", 'l': "East Vancouver"},
        {'r': "vancouver", 'l': "Vancouver"},
        {'r': "beach ave", 'l': "West End"},
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
