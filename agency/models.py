from django.db import models
import datetime
import numpy as np
from django.utils import timezone
from django import forms


class Author(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    def __str__(self):
        return self.username




class Story(models.Model):
    # 避免重复 ok
    story_headline = models.CharField(max_length=64,unique = True)
    story_details = models.CharField(max_length=512,unique = True)
    story_category = models.CharField(max_length=64)
    # uk, eu (for European news), or w (for world
    # news)
    story_region = models.CharField(max_length=64)
    # (("tech","tech"),("art","art"),("pol","'pol'"),("trivia","trivia"))
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    unique_key = models.AutoField(auto_created=True, primary_key=True, serialize=False)

    # 都不行 ：
    # 自动产生时间产生时间
    # 1 no
    # created_time = models.DateField(auto_now_add=True)
    # 2 no
    # created_time = models.DateTimeField( default = timezone.now)

    # 3 django site 上可以看到

    # created_time = models.DateTimeField(auto_created = True,default=timezone.now)
    # 4 ok

    story_date = models.DateTimeField(auto_now_add=True)

    # 5 no

    # created_time =  models.DateTimeField()

    #n 6 改setting USE_TZ=False no

    # created_time = models.DateTimeField(auto_created = True )

    #
 #   def get_key(self.unique_key): no

      # return "<Story:unique_key= %s story_headline=%s %s %s %s %s %s >" % (self.unique_key ,self.story_headline ,self.story_category ,self.story_region ,self.author ,self.story_date ,self.story_details)
       # return np.array ([ [self.unique_key], [self.story_headline] ]) no
# % self.unique_key %self.story_headline % self.story_category %self.story_region %self.author %self.story_date %self.story_details
   # def __str__(self):
   #     return self.unique_key no
    # def get(self): # no
     #   return self.unique_key ,self.story_headline
 #query_list = Story.objects.values('unique_key','story_headline')


#def get_type(self):
       # return self.unique_key ,self.story_headline
    @staticmethod
    def get1(date,cat,reg):
        stories = [0,1,2,3,4,5,6]

        stories[2] = Story.objects.values('story_category').filter(story_date__range=[date, "2019-03-31"],story_category=cat, story_region=reg)
        stories[0] = Story.objects.values('story_headline').filter(story_date__range=[date, "2019-03-31"], story_category=cat, story_region=reg)
        stories[1] = Story.objects.values('unique_key').filter(story_date__range=[date, "2019-03-31"],story_category=cat, story_region=reg)
        stories[3] = Story.objects.values('story_region').filter(story_date__range=[date, "2019-03-31"],story_category=cat, story_region=reg)
        stories[4] = Story.objects.values('author').filter(story_date__range=[date, "2019-03-31"],story_category=cat, story_region=reg)
        stories[5] = Story.objects.values('story_date').filter(story_date__range=[date, "2019-03-31"],story_category=cat, story_region=reg)
        stories[6] = Story.objects.values('story_details').filter(story_date__range=[date, "2019-03-31"], story_category=cat,story_region=reg)

        # 一定要加 不然显示不出来
        b = np.array(stories)
        return b

    @staticmethod
    def get2(date, reg):
        stories = [0, 1, 2, 3, 4, 5, 6]

      #  stories[2] = np.array(Story.objects.values('story_category').filter(story_date__range=[date, "2019-03-31"],story_region=reg) )
        stories[2] = Story.objects.values('story_category').filter(story_date__range=[date, "2019-03-31"], story_region=reg)
        stories[0] = Story.objects.values('story_headline').filter(story_date__range=[date, "2019-03-31"], story_region=reg)
        stories[1] = Story.objects.values('unique_key').filter(story_date__range=[date, "2019-03-31"],story_region=reg)
        stories[3] = Story.objects.values('story_region').filter(story_date__range=[date, "2019-03-31"], story_region=reg)
        stories[4] = Story.objects.values('author').filter(story_date__range=[date, "2019-03-31"], story_region=reg)
        stories[5] = Story.objects.values('story_date').filter(story_date__range=[date, "2019-03-31"], story_region=reg)
        stories[6] = Story.objects.values('story_details').filter(story_date__range=[date, "2019-03-31"], story_region=reg)

        # 一定要加 不然显示不出来
        b = np.array(stories)
        return b

    @staticmethod
    def get3(date, cat):
        stories = [0, 1, 2, 3, 4, 5, 6]

        #  stories[2] = np.array(Story.objects.values('story_category').filter(story_date__range=[date, "2019-03-31"],story_region=reg) )
        stories[2] = Story.objects.values('story_category').filter(story_date__range=[date, "2019-03-31"],story_category=cat)
        stories[0] = Story.objects.values('story_headline').filter(story_date__range=[date, "2019-03-31"],story_category=cat)
        stories[1] = Story.objects.values('unique_key').filter(story_date__range=[date, "2019-03-31"], story_category=cat)
        stories[3] = Story.objects.values('story_region').filter(story_date__range=[date, "2019-03-31"],story_category=cat)
        stories[4] = Story.objects.values('author').filter(story_date__range=[date, "2019-03-31"], story_category=cat)
        stories[5] = Story.objects.values('story_date').filter(story_date__range=[date, "2019-03-31"],story_category=cat)
        stories[6] = Story.objects.values('story_details').filter(story_date__range=[date, "2019-03-31"],story_category=cat)

        # 一定要加 不然显示不出来
        b = np.array(stories)
        return b

    @staticmethod
    def get4(date):
        stories = [0, 1, 2, 3, 4, 5, 6]
        #  stories[2] = np.array(Story.objects.values('story_category').filter(story_date__range=[date, "2019-03-31"],story_region=reg) )
        stories[2] = Story.objects.values('story_category').filter(story_date__range=[date, "2019-03-31"])
        stories[0] = Story.objects.values('story_headline').filter(story_date__range=[date, "2019-03-31"])
        stories[1] = Story.objects.values('unique_key').filter(story_date__range=[date, "2019-03-31"])
        stories[3] = Story.objects.values('story_region').filter(story_date__range=[date, "2019-03-31"])
        stories[4] = Story.objects.values('author').filter(story_date__range=[date, "2019-03-31"] )
        stories[6] = Story.objects.values('story_details').filter(story_date__range=[date, "2019-03-31"] )

        # 一定要加 不然显示不出来
        b = np.array(stories)
        return b