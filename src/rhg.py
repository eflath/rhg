#!/usr/bin/env python

import os
import sys
import random
import csv
import pprint
import string

import cgitb
cgitb.enable()

##Pretty print
##syntax: pp.pprint(stuff)

pp = pprint.PrettyPrinter(indent=4)


def assemble_csv(*csvFile):
    """returns a combined list of the specified csv's"""

    csvList = []

    for each in csvFile:
        csvReader = csv.DictReader(open(each, "rb"))
        for each in csvReader:
            csvList.append(each)

    return csvList


def randomSelection(list):
    """select a random element in a list"""
    
    return random.choice(list)
    
def randomWord(*file):
    """returns a random word dict"""
    
    return randomSelection(assemble_csv(*file))

def nounToPronoun(gender):
    
    pronounList = assemble_csv("rhg_pronouns.csv")

    for each in pronounList:
        if each["gender"] == gender:
            return each
    
class Word(object):
    
    """This is the word class"""
    
    def __init__(self):
        print "initializing"

class Verb(Word):
    """This is the verb class"""

    def __init__(self, name):
        self.name = name

    @property
    def infinitive(self):
        return self.name["infinitive"]

    @property
    def present(self):
        return self.name["present"]

    @property
    def presentparticiple(self):
        return self.name["present participle"]

    @property
    def past(self):
        return self.name["past"]

class Noun(Word):
    
    """This is the noun class"""
    
    def __init__(self,name):
        self.name = name

    @property
    def singular(self):
        return self.name["singular"]

    @property
    def plural(self):
        return self.name["plural"]

    @property
    def gender(self):
        return self.name["gender"]

    @property
    def article(self):
        if self.name["article"]:
            return self.name["article"]
        else:
            return None

    @property
    def prepositions(self):
        if self.name["prepositions"]:
            prepositionList = self.name["prepositions"].split(",")
            return prepositionList
        else:
            None

    @property
    def quantifier(self):
        if self.name["quantifier"]:
            quantifierList = self.name["quantifier"].split(",")
            return quantifierList
        else:
            None

class Adjective(Word):

    """This is the adjective class"""

    def __init__(self, name):
        self.name = name

    @property
    def positive(self):
        return self.name["positive"]

    @property
    def comparitive(self):
        return self.name["comparitive"]

    @property
    def superlative(self):
        return self.name["superlative"]


class Pronoun(object):
    """This is the pronoun class"""

    def __init__(self, name):
        self.name = name

    @property
    def gender(self):
        return self.name["gender"]

    @property
    def object(self):
        return self.name["object"]

    @property
    def subject(self):
        return self.name["subject"]

    @property
    def possessive(self):
        return self.name["possessive"]

    @property
    def reflexive(self):
        return self.name["reflexive"]


class Headline(object):
    
    """This is the headline class"""
    
    def __init__(self,*args,**kwargs):
        
        if kwargs["type"] == "basic":
            
            hSubject = Noun(randomWord("rhg_nAnimate.csv"))
            hAction = Verb(randomWord("rhg_verbs.csv"))
            hObject = Noun(randomWord("rhg_nInanimate.csv"))
            hObjectArticleQuantifier = ""
            hObjectReply = ""
            
    
            if hObject.article == None:
                hObjectReply = hObject.plural
                hObjectArticleQuantifier =  random.choice(hObject.quantifier)
            else:
                hObjectReply = hObject.singular
                hObjectArticleQuantifier =  hObject.article
                
            
            mainHeadline = (hSubject.singular + " " + hAction.present + " " + hObject.singular)
            
            print("\n")
            
            print("----Today's News----")
            
            print("\n")
            
            print(string.capwords(mainHeadline))
            
            print("\n")
            
            print(hSubject.singular + " replied, " + "\"I " + hAction.past + " " + hObjectArticleQuantifier +
                  " " + hObjectReply + ". Who Cares?\"")
            
            print("\n")    
        
        
class Obituary(object):
    
    """This is the obituary class"""
    
    def __init__(self):
        
        #obituary headline
        
        oSubject = Noun(randomWord("rhg_nAnimate.csv"))
        oVerb = Verb(randomWord("rhg_verbs.csv"))
        oObject = Noun(randomWord("rhg_nInanimate.csv"))
        oObjectArticleQuantifier = ""
        oObjectState = ""
        
        if oObject.article == None:
            oObjectState = oObject.plural
            oObjectArticleQuantifier =  random.choice(oObject.quantifier)
        else:
            oObjectState = oObject.singular
            oObjectArticleQuantifier =  oObject.article
        
        obituaryText = oSubject.singular + " dies while " + oVerb.presentparticiple + " " + oObjectArticleQuantifier + " " + oObjectState
        
        #remembering the deceased
        
        oSubjectFriend = Noun(randomWord("rhg_nAnimate.csv"))
        oPlace = Noun(randomWord("rhg_nPlaces.csv"))
        oPronoun = Pronoun(nounToPronoun(oSubject.gender))
        oPlacePrep = random.choice(oPlace.prepositions)
        oPlaceArticle = ""
        oSubjectAdj = Adjective(randomWord("rhg_adjectives.csv"))
        
        if oPlace.article == None:
            oPlaceArticle = ""
        else:
            oPlaceArticle = oPlace.article
        
        remembranceSentence1 = oSubjectFriend.singular + " said, \"Last time I saw " + oPronoun.object + ", " + oPronoun.subject + " was " + oPlacePrep + " " + oPlaceArticle + " " + oPlace.singular + ".\""
        remembranceSentence2 = "\"" + oPronoun.subject + " was a " + oSubjectAdj.positive + " dude and I'll never forget " + oPronoun.object + ".\""
        
        print("----Today's Death----")
        
        print("\n")
        
        print(string.capwords(obituaryText))
        
        print("\n")
        
        print(remembranceSentence1.capitalize())
        print(remembranceSentence2.capitalize())
        
        print("\n")
        
        
        
    
# def main():
    
#     newHeadline = Headline(type = "basic")
#     newObituary = Obituary()


# print("Content-type: text/plain\n\n")
# main() 





