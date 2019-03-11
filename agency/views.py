from django.shortcuts import render_to_response,get_object_or_404
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Author,Story
import numpy as np
from rest_framework.views import APIView
from rest_framework import exceptions
from rest_framework.authentication import BasicAuthentication
from agency import models
from django.utils import timezone
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth import authenticate, login, logout
import datetime
from django.contrib import auth


# login
@csrf_exempt
def login(request):
    # author 必须在这里添加了才有用，在site中添加的连接不上去
    # models.Author.objects.create(username="new", password="new")
    # models.Author.objects.create(username="555", password="555") ok
    if request.method == 'POST':
        name=request.POST.get('username')
        pwd=request.POST.get('password')

        if name :
            try:
                user = models.Author.objects.get(username=name)
                # user = models.Author.objects.filter(username=name, password=pwd)
            except:
                payload = {'sorry': 'unsername not exists !'}
                http_badresponse = HttpResponse(json.dumps(payload))
                http_badresponse['content-type'] = 'text/plain'
                http_badresponse.status_code = 404
                http_badresponse.reason_phrase = ' unsername or password is wrong'
                return http_badresponse

        else : # get username
            return HttpResponse("please input your username and password")

        if pwd :
            # get pwd

            if user.password == pwd :
                request.session['name'] = user.username
                # 登陆成功
                payload = {'Hell': 'welcome you !'}
                http_response = HttpResponse(json.dumps(payload))
                http_response['content-type'] = 'text/plain'
                http_response.status_code = 200
                http_response.reason_phrase = 'OK'
                return http_response
            else:
                # 登陆失败
                payload = {'sorry': 'unsername or password is wrong !'}
                http_badresponse = HttpResponse(json.dumps(payload))
                http_badresponse['content-type'] = 'text/plain'
                http_badresponse.status_code = 404
                http_badresponse.reason_phrase = ' unsername or password is wrong'
                return http_badresponse
        else:
            return HttpResponse("please input your password and password")


    # post request
    else:
        payload = {'request problem': 'need POST request '}
        http_badresponse = HttpResponse(json.dumps(payload))
        http_badresponse['content-type'] = 'text/plain'
        http_badresponse.status_code = 404
        http_badresponse.reason_phrase = 'need POST request'
        return http_badresponse

# log out
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        # 登出成功 (ok)
        del request.session['name']
        payload = {'Goodbye': 'see u next time !'}
        http_response = HttpResponse(json.dumps(payload))
        http_response['content-type'] = 'text/plain'
        http_response.status_code = 200
        http_response.reason_phrase = 'OK'
        return http_response
    else:
        # 登出失败 (ok)
        payload = {'request problen': ' need POST request '}
        http_badresponse = HttpResponse(json.dumps(payload))
        http_badresponse['content-type'] = 'text/plain'
        http_badresponse.status_code = 404
        http_badresponse.reason_phrase = 'need POST request'
        return http_badresponse


# post story
@csrf_exempt
def poststory(request):
    if request.method == 'POST':
        # check if log in
        if 'name' in request.session :
            # get data （ok）
            head = request.POST.get('headline')
            reg = request.POST.get('region')
            cat = request.POST.get('category')
            det = request.POST.get('details')
            # input not 0 (ok)
            if head and cat and reg and det:
                if (cat == 'tech') or (cat == 'art') or (cat == 'pol') or (cat == 'trivia'):
                    if (reg =='uk') or (reg =='w') or (reg == 'eu'):
                        try:
                            # 1
                            # user_todo = Story(tory_headline=head, story_details=det,author=request.session['name'],story_category=cat,story_region=reg, created_time=datetime.datetime.now(),unique_key=1)
                            # user_todo.save()
                            # 2
                            #user_todo = models.Story(story_headline=head, story_details=det, author=user_id,story_category=cat, story_region=reg)
                            #user_todo.save()
                            # # 3
                            #models.Story.objects.create(story_headline=head, story_details=det, author=user_id,story_category=cat, story_region=reg)
                            # dic = {'story_headline': head, 'story_details': det,'author':user_id,'story_region':reg}
                            # models.Story.objects.create(**dic)
                            # 1
                            # save data
                            #dic = {'story_headline': head, 'story_details': det,'story_region':reg,'story_category':cat}
                            #models.Story.objects.create(**dic)

                              ###  方法1 ok  ###
                            #初始化
                            user_id = models.Author.objects.get(username=request.session['name']) # 只是名字无pwd
                            # create 对象
                            #models.Story.objects.create(author = user_id,story_headline=head, story_details=det,story_category=cat, story_region=reg)
                               ### 方法 2 ok ###
                            p = models.Story()
                            p.author = user_id
                            p.story_category=cat
                            p.story_headline=head
                            p.story_region=reg
                            p.story_details=det
                            # no
                            # p.created_time = models.DateTimeField(default=timezone.now,auto_created = True )
                            p.save()
                            # 有问题 print(p.XX)
                            #print(p.created_time)


                        except:
                            payload = {'sorry': 'cannot create object!'}
                            http_badresponse = HttpResponse(json.dumps(payload))
                            http_badresponse['content-type'] = 'text/plain'
                            http_badresponse.status_code = 503
                            http_badresponse.reason_phrase = ' it may already exists or datatype is wrong'
                            return http_badresponse
                            # catogory not satisfied

                    else:
                        payload = {
                            'region reuqire': 'please input right region'}
                        http_badresponse = HttpResponse(json.dumps(payload))
                        http_badresponse['content-type'] = 'text/plain'
                        http_badresponse.status_code = 503
                        http_badresponse.reason_phrase = ' region require !'
                        return http_badresponse

                # catogory not satisfied
                else:
                    payload = {
                        'category reuqire': 'please input right category'}
                    http_badresponse = HttpResponse(json.dumps(payload))
                    http_badresponse['content-type'] = 'text/plain'
                    http_badresponse.status_code = 503
                    http_badresponse.reason_phrase = ' category require !'
                    return http_badresponse

            # input require
            else:
                payload = {'input reuqire':'please input : story_headline,story_details ,author,story_category and story_region'}
                http_badresponse = HttpResponse(json.dumps(payload))
                http_badresponse['content-type'] = 'text/plain'
                http_badresponse.status_code = 503
                http_badresponse.reason_phrase = ' input require !'
                return http_badresponse


            # http response
            payload = {'ok': 'created'}
            http_badresponse = HttpResponse(json.dumps(payload))
            http_badresponse['content-type'] = 'text/plain'
            http_badresponse.status_code = 201
            http_badresponse.reason_phrase = ' created!'
            return http_badresponse

        # login request (ok)
        else:
             # 没登陆
            payload = {'login request': 'please login first !'}
            http_badresponse3 = HttpResponse(json.dumps(payload))
            http_badresponse3['content-type'] = 'text/plain'
            http_badresponse3.status_code = 503
            http_badresponse3.reason_phrase = ' please login first !'
            return http_badresponse3

    # post request (ok)
    else:
        payload = {'request problem': 'need POST request '}
        http_badresponse = HttpResponse(json.dumps(payload))
        http_badresponse['content-type'] = 'text/plain'
        http_badresponse.status_code = 404
        http_badresponse.reason_phrase = 'need POST request'
        return http_badresponse


