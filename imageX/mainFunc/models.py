from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name

class Member(models.Model):
    usr = models.OneToOneField(User, on_delete=models.CASCADE, null=True, unique=True)
    #email = models.EmailField()
    description = models.TextField(default='Hello there I am using ImageX!')
    avatar = models.ImageField(upload_to='userAvatar',blank=True,null=True)
    dailyUploadCount = models.IntegerField()
    totalUploadCount = models.IntegerField()

    def check_quota(self):
        DAILY_UPLOAD_QUOTA = 3
        TOTAL_UPLOAD_QUOTA = 4
        return (self.dailyUploadCount < DAILY_UPLOAD_QUOTA and self.totalUploadCount < TOTAL_UPLOAD_QUOTA)

    def exceed_daily_quota(self):
        DAILY_UPLOAD_QUOTA = 3
        return (self.dailyUploadCount >= DAILY_UPLOAD_QUOTA)

    def exceed_total_quota(self):
        TOTAL_UPLOAD_QUOTA = 4
        return (self.totalUploadCount >= TOTAL_UPLOAD_QUOTA)

    def increment_counts(self):
        self.dailyUploadCount += 1
        self.totalUploadCount += 1
        self.save()

    def reset_counts(self):
        self.dailyUploadCount = 0
        self.totalUploadCount = 0
        self.save()


    def __str__(self):
        return self.usr.username

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Photo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='Add photo description here.')
    imageFile = models.ImageField(upload_to='userImg', null=True)
    uploadTime = models.DateTimeField(default=timezone.now)
    uploadBy = models.ForeignKey(Member, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(Tag)
    # this function add tags to the photo
    def associate_tag(self, tag_info):
        MAX_TAG_NUMBER = 10
        tagList = tag_info.split()
        if len(tagList) + self.tag.count() > MAX_TAG_NUMBER:
            return False
        else:
            for tag in tagList:
                if Tag.objects.filter(name=tag).exists():
                    tmp_tag = Tag.objects.get(name=tag)
                    self.tag.add(tmp_tag)
                else:
                    tmp_tag = Tag.objects.create(name=tag)
                    self.tag.add(tmp_tag)
        return True
    def __str__(self):
        return self.title


def matchAndSort(keyword="None",filter="None",sortBy="None"):
    '''
    to start a search for photos, support search gallery in the later version
    input: searching keyword, search category, sorting condition
    output: list of matched Photo objects
    '''
    print ("----------------------------------")
    print ("filter: ", filter, "val= ", filter == "None")
    print ("sortBy: ", sortBy, "val= ", sortBy == "None")
    print ("----------------------------------")
    if keyword == "None":
        #print ("matched: all photo")
        matched = Photo.objects.all()
    else:
        keyword= keyword.split()
        matched = Photo.objects.all()
        #print ("selected search, kw=", keyword)
        #split keywords by space bar
        print (keyword)
        for kw in keyword:
            matched = matched.filter(tag__name__contains = kw)
    if filter == "None":
        #print ("hello")
        pass
    else:
        matched = matched.filter(category__name__iexact=filter)
    if sortBy != "None":
        matched = sortResult(matched, sortBy)
    return matched

def sortResult(photoObj,sortBy):
    if sortBy == "sort_1":
        print ("Sorting now")
        return photoObj.order_by('uploadTime')[::-1]
    else:
        return photoObj
