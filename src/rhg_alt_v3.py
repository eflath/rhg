#!/usr/bin/env python

import os
import sys
import random
import csv
import pprint
import string
import locale


import cgitb
cgitb.enable()

CSV_RELATIVE_PATH = "../resources/csv"

test = []

##Pretty print
##syntax: pp.pprint(stuff)

pp = pprint.PrettyPrinter(indent=4)

 
def randomDict(csvfile,filter = 0):
    
    """returns a random word dict"""
    
    return random.choice(csvToDict(csvfile,filter))


def superPrint(myList):
    
    for d in myList:
        print d["singular"]

def csvToDict(csvfile,filter = 0):
    
    """returns a list of dicts from the provided csvfile(s), each
    dict corresponding to a row in the file.  A custom list is
    returned if the user provides a filter. The filter should be
    provided in dict format like {"uscapitals" = "1", "human" : "1"}
    """
    
    # return a list of dictionaries, each dictionary representing a horizontal
    # row in the csv
    
    dictList = []

    for f in csvfile:
        csvReader = csv.DictReader(open(f,"rb"))
        for each in csvReader:
            dictList.append(each)
    
    
    # create an empty list to eventually be filled with words that match
        # the filter(s)
        
    filteredDictList = []
    
    
    if filter is not 0:
        
        
        # for every word in the full list of words, check to see if it matches
        # the filter.  If it matches, add it to the custom word list, otherwise
        # move on to the next.
        
        for word in dictList:
            newWord = _csvToDictFilter(word,filter)
            if newWord:
                filteredDictList.append(newWord)
                
    else:
        filteredDictList = dictList
    
    
    
    return filteredDictList
        
          

def _csvToDictFilter(word,filter):
    """returns a word(dict) if it has a key/value pair that matches
    the filter
    """
    
    # for each filter, if the word has a matching key/value pair,
    # return the word.  If not, return None.

    
    for (key,value) in filter.items():
        if word[key] != value:
            return
    return word
            
def randomQuantity():
    singularOrPluralList = ["singular", "plural"]

    singularOrPluralSelection = random.choice(singularOrPluralList)
    if singularOrPluralSelection == "singular":
       return {"form" : "singular", "number" : 1}
    
    else:
        return {"form" : "plural", "number" : random.randrange(2,11,1)}

def nounToPronoun(gender):
    
    pronounList = csvToDict(CSV_RELATIVE_PATH+"/rhg_pronouns.csv")

    for each in pronounList:
        if each["gender"] == gender:
            return each

def getQuantifiers(countable):
    
    quantifierList = csvToDict([CSV_RELATIVE_PATH+"/rhg_quantifiers.csv"])
    
    countableQuantifierList = quantifierList[0]["countable"].split(",")
    uncountableQuantifierList = quantifierList[0]["uncountable"].split(",")
        
    if countable == 1:
        return countableQuantifierList
     
    else:
        return uncountableQuantifierList
    
def numberToString(number):
    
    numberToStringList = csvToDict([CSV_RELATIVE_PATH+"/rhg_numbers.csv"])
    

    for each in numberToStringList:
        if each["number"] == number:
            return each["string"]
        

def dollars(amount):
    
    locale.setlocale( locale.LC_ALL, '' )
    
    convertedAmount = locale.currency( amount, grouping=True )
    
    convertedAmount = convertedAmount.split(".")
        
    return convertedAmount[0]    

def weightedDonationAmount():
    
    rangeMasterList = [[2,5000000],[2,500000],[2,10000],[2,5000],[2,500],[2,50]]
    
    randomRange = random.choice(rangeMasterList)
    
    return random.randint(randomRange[0],randomRange[1])


def randomName(gender = "m"):
    
    firstNameList = csvToDict([CSV_RELATIVE_PATH + "/rhg_firstNames.csv"],{"gender" : gender})
    lastNameList = csvToDict([CSV_RELATIVE_PATH+"/rhg_lastNames.csv"]) 
       
    name = random.choice(firstNameList)["first"]
    lastName = random.choice(lastNameList)["last"]
          
    return (name,lastName)

def randomGender():
    
    gender = ["m","f"]

    return random.choice(gender)

def getJob(job = None):
    
    allJobs = csvToDict([CSV_RELATIVE_PATH + "/rhg_nJobs.csv"])
    
    if job == None:
        return random.choice(allJobs)

    else:
        for each in allJobs:
            if each["singular"] == job:
                return each

def ageToStage(age):
    
    allStages = csvToDict([CSV_RELATIVE_PATH + "/rhg_nStages.csv"])
    
    matchedStages = []
    
    for stage in allStages:
        if age >= int(stage["range_low"]) and age <= int(stage["range_high"]):
            matchedStages.append(stage)
    
    return random.choice(matchedStages)
    
   
def createHumanSubject(amount,**kwargs):
    
    if amount == None:
        subjectAmount = random.randint(1,10)
        
    else:
        subjectAmount = amount
    
    print("\n\\\\\\\\")
    print("subjectAmount:")
    print(subjectAmount)
    print("\n\\\\\\\\")
    
    print("\n\\\\\\\\")
    print("range:")
    print(range(subjectAmount))
    print("\n\\\\\\\\")

    humanSubjectList = []
    
    print(kwargs)
    
    for i in range(subjectAmount):
        
        print(i)
        
        if kwargs == {}:
            newHumanSubject = Human()
            humanSubjectList.append(newHumanSubject)
            print(humanSubjectList)
        else:
            newHumanSubject = Human(**kwargs)
            humanSubjectList.append(newHumanSubject)
            print(humanSubjectList)
         
    return humanSubjectList


class HumanGroup(object):
    
    """This is the human group class"""
    
    def __init__(self,count,**kwargs):
        
        if count == None:
            self.humanCount = random.randint(1,10)
        
        else:
            self.humanCount = count
            
        self.humanList = []
        
        for i in range(self.humanCount):
            if kwargs == {}:
                newHuman = Human()
                self.humanList.append(newHuman)
                #print(humanList)
            else:
                newHuman = Human(**kwargs)
                self.humanList.append(newHuman)
                #print(humanList)    
    
    @property
    def jobs(self):
        
        jobList = []
        
        for each in self.humanList:
            jobList.append(each.job["singular"])
        
        
        jobDict = {}
        
        for job in jobList:
            if job not in jobDict:
                print(job)
                jobDict[job] = 1
            else:
                print(job)
                jobDict[job] += 1
        
        print(jobDict)
        
        
        
        #
        #for each in jobList:
        #    print(jobList.count(each))
        #
        #
        #return jobList
        
        
        
        
        
        


class Human(object):
    
    """This is the human class"""
    
    def __init__(self,gender = None,fullName = None,age = None,job = None):
        
        # if a gender hasn't been provided, pick
        # a random gender
        
        if gender == None:
            self.gender = randomGender()
        else:
            self.gender = gender
        
        print("\n\\\\\\\\\\\\\\\\\\")
        print "%s" % (self.gender)
        print("\\\\\\\\\\\\\\\\\\")
        
        # if a name hasn't been provided, pick
        # a random name
        
        if fullName == None:
            
            fullName = randomName(self.gender)
            self.fullName = fullName
            self.firstName = fullName[0]
            self.lastName = fullName[1]
        else:
            self.fullName(fullName[0],fullName[1])
            self.firstName = fullName[0]
            self.lastName = fullName[1]
        
        print("\n\\\\\\\\\\\\\\\\\\")
        print "%s %s" % (self.fullName[0],self.fullName[1])
        print "%s" % (self.firstName)
        print "%s" % (self.lastName)
        print("\\\\\\\\\\\\\\\\\\")
        
        
        # if an age hasn't been provided, pick
        # a random age.
        
        if age == None:
            self.age = random.randint(0,105)
        else:
            self.age = age
        
        print("\n\\\\\\\\\\\\\\\\\\")
        print "%s" % (self.age)
        print("\\\\\\\\\\\\\\\\\\")
        
            
        # determine the stage in the human's life
        # based on age
        
        self.stage = ageToStage(self.age)
        
        print("\n\\\\\\\\\\\\\\\\\\")
        print "%s" % (self.stage)
        print("\\\\\\\\\\\\\\\\\\")
        
        # if a job hasn't been provided, pick
        # a random job.  A specific job can be provided
        # by using the getJob() function and passing
        # the job name as an argument, i.e., getJob("baker")
    
        if job == None:
            self.job = getJob()
        else:
            self.job = job
        
        print("\n\\\\\\\\\\\\\\\\\\")
        print "%s" % (self.job)
        print("\\\\\\\\\\\\\\\\\\")
    
    def __repr__(self):
        return ("<Human instance: %s %s>") % (self.fullName)
    
    def __str__(self):
        return ("%s %s") % (self.fullName)
    
           
    def hello(self):
        
        hello = ("Hello, my name is {firstName} {lastName} and I am {stageArticle} {stage}!" +
                 " I'm {age} years old and working as {jobArticle} {job}!")
            
        helloFormat = hello.format(firstName = self.firstName,
                                   lastName = self.lastName,
                                   stageArticle = self.stage["article"],
                                   stage = self.stage["singular"],
                                   age = self.age,
                                   jobArticle = self.job["article"],
                                   job = self.job["singular"])
                                                    
        print(helloFormat)
        



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
    def proper(self):
        return self.definition["proper"]
    
    @property
    def gender(self):
        if "gender" in self.definition:
            return self.definition["gender"]
        else:
            return "neuter"
        
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
                        

class Subject(object):
    
    """This is the subject class"""
    
    def __init__(self,subjects,quantity):
        pass
        # subjects is a list of all of the 
        
    
    





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
            pronouns = csvToDict([CSV_RELATIVE_PATH+"/rhg_sPronouns.csv"])
            
        # if the noun passed is "plural" then assemble the plural
        # pronoun list    
            
        if noun.form == "plural":
            pronouns = csvToDict([CSV_RELATIVE_PATH+"/rhg_pPronouns.csv"])
        
        # if the pronoun requested is in the "3rd person", append the gender on the end of it so that
        # it can match the appropriate dictionary in the pronoun list
        
        if pov == "3rd":
            if noun.gender:
                gender = str.capitalize(noun.gender)
                pov = (pov + gender)
            else:
                pov = "3rdNeuter"
        
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
    def have(self):
        return self.definition["have"]
    
    @property
    def demonstrativeClose(self):
        return self.definition["demonstrative close"]
    
    @property
    def demonstrativeFar(self):
        return self.definition["demonstrative far"]
    


class Headline(object):
    
    # This is the headline class
    
    def __init__(self,*args,**kwargs):
        self.main_headline = None
        if "type" in kwargs and kwargs["type"] == "charity":    
            
            # Create the words necessary for the headline
            
            hSubject = NounAnimate(randomDict([CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"]),randomQuantity())
            hAction = Verb(randomDict([CSV_RELATIVE_PATH+"/rhg_verbs.csv"]))
            hActionTense = ""
            hObject = Noun(randomDict([CSV_RELATIVE_PATH+"/rhg_nInanimate.csv"]),randomQuantity())
            
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
            hObjectAdjective = Adjective(randomDict([CSV_RELATIVE_PATH+"/rhg_adjectives.csv"]))
            hPlace = Noun(randomDict([CSV_RELATIVE_PATH+"/rhg_nPlaces.csv"]))
            hPlaceAdjective = Adjective(randomDict([CSV_RELATIVE_PATH+"/rhg_adjectives.csv"]))
            hFoundationCity = Noun(randomDict([CSV_RELATIVE_PATH+"/rhg_nPlaces.csv"],{"uscapital" : "1"}))
            hFoundationObject = Noun(randomDict([CSV_RELATIVE_PATH+"/rhg_nInanimate.csv"]),randomQuantity())
            hFoundationSuffix = random.choice(["Foundation","Institute","Alliance","Hospital","Association","Conservancy",
                                               "Society","Trust","Committee","Fund"])
                                               
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
                         
            # Assemble the 1st sentence using the words
            #
            # Ex: Today seven police officers destroyed some naughty couches
            # on a cruise ship for a local charity.
            
            firstSentence = ("Today {subjectArticle} {subjectQuantity} {subject} {actionPast}" +
                            " {objectQuantifier} {theObject} {placePreposition}" +
                            " {placeArticle} {place} for the {foundationCity} {foundationObject} {foundationSuffix}. ")
            
            firstSentenceFormat = firstSentence.format(subjectArticle = hSubjectArticle,
                                                       subjectQuantity = hSubjectQuantity,
                                                       subject = hSubject.name,
                                                       actionPast = hAction.past,
                                                       objectQuantifier = hObjectQuantifier,
                                                       theObject = hObject.name,
                                                       placePreposition = hPlace.prepositions,
                                                       placeArticle = hPlace.article,
                                                       place = hPlace.name,
                                                       foundationCity = hFoundationCity.name,
                                                       foundationObject = hFoundationObject.singular.capitalize(),
                                                       foundationSuffix = hFoundationSuffix
                                                       )
            
            # Create the words necessary for the 2nd sentence
            
            hAttendanceAmount = random.randint(2,998)
            hDollarsInt = weightedDonationAmount()
            hDollars = dollars(hDollarsInt)
            hDollarsAdjective = ["a paltry","a dissapointing","an astonishing"]
            
            # Choose an adjective for the dollar amount based on how high are low it is..
            
            if hDollarsInt < 500:
                hDollarsAdjective = hDollarsAdjective[0]
                
            elif hDollarsInt >= 500 and hDollarsInt <= 2500:
                hDollarsAdjective = hDollarsAdjective[1]
                
            elif hDollarsInt >= 500000:
                hDollarsAdjective = hDollarsAdjective[2]    
                
            else:
                hDollarsAdjective = ""
            
            
            # Assemble the 2nd sentence using the words
            
            secondSentence = ("The event, which garnered an average attendance of {attendanceAmount}" +
                              " people, was said to have raised {dollarsAdjective} {dollars}. ")
            
            secondSentenceFormat = secondSentence.format(attendanceAmount = hAttendanceAmount,
                                                         dollarsAdjective = hDollarsAdjective,
                                                         dollars = hDollars
                                                         )
                       
            # Create the words necessary for the 3rd sentence
            
            hSubjectPronoun1st = Pronoun(hSubject,pov = "1st")
            hPlacePronoun3rd = Pronoun(hPlace,pov = "3rd")
            hPlacePronounDemonstrativeClose = hPlacePronoun3rd.demonstrativeClose
            hObjectPronoun3rd = Pronoun(hObject,pov = "3rd")
            hObjectPronoun3rdDemonstrativeClose = hObjectPronoun3rd.demonstrativeClose
            hSubjectQuantifier = ""
            
            # If the object is not countable, use "this" as its close demonstrative pronoun,
            # because otherwise it sounds strange.. i.e. : Given the object blood, it would write
            # "People love to watch me eat these blood" if blood were plural
            
            
            if hPlace.proper == "1":
                hPlacePronounDemonstrativeClose = ""
            
            if hObject.countable == "0":
                hObjectPronoun3rdDemonstrativeClose = "this"

            if hSubject.form == "singular" and hSubject.proper == "0":
                hSubjectQuantifier = "the"
                
            if hSubject.form == "plural":
                hSubjectQuantifier = "one of the"
             
            # Assemble the 3rd sentence using the words
            
            thirdSentence = ("{beginQuote}{subjectPronoun1stHave} been coming to {placePronounDemonstrative} " +
                            "{place} for {numberOfYears} years. People love to watch {subjectPronoun1stObject} " +
                            "{actionInfinitive} {objectPronoun3rdDemonstrative} {theobject} and {SubjectPronoun1stSubject} " +
                            "love every second of it!{endQuote}, explained {subjectQuantifier} {subject}.")
            
            
            #thirdSentence = ("{pronoun1stHave} been coming to {this} {place} for {numberOfYears} years. " +
            #                 "People love to watch {Pronoun} {actionInfinitive} {thisThese} {object} and " +
            #                 "{Pronoun} {emotion} every second of it.")
            
            thirdSentenceFormat = thirdSentence.format(beginQuote = "\"",
                                                       subjectPronoun1stHave = hSubjectPronoun1st.have.capitalize(),
                                                       placePronounDemonstrative = hPlacePronounDemonstrativeClose,
                                                       place = hPlace.name,
                                                       numberOfYears = str(random.randint(2,79)),
                                                       subjectPronoun1stObject = hSubjectPronoun1st.object,
                                                       actionInfinitive = hAction.infinitive,
                                                       objectPronoun3rdDemonstrative = hObjectPronoun3rdDemonstrativeClose,
                                                       theobject = hObject.name,
                                                       SubjectPronoun1stSubject = hSubjectPronoun1st.subject,
                                                       subjectQuantifier = hSubjectQuantifier,
                                                       subject = hSubject.name,
                                                       endQuote = "\""
                                                       )
            

            # Remove extra spaces
            
            if "   " in firstSentenceFormat:
                # print("\nthere's a triple space in the sentence.. repairing.\n")
                firstSentenceFormat = firstSentenceFormat.replace("   "," ")
            
            if "  " in firstSentenceFormat:
                # print("\nthere's a double space in the sentence.. repairing.\n")
                firstSentenceFormat = firstSentenceFormat.replace("  "," ")
            
            if "  " in secondSentenceFormat:
                # print("\nthere's a double space in the sentence.. repairing.\n")
                secondSentenceFormat = secondSentenceFormat.replace("  "," ")
            
            if "  " in secondSentenceFormat:
                # print("\nthere's a double space in the sentence.. repairing.\n")
                secondSentenceFormat = secondSentenceFormat.replace("  "," ")
               
            if "   " in thirdSentenceFormat:
                # print("\nthere's a triple space in the sentence.. repairing.\n")
                thirdSentenceFormat = thirdSentenceFormat.replace("   "," ")
            
            if "  " in thirdSentenceFormat:
                # print("\nthere's a double space in the sentence.. repairing.\n")
                thirdSentenceFormat = thirdSentenceFormat.replace("  "," ")    
            
              
            print("\n")
           
            print("----Today's News----")
           
            print("\n")
           
            print(string.capwords(mainHeadlineFormat))
           
            print("\n")
           
            print(firstSentenceFormat + secondSentenceFormat + thirdSentenceFormat)
       
            print("\n")

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

#         oSubject = Noun(randomDict(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"))
#         oVerb = Verb(randomDict(CSV_RELATIVE_PATH+"/rhg_verbs.csv"))
#         oObject = Noun(randomDict(CSV_RELATIVE_PATH+"/rhg_nInanimate.csv"))
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

#         oSubjectFriend = Noun(randomDict(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"))
#         oPlace = Noun(randomDict(CSV_RELATIVE_PATH+"/rhg_nPlaces.csv"))
#         oPronoun = Pronoun(nounToPronoun(oSubject.gender))
#         oPlacePrep = random.choice(oPlace.prepositions)
#         oPlaceArticle = ""
#         oSubjectAdj = Adjective(randomDict(CSV_RELATIVE_PATH+"/rhg_adjectives.csv"))

#         if oPlace.article is None:
#             oPlaceArticle = ""
#         else:
#             oPlaceArticle = oPlace.article

#         self.full_text = oSubjectFriend.singular + " said, \"Last time I saw " + oPronoun.object + ", " + oPronoun.subject + " was " + oPlacePrep + " " + oPlaceArticle + " " + oPlace.singular + ". " + oPronoun.subject + " was a " + oSubjectAdj.positive + " dude and I'll never forget " + oPronoun.object + ".\""

def randomAnimateNoun(): 
    newNoun =  Noun(randomDict(CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"),randomQuantity())
    print(newNoun.name)
    print(newNoun.quantity)
    print(newNoun.form)



def randomInanimateNoun(): 
    newNoun =  Noun(randomDict(CSV_RELATIVE_PATH+"/rhg_nInanimate.csv"),randomQuantity())
    
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



character = Noun(randomDict([CSV_RELATIVE_PATH+"/rhg_nAnimate.csv"]),randomQuantity())
characterPronoun = Pronoun(character,pov = "3rd")

hPlace = Noun(randomDict([CSV_RELATIVE_PATH+"/rhg_nPlaces.csv"]))
hPlacePronounDemonstrative = Pronoun(hPlace,pov = "3rd")



print("Content-type: text/plain\n\n")

main() 



