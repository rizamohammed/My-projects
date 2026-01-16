from asyncore import poll
from random import choice, choices
from urllib import request
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import Question, Tags
from django.http import Http404
from .models import Choice, Question
from django.urls import reverse
from django.views import generic
import json
from datetime import datetime
from django.http import JsonResponse
from django.template.response import TemplateResponse
# import requests
from django.template.loader import get_template

def returnJsonResponse(request,dataToSend):
    return JsonResponse(dataToSend)
    # pass
def dictMaker(quest,optVoteDict,TgsLst,qid):
    myDict = {
        "Question" : quest,
        "OptionVote" : optVoteDict,
        "Tags" : TgsLst,
        "Question_Id":qid
    }
    return myDict

# Project end points 

def createPoll(request):
    if request.method == "POST":
        jsn = request.body.decode('utf8') 
        data  = json.loads(jsn)
        date = datetime.today()
        question = Question(question_text = data['Question'], pub_date=date)
        question.save()
        for opt in data["OptionVote"].keys():
            choice = Choice(question=question, choice_text = opt, votes = int(data["OptionVote"][opt]))
            choice.save()
        for i in range(len(data["Tags"])):
            tag = data["Tags"][i]
            tags = Tags(question=question, tag_text=tag)
            tags.save()
        return HttpResponse('Poll Created Sucessfully')
    else:
        return render(request,"CreatePoll.html")
      
def getPoll(request):
    qstIds    = Question.objects.values_list('pk', flat=True)
    listOfPoll = []
    for i in qstIds:
        OptVoteDict = {}
        quest = Question.objects.all().filter(id = i)
        tgsFilter = Tags.objects.all().filter(question = i)
        for j in range(len(Choice.objects.values())):
            q_id = Choice.objects.values()[j]['question_id']
            if( i == q_id ):
                opt = Choice.objects.values()[j]['choice_text']
                vot = Choice.objects.values()[j]['votes']
                OptVoteDict.update({
                    str(opt) : vot
                })
        tags = []
        for tag in tgsFilter:
            tags.append(str(tag))
        dictPoll = dictMaker(str(quest[0]),OptVoteDict,tags,i)
        listOfPoll.append(dictPoll)
    # print(listOfPoll)
    return JsonResponse(listOfPoll,None,0)

def filterByTags(request):
    ''' pollDataList is a list of dictionary of all questions       '''
    # ----------------------------------------
    qstIds    = Question.objects.values_list('pk', flat=True)
    pollDataList = []
    for i in qstIds:
        OptVoteDict = {}
        quest = Question.objects.all().filter(id = i)
        tgsFilter = Tags.objects.all().filter(question = i)
        for j in range(len(Choice.objects.values())):
            q_id = Choice.objects.values()[j]['question_id']
            if( i == q_id ):
                opt = Choice.objects.values()[j]['choice_text']
                vot = Choice.objects.values()[j]['votes']
                OptVoteDict.update({
                    str(opt) : vot
                })
        tags = []
        for tag in tgsFilter:
            tags.append(str(tag))
        dictPoll = dictMaker(str(quest[0]),OptVoteDict,tags,i)
        pollDataList.append(dictPoll)
    # --------------------------------
    RowFilteredList = []
    filteredList = []
    tags = request.GET.get("tags","")
    userTagsLst = str(tags).split(",")
    
    for userTag in userTagsLst:
        for i in range(len(pollDataList)):
            if(str(userTag) in pollDataList[i]["Tags"]):
                RowFilteredList.append(pollDataList[i])
    for j in RowFilteredList:
        if j not in filteredList:
            filteredList.append(j)
    return JsonResponse(filteredList,None,0)

def allTags(request):
    dictTags = {}
    allTagsLst = []
    for i in Tags.objects.all():
        allTagsLst.append(str(i))
    allTagsLst = list(dict.fromkeys(allTagsLst))
    dictTags.update(
        {
            "Tags" : allTagsLst
        })
    
    return JsonResponse(dictTags,None,0)

def getQuest_Vote(request,question_id):
    qstIds    = Question.objects.values_list('pk', flat=True)
    for Ids in qstIds:
        if(Ids == question_id ):
            questReq = Question.objects.filter(id=Ids)[0]
            # ----------------------------------------
        qstIds    = Question.objects.values_list('pk', flat=True)
        pollDataList = []
        for i in qstIds:
            OptVoteDict = {}
            quest = Question.objects.all().filter(id = i)
            tgsFilter = Tags.objects.all().filter(question = i)
            for j in range(len(Choice.objects.values())):
                q_id = Choice.objects.values()[j]["question_id"]
                if( i == q_id ):
                    opt = Choice.objects.values()[j]['choice_text']
                    vot = Choice.objects.values()[j]['votes']
                    OptVoteDict.update({
                        str(opt) : vot
                    })
            tags = []
            for tag in tgsFilter:
                tags.append(str(tag))
            dictPoll = dictMaker(str(quest[0]),OptVoteDict,tags,i)
            pollDataList.append(dictPoll)

    for i in range(len(pollDataList)):
        if( str(pollDataList[i]["Question"]) == str(questReq) ):
            data = pollDataList[i]


    if request.method == "GET":
        return JsonResponse(data)

def home(request):
    return render(request,"Home.html")
    
def pollDetail(request,id):
    mydata = {
        "questId" : id
    }
    return render(request,"PollDetail.html",mydata)

def votePoll(request,question_id):
        # --------------------g--------------------
    qstIds    = Question.objects.values_list('pk', flat=True)
    result = []
    for Ids in qstIds:
        if(Ids == question_id ):
            questReq = Question.objects.filter(id=Ids)[0]
        qstIds    = Question.objects.values_list('pk', flat=True)
        pollDataList = []
        for i in qstIds:
            OptVoteDict = {}
            quest = Question.objects.all().filter(id = i)
            tgsFilter = Tags.objects.all().filter(question = i)
            for j in range(len(Choice.objects.values())):
                q_id = Choice.objects.values()[j]["question_id"]
                if( i == q_id ):
                    opt = Choice.objects.values()[j]['choice_text']
                    vot = Choice.objects.values()[j]['votes']
                    OptVoteDict.update({
                        str(opt) : vot
                    })
            tags = []
            for tag in tgsFilter:
                tags.append(str(tag))
            dictPoll = dictMaker(str(quest[0]),OptVoteDict,tags,i)
            pollDataList.append(dictPoll)

    for i in range(len(pollDataList)):
        if( str(pollDataList[i]["Question"]) == str(questReq) ):
            data = pollDataList[i]

        # -----------------------------------
    if request.method == "PUT":
        jsn = request.body.decode('utf8') 
        content  = json.loads(jsn)
        option = content["incrementOption"] # It is a option which is to be subjected to increment
        
        try:
            vote = data["OptionVote"][option]
            vote +=1
            VoteToSave = Choice(question=questReq,choice_text=option,votes=vote)
            VoteToSave.save()
            result.append("Vote sucessfully added")
            return HttpResponse("Vote sucessfully added")
        except:
            result.append("Vote has not been added.")
            return HttpResponse("Vote has not been updated. Please try with a valid option.")
    else:

        mydata = {
            "qId" : question_id,
        }
        return render(request,"Vote.html",mydata)