#!/usr/bin/env python

import os
import sys
import random
import csv
import pprint
import string

import cgitb
cgitb.enable()

CSV_RELATIVE_PATH = "../resources/csv"

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


def randomQuantity():
    singularOrPluralList = ["singular", "plural"]

    singularOrPluralSelection = random.choice(singularOrPluralList)
    if singularOrPluralSelection == "singular":
       return {"form" : "singular", "number" : 1}
    
    else:
        return {"form" : "plural", "number" : random.randrange(2,11,1)}

def nounToPronoun(gender):
    
    pronounList = assemble_csv(CSV_RELATIVE_PATH+"/rhg_pronouns.csv")

    for each in pronounList:
        if each["gender"] == gender:
            return each
def getQuantifiers(countable):
    
    quantifierList = assemble_csv(CSV_RELATIVE_PATH+"/rhg_quantifiers.csv")
    
    countableQuantifierList = quantifierList[0]["countable"].split(",")
    uncountableQuantifierList = quantifierList[0]["uncountable"].split(",")
        
    if countable == 1:
        return countableQuantifierList
     
    else:
        return uncountableQuantifierList
    
def numberToString(number):
    
    numberToStringList = assemble_csv(CSV_RELATIVE_PATH+"/rhg_numbers.csv")
    

    for each in numberToStringList:
        if each["number"] == number:
            return each["string"]
        
#def money():
#    
#    random.randrange(2,5000000)
#    
#
#        


class Word(object):
    
    """This is the word class"""
    
    def __init__(self):
        print "initializing"

    @staticmethod    
    def sandwich():
        pass

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
    
    def __init__(self,definition,quantity = {"number" : 1,"form" : "singular"}):
        
        self.definition = definition
        self.quantity = quantity["number"]
        self.form = quantity["form"]
        
        if "countable" in self.definition:
            self.countable = self.definition["countable"]
        else:
            self.countable = None
        
    @property
    def name(self):
        
        # If there's 1, return the singular form of the noun
        
        if self.quantity == 1:
            return self.singular
        
        # If there's more than 1 and the noun is proper, ignore the
        # quantity and return the singular form
        
        elif self.quantity > 1:
            return self.plural
                 
    @property
    def singular(self):
        return self.definition["singular"]
    
    @property
    def plural(self):
        return self.definition["plural"]
    
    @property
    def gender(self):
        return self.definition["gender"]
    
    @property
    def article(self):
        if self.definition["article"] == "":
            return ""
        else:
            return self.definition["article"]
    
    @property
    def prepositions(self):
        
        """ Return a random preposition (i.e. inside of, on top of) """
        
        if self.definition["prepositions"]:
            prepositionList = self.definition["prepositions"].split(",")
            return random.choice(prepositionList)
        else:
            None
            
    @property
    def quantifiers(self):
        
        # get a list of appropriate quantifiers based on if the noun is countable/uncountable
        
        availableQuantifiers = getQuantifiers(self.countable)
        
        # if the noun is singular and countable, use the article.  Quantifiers describe
        # things that are plural so it wouldn't make sense
        
        if self.form == "singular" and self.countable == "1":
            return self.article
        
        # if the noun is singular and not countable, "some" is the only quantifier
        # afaik that works
        
        if self.form == "singular" and self.countable == "0":
            return "some"
        
        if self.form == "plural":
            return random.choice(availableQuantifiers)
            

class NounAnimate(Noun):
    
    """This is the noun class"""
    
    def __init__(self,definition,quantity):
        
        Noun.__init__(self,definition,quantity)
        
        # if the noun is a proper noun, ignore the quantity and set it to 1
        
        if self.definition["proper"] == "1":
            self.quantity = 1
            self.form = "singular"
            
        # if the noun is a common noun, set it to the quantity    
            
        else:
            self.quantity = quantity["number"]
            self.form = quantity["form"]
                        
    @property
    def proper(self):
        return self.definition["proper"]


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

    @property
    def article(self):
        return self.name["article"]


class Pronoun(Word):

    """This is the Pronoun class."""
    # A new instance requires a noun object and a point of view as an argument. The noun
    # object let's the new pronoun know the form (singular or plural) and the gender (male,female,neuter)
    # so that it knows which dictionary to use.  Valid pov arguments include "1st", "2nd" and "3rd".

    def __init__(self, noun, pov = "1st"):
        
        # if the noun passed is "singular" then assemble the singular
        # pronoun list
        
        if noun.form == "singular":
            pronouns = assemble_csv(CSV_RELATIVE_PATH+"/rhg_sPronouns.csv")
            
        # if the noun passed is "plural" then assemble the plural
        # pronoun list    
            
        if noun.form == "plural":
            pronouns = assemble_csv(CSV_RELATIVE_PATH+"/rhg_pPronouns.csv")
        
        # if the pronoun requested is in the "3rd person", append the gender on the end of it so that
        # it can match the appropriate dictionary in the pronoun list
        
        if pov == "3rd":
            gender = str.capitalize(noun.gender)
            pov = (pov + gender)
        
        # declare the definition method since for some reason it can't be while nested
        
        self.definition = ""
        
        # assign the approprirate dictionary to the definition method based on the requested pov
        # and the noun object's attributes
        
        for each in pronouns:
            if each["point of view"] == pov:
                self.definition = each

    @property
    def object(self):
        return self.definition["object"]
    
    @property
    def subject(self):
        return self.definition["subject"]
    
    @property
    def possessiveD(self):
        return self.definition["possessiveD"]
    
    @property
    def possessiveD(self):
        return self.definition["possessiveP"]
    
    @property
    def reflexive(self):
        return self.definition["reflexive"]
    
    @property
    def reflexive(self):
        return self.definition["have"]