# get story
@csrf_exempt
def getstories(request):
    # get data
    if request.method == "GET":
        reg = request.GET.get('story_region')
        cat = request.GET.get('story_cat')
        date = request.GET.get('story_date')

        # input not 0 (ok)
        if reg and cat and date :
            if (cat == 'tech') or (cat == 'art') or (cat == 'pol') or (cat == 'trivia' or (cat == '*' ) ):
                if (reg == 'uk') or (reg == 'w') or (reg == 'eu' or (reg =='*') ):
                    try:
                        # ok
                        if (cat != '*') & (reg != '*') :
                            text = Story.get1(date, cat, reg)
                            print(text)
                            # http response
                            payload = {'stories': str(text)}
                            http_response = HttpResponse(json.dumps(payload))
                            http_response['content-type'] = 'text/plain'
                            http_response.status_code = 200
                            http_response.reason_phrase = ' ok'
                            return http_response

                        if (cat == '*')  & (reg != '*') :
                            text = Story.get2(date, reg)
                            # http response
                            payload = {'stories': str(text)}
                            http_response = HttpResponse(json.dumps(payload))
                            http_response['content-type'] = 'text/plain'
                            http_response.status_code = 200
                            http_response.reason_phrase = ' ok'
                            return http_response

                        if (reg == '*') & (cat != '*') :
                            text = Story.get3(date, cat)
                            # http response
                            payload = {'stories': str(text)}
                            http_response = HttpResponse(json.dumps(payload))
                            http_response['content-type'] = 'text/plain'
                            http_response.status_code = 200
                            http_response.reason_phrase = ' ok'
                            return http_response

                        if (reg == '*') & (cat == '*') :
                            text = Story.get4(date)
                            print(text)
                            # http response
                            payload = {'stories': str(text)}
                            http_response = HttpResponse(json.dumps(payload))
                            http_response['content-type'] = 'text/plain'
                            http_response.status_code = 200
                            http_response.reason_phrase = ' ok'
                            return http_response




                    except:
                        payload = {'sorry': 'cannot find object!'}
                        http_badresponse = HttpResponse(json.dumps(payload))
                        http_badresponse['content-type'] = 'text/plain'
                        http_badresponse.status_code = 404
                        http_badresponse.reason_phrase = ' sorry'
                        return http_badresponse


                else:
                    payload = {
                        'region reuqire': 'please input right region'}
                    http_badresponse = HttpResponse(json.dumps(payload))
                    http_badresponse['content-type'] = 'text/plain'
                    http_badresponse.status_code = 503
                    http_badresponse.reason_phrase = ' region require !'
                    return http_badresponse

            # catogory not satisfied
            else:
                payload = {
                    'category reuqire': 'please input right category'}
                http_badresponse = HttpResponse(json.dumps(payload))
                http_badresponse['content-type'] = 'text/plain'
                http_badresponse.status_code = 503
                http_badresponse.reason_phrase = ' category require !'
                return http_badresponse



        # input require
        else:
            payload = {
                'input reuqire': 'please input，story_cat，story_date '}
            http_badresponse = HttpResponse(json.dumps(payload))
            http_badresponse['content-type'] = 'text/plain'
            http_badresponse.status_code = 503
            http_badresponse.reason_phrase = ' input require !'
            return http_badresponse



        # get request (ok)
    else:
        payload = {'request problem': 'need GET request '}
        http_badresponse = HttpResponse(json.dumps(payload))
        http_badresponse['content-type'] = 'text/plain'
        http_badresponse.status_code = 404
        http_badresponse.reason_phrase = 'need get request'
        return http_badresponse


# delete story
@csrf_exempt
def deletestory(request):
    if request.method == 'POST':
        # check if log in
        if 'name' in request.session :
            # get data （ok）
            story_key = request.POST.get('story_key')

            # input not 0 (ok)
            if story_key:
                try:
                    # 1

                    dele = models.Story.objects.filter(unique_key=story_key).delete()

                    # http response
                    payload = {'ok': 'created'}
                    http_badresponse = HttpResponse(json.dumps(payload))
                    http_badresponse['content-type'] = 'text/plain'
                    http_badresponse.status_code = 201
                    http_badresponse.reason_phrase = ' created!'
                    return http_badresponse

                except:
                    payload = {'sorry': 'cannot delete object!'}
                    http_badresponse = HttpResponse(json.dumps(payload))
                    http_badresponse['content-type'] = 'text/plain'
                    http_badresponse.status_code = 503
                    http_badresponse.reason_phrase = ' it may already exists or datatype is wrong'
                    return http_badresponse
                    # catogory not satisfied

            # input require
            else:
                payload = {'input reuqire':'please input : story_headline,story_details ,author,story_category and story_region'}
                http_badresponse = HttpResponse(json.dumps(payload))
                http_badresponse['content-type'] = 'text/plain'
                http_badresponse.status_code = 503
                http_badresponse.reason_phrase = ' input require !'
                return http_badresponse




        # login request (ok)
        else:
             # 没登陆
            payload = {'login request': 'please login first !'}
            http_badresponse3 = HttpResponse(json.dumps(payload))
            http_badresponse3['content-type'] = 'text/plain'
            http_badresponse3.status_code = 503
            http_badresponse3.reason_phrase = ' please login first !'
            return http_badresponse3

    # post request (ok)
    else:
        payload = {'request problem': 'need POST request '}
        http_badresponse = HttpResponse(json.dumps(payload))
        http_badresponse['content-type'] = 'text/plain'
        http_badresponse.status_code = 404
        http_badresponse.reason_phrase = 'need POST request'
        return http_badresponse
