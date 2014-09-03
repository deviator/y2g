#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import argparse
import os.path
from urllib.parse import *

def main():

    args = parseArguments()
    processor = TableProcessor()

    with open( args.filename ) as f:
        reader = csv.reader( f, delimiter=args.delimiter,
                                quotechar=args.quotechar )

        skip = SkipFirst( args.skipfirst )

        for row in reader: 
            if skip(): continue

            processor.parseRow( row )

    filename = os.path.splitext( args.filename )[0]

    with open( filename + "_tbl1.csv", 'w', newline='' ) as f:
        writer = csv_writer(f,args)

        for row in processor.getKWordsWithMWords():
            writer.writerow( row )

    with open( filename + "_tbl2.csv", 'w', newline='' ) as f:
        writer = csv_writer(f,args)

        for row in processor.getKWordsWithAdv():
            writer.writerow( row )

def parseArguments():
    ap = argparse.ArgumentParser()
    ap.add_argument( "filename", help="input file name" )
    ap.add_argument( "-s", "--skipfirst", dest="skipfirst", metavar="N", default=10, help="skip first N lines" )
    ap.add_argument( "-d", "--delimiter", dest="delimiter", metavar="CHAR", default=',', help="csv delimiter" )
    ap.add_argument( "-q", "--quotechar", dest="quotechar", metavar="CHAR", default='"', help="csv quotechar" )
    return ap.parse_args()

class SkipFirst:
    def __init__(self,count):
        self.rownum = 0
        self.count = count

    def __call__(self):
        r = self.rownum < self.count
        self.rownum += 1
        return r

def csv_writer(f,args):
    return csv.writer( f, delimiter=args.delimiter,
                          quotechar=args.quotechar,
                          quoting=csv.QUOTE_MINIMAL )

class Adv:
    def __init__(self, keywords):
        self.keywords = keywords
        self.minuswords = {}
        self.advtext = []

    def appendMinuswords(self, mwords):
        for mw in mwords:
            if mw not in self.minuswords:
                self.minuswords[mw] = 0
            self.minuswords[mw] += 1

    def appendAdv(self, title, text, link):
        self.advtext.append( [title,text,link] )

class TableProcessor:

    def __init__(self):
        self.phraseIndex = 2 # phrase column number in table
        self.titleIndex = 4  # title --//--
        self.textIndex = 5   # text
        self.linkIndex = 8   # link
        self.maxTitleLen = 30
        self.maxTextLen = 38
        self.linkBadQuery = "utm"
        self.data = {}

    def parseRow(self, row):
        (keywords, minuswords) = self.parseKeywords(row[self.phraseIndex])
        title = row[self.titleIndex]
        text = row[self.textIndex]
        link = row[self.linkIndex]

        if keywords not in self.data:
            self.data[keywords] = Adv(keywords)

        self.data[keywords].appendMinuswords( minuswords )
        self.data[keywords].appendAdv( title, text, link )

    # for table 1
    def getKWordsWithMWords(self):
        for (kw, adv) in self.data.items():
            for (mw,cnt) in adv.minuswords.items():
                yield [ kw, mw ]

    # for table 2
    def getKWordsWithAdv(self):
        for (kw, adv) in self.data.items():
            for tt in adv.advtext:
                yield [ kw ] + self.titleOutput(tt[0]) +\
                               self.textOutput(tt[1]) +\
                               self.linkOutput(tt[2])

    def parseKeywords(self, keywords):
        words = keywords.split()
        kw = []
        mw = []

        for word in words:
            if word[0] == '+':
                kw.append( '!' + word[1:] )
            elif word[0] == '-':
                mw.append( word[1:] )
            else:
                kw.append( word )

        return ( str.join(" ", kw), mw )

    def titleOutput(self, title):
        error = ""
        if( len(title) > self.maxTitleLen ):
            error = "title length > %s"%self.maxTitleLen
        return [title, error]

    def textOutput(self, text):
        spl = text.split()
        text1 = ""
        while( len(text1) + len(spl[0]) < self.maxTextLen ):
            text1 += " " + spl[0]
            spl = spl[1:]

        text2 = " ".join(spl)
        error = ""
        if( len(text2) > self.maxTextLen ):
            error = "text2 length > %s"%self.maxTextLen

        return [text1, text2, error]
        
    def linkOutput(self, link):
        up = urlparse(link)
        query = []
        for q in up.query.split('&'):
            if not q.startswith( self.linkBadQuery ):
                query.append( q )
        result = up.path
        if len(query):
            result += "?" + "&".join(query)
        return [ result ]

if __name__ == '__main__': main()