class Headline(object):
    
    # This is the headline class
    
    def __init__(self,*args,**kwargs):
        self.main_headline = None
        if "type" in kwargs and kwargs["type"] == "charity":    
            
            # Create the words necessary for the headline
            
            hSubject = NounAnimate(randomWord(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"),randomQuantity())
            hAction = Verb(randomWord(CSV_RELATIVE_PATH+"/rhg_verbs.csv"))
            hActionTense = ""
            hObject = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nInanimate.csv"),randomQuantity())
            
            # Assign the appropriate tense of the verb based on whether or not
            # the subject is singular/plural
            
            if hSubject.form == "singular":
                hActionTense = hAction.present
                
            if hSubject.form == "plural":
                hActionTense = hAction.infinitive
            
            # Assemble the headline using the words
            
            mainHeadline = "{subject} {action} {theObject} For Charity"
            
            mainHeadlineFormat = mainHeadline.format(subject = hSubject.name,
                                                     action = hActionTense,
                                                     theObject = hObject.name,
                                                    )
            
            # Create the words necessary for the first sentence
            
            hSubjectArticle = hSubject.article
            hSubjectQuantity = hSubject.quantity
            hObjectQuantifier = hObject.quantifiers
            hObjectAdjective = Adjective(randomWord(CSV_RELATIVE_PATH+"/rhg_adjectives.csv"))
            hPlace = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nPlaces.csv"))
            hPlaceAdjective = Adjective(randomWord(CSV_RELATIVE_PATH+"/rhg_adjectives.csv"))
            
            
            # if the subject is a singular common noun use its article
            # if the subject is a proper noun, ignore..
            
            if hSubject.form == "singular" and hSubject.proper == "0":
                hSubjectArticle = hSubjectArticle
            else:
                hSubjectArticle = ""
                
            
            # If there is only one subject, don't indicate the quantity 
            
            if hSubjectQuantity == 1:
                hSubjectQuantity = ""
                
            
            # If there is more than one subject, take the int quantity and
            # convert it to a string (i.e. 4 to four)
                
            elif hSubjectQuantity > 1:
                hSubjectQuantity = numberToString(str(hSubject.quantity))
                
            
            # if "a" is going to be used as an article for the object, use
            # the adjective's article instead since it directly precedes
            # the adjective 
                
            if hObjectQuantifier == hObject.article:
                hObjectQuantifier = hObjectAdjective.article
                
            # Assemble the 1st sentence using the words
            #
            # Ex: Today seven police officers destroyed some naughty couches
            # on a cruise ship for a local charity.
            
            
            firstSentence = ("Today {subjectArticle} {subjectQuantity} {subject} {actionPast}" +
                            " {objectQuantifier} {objectAdjective} {theObject} {placePreposition}" +
                            " {placeArticle} {place} for a local charity.")
            
            firstSentenceFormat = firstSentence.format(subjectArticle = hSubjectArticle,
                                                       subjectQuantity = hSubjectQuantity,
                                                       subject = hSubject.name,
                                                       actionPast = hAction.past,
                                                       objectQuantifier = hObjectQuantifier,
                                                       objectAdjective = hObjectAdjective.positive,
                                                       theObject = hObject.name,
                                                       placePreposition = hPlace.prepositions,
                                                       placeArticle = hPlace.article,
                                                       place = hPlace.name
                                                       )
            
            # Create the words necessary for the 2nd sentence
            
            hAbstract = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nAbstract.csv"))
            hAbstractAdjective = Adjective(randomWord(CSV_RELATIVE_PATH+"/rhg_adjectives.csv"))
            hHeartsAdjective = Adjective(randomWord(CSV_RELATIVE_PATH+"/rhg_adjectives.csv"))
            
            # Assemble the 2nd sentence using the words
            
            secondSentence = ("This generous act of {abstract} demonstrated {possessivePronoun}" +
                             " love of {actionPresentParticiple},")
            
            
            
            # Today Kooly The Bear murdered a filthy flower in a graveyard for
            # the New York Saddle Foundation. The event, which garned an average attendance of 25 people,
            # was said to have raised $25,000.
            
            # Kentucky Dog Hospital, 
            #
            # "I've been coming to this graveyard for twenty-five years.  People love to watch
            # me murder these flowers and I love every second of it.
            #
            # "We've been coming to this graveyard for twenty-five years. People love to watch
            # us murder these flowers and we love every minute of it.
            #
            # {HaveContractionFirstPersonPresent} been coming to this {place} for {number2-50}. People {emotionLoveOrHate}
            # {objectPronoun} {actionInfinitive} and we {emotionLoveOrHate} every {randomAmountOfTime} of it
            #
            #
            
            # raised money
            # much to be proud of
            # will continue to make a positive impact in the years ahead
            
            
            
            #print("\nDebug:\n")
            #
            #print("subject singular: " + hSubject.singular + "\n")
            #print("subject plural: " + hSubject.plural + "\n")
            #print("subject name: " + hSubject.name + "\n")
            #print("object quantifier: " + hObjectQuantifier + "\n")
            #print("object's adjective article: " + hObjectAdjective.article + "\n")
            #
            #
            #print("\nHsubjectQuantity : " + hSubjectQuantity + "\n")
            #
            #if "  " in firstSentenceFormat:
            #    print("This sentence has a double space\n")
            
            
            # Remove extra spaces
            
            if "   " in firstSentenceFormat:
                # print("\nthere's a triple space in the sentence.. repairing.\n")
                firstSentenceFormat = firstSentenceFormat.replace("   "," ")
            
            if "  " in firstSentenceFormat:
                # print("\nthere's a double space in the sentence.. repairing.\n")
                firstSentenceFormat = firstSentenceFormat.replace("  "," ")
            
              
            # print("\n")
            
            # print("----Today's News----")
            
            # print("\n")
            
            # print(string.capwords(mainHeadlineFormat))
            
            # print("\n")
            
            # print(firstSentenceFormat)
        
            # print("\n")

            self.main_headline = string.capwords(mainHeadlineFormat)

            self.blurb = firstSentenceFormat
            # print("\n")
            # print("----Today's News----")
            # print("\n")
            # print(string.capwords(mainHeadline))
            # print("\n")
            # print(hSubject.singular + " replied, " + "\"I " + hAction.past + " " + hObjectArticleQuantifier +
            #       " " + hObjectReply + ". Who Cares?\"")
            # print("\n")
##
## Obit class needs update to new word types
## 
# class Obituary(object):
#     """This is the obituary class"""

#     def __init__(self):
#         #obituary headline

#         oSubject = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"))
#         oVerb = Verb(randomWord(CSV_RELATIVE_PATH+"/rhg_verbs.csv"))
#         oObject = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nInanimate.csv"))
#         oObjectArticleQuantifier = ""
#         oObjectState = ""

#         if oObject.article is None:
#             oObjectState = oObject.plural
#             oObjectArticleQuantifier = random.choice(oObject.quantifier)
#         else:
#             oObjectState = oObject.singular
#             oObjectArticleQuantifier = oObject.article

#         self.headline = oSubject.singular + " dies while " +\
#                              oVerb.presentparticiple + " " +\
#                              oObjectArticleQuantifier + " " +\
#                              oObjectState

#         #remembering the deceased

#         oSubjectFriend = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"))
#         oPlace = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nPlaces.csv"))
#         oPronoun = Pronoun(nounToPronoun(oSubject.gender))
#         oPlacePrep = random.choice(oPlace.prepositions)
#         oPlaceArticle = ""
#         oSubjectAdj = Adjective(randomWord(CSV_RELATIVE_PATH+"/rhg_adjectives.csv"))

#         if oPlace.article is None:
#             oPlaceArticle = ""
#         else:
#             oPlaceArticle = oPlace.article

#         self.full_text = oSubjectFriend.singular + " said, \"Last time I saw " + oPronoun.object + ", " + oPronoun.subject + " was " + oPlacePrep + " " + oPlaceArticle + " " + oPlace.singular + ". " + oPronoun.subject + " was a " + oSubjectAdj.positive + " dude and I'll never forget " + oPronoun.object + ".\""

def randomAnimateNoun(): 
    newNoun =  Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"),randomQuantity())
    print(newNoun.name)
    print(newNoun.quantity)
    print(newNoun.form)



def randomInanimateNoun(): 
    newNoun =  Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nInanimate.csv"),randomQuantity())
    
    print("\n\n")
    
    print(newNoun.name)
    print(newNoun.quantity)
    print(newNoun.form)
    print("countable: " + newNoun.countable)
    print("article: " + str(newNoun.article))
    print("quantifiers: " + newNoun.quantifiers)
    
    print("\n\n")
    
    if newNoun.form == "singular":
        print("He picked up " + newNoun.quantifiers + " " + newNoun.name)
    elif newNoun.form == "plural":
        print("He picked up " + newNoun.quantifiers + " " + newNoun.name)

    print("\n\n")

def main():
    
    newHeadline = Headline(type = "charity")
    #newObituary = Obituary()



character = Noun(randomWord(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"),randomQuantity())
characterPronoun = Pronoun(character,pov = "3rd")

print("\nCharacter: " + character.name)
print("\nCharacter Form: " + character.form)
print("\nCharacter Gender: " + character.gender)
print("\n")

#print("\nCharacter Pronoun: " + characterPronoun.object)
#print("\nCharacter Form: " + characterPronoun.subject)
#print("\nCharacter Gender: " + character.have)
#print("\n")


print("Content-type: text/plain\n\n")

main() 



