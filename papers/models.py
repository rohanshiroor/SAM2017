from django.core.exceptions import PermissionDenied
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from datetime import datetime
from django.db.models.query_utils import Q


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=self.normalize_email(username),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **kwargs):
        user = self.model(
            username=username,
            is_staff=True,
            is_superuser=True,
            is_active=True,
            is_admin=True,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(verbose_name='email address', max_length=255, unique=True,null=False)
    first_name = models.CharField(verbose_name='first name',max_length=30,unique=False,null=False)
    last_name = models.CharField(verbose_name='last name',max_length=30,unique=False,null=True)
    street_line_1 = models.CharField(verbose_name='street_line_1', max_length=30)
    street_line_2 = models.CharField(verbose_name='street_line_2', max_length=30)
    city = models.CharField(verbose_name='city', max_length=30)
    state = models.CharField(verbose_name='state', max_length=30)
    zip_code = models.IntegerField()
    phone_number = models.CharField(verbose_name='phone number', blank=True, max_length=15)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    AUTHOR = 0
    PCM = 1
    PCC = 2
    ADMIN = 3
    UserTypes = (
        (AUTHOR, "Author"),
        (PCM, "PCM"),
        (PCC, "PCC"),
        (ADMIN, "Admin"),
        )
    user_type = models.IntegerField(choices=UserTypes, default=AUTHOR)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_address(self):
        return self.street_line_1 + ", " + self.street_line_2 + ", " + self.city + ", " + \
            self.state + ", " + str(self.zip_code)

    def get_full_name(self):
        # The user is identified by their email address
        return self.username

    def get_short_name(self):
        # The user is identified by their email address
        return self.username

    def __str__(self):  # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Author(CustomUser):
    def get_author(request):
        return Author.objects.get(customuser_ptr_id=request.user.id)

    def update_user(user_id, new_user):
        users = Author.objects.filter(customuser_ptr_id=user_id)
        users.update(first_name=new_user.first_name, last_name=new_user.last_name,
                     street_line_1=new_user.street_line_1,
                     street_line_2=new_user.street_line_2, city=new_user.city, state=new_user.state,
                     zip_code=new_user.zip_code,
                     phone_number=new_user.phone_number)

    def __str__(self):
        return self.first_name + " " + self.last_name


class PCM(Author):
    def update_user(user_id, new_user):
        users = PCM.objects.filter(author_ptr_id=user_id)
        users.update(first_name=new_user.first_name, last_name=new_user.last_name,  street_line_1=new_user.street_line_1,
                     street_line_2=new_user.street_line_2,  city=new_user.city, state=new_user.state, zip_code=new_user.zip_code, phone_number=new_user.phone_number)


class PCC(CustomUser):
    pass


class Admin(CustomUser):
    pass


def concat_media_path(instance, filename):
    return 'paper/userId_' + \
           str(instance.ownedBy.id) + \
           '/paper_' + \
           str(instance.pk) + \
           '.' + filename.split('.')[-1]


class Paper(models.Model):
    file = models.FileField(null=False, blank=False, upload_to=concat_media_path)
    title = models.CharField(verbose_name='title', max_length=255,null=False)
    abstract = models.TextField(verbose_name='abstract', max_length=1000,unique=False,null=True,blank=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="author")
    submission_date = models.DateTimeField(editable=False)
    version = models.IntegerField(null=False, blank=False, unique=False, default=1)
    pcm_one = models.ForeignKey(PCM, related_name="FirstPCM_Assigned", null=True, blank=True)
    pcm_two = models.ForeignKey(PCM, related_name="SecondPCM_Assigned", null=True, blank=True)
    pcm_three = models.ForeignKey(PCM, related_name="ThirdPCM_Assigned", null=True, blank=True)
    rate = models.IntegerField(verbose_name="rating", null=True, blank=True,validators=[MinValueValidator(1), MaxValueValidator(5)])



    class Meta:
        unique_together = ['title', 'author', 'version']

    def save(self, *args, **kwargs):
        self.submission_date = datetime.now()
        return super(Paper, self).save(*args, **kwargs)

    def update_paper(paper_id, new_paper):
        papers = Paper.objects.filter(id=paper_id)
        papers.update(title=new_paper.title, abstract=new_paper.abstract, version=new_paper.version,
                      file=new_paper.file, submission_date=datetime.now())

    def get_papers(user_id):
        papers = Paper.objects.filter(author_id=user_id).order_by('-submission_date')
        for paper in papers:
            paper.state = "inactive"
        return papers

    def get_paper_for_review(pcm, paper_id):
        query = Q(pcm_one=pcm) | Q(pcm_two=pcm) | Q(pcm_three=pcm)
        paper = Paper.objects.get(Q(id=paper_id) & query)
        return paper

    def get_paper(paper_id, papers=None):
        if papers:
            for paper in papers:
                if paper.id == paper_id:
                    paper.state = "active"
                    return paper
        return Paper.objects.get(id=paper_id)

    def get_assigned_papers(pcm):
        papers = Paper.objects.filter(Q(pcm_one=pcm) | Q(pcm_two=pcm) | Q(pcm_three=pcm)).order_by('submission_date')
        for paper in papers:
            paper.state = "inactive"
        return papers

    def other_papers(pcm, paper_id=None):
        papers = Paper.objects.filter(~Q(author=pcm))
        for paper in papers:
            paper.state = "inactive"
        return papers

    def choosing_paper(paper_id, papers=None):
        for paper in papers:
            if paper.id == int(paper_id):
                paper.state = "active"
                return paper
        raise PermissionDenied()


class PaperAuthors(models.Model):
    paper = models.ForeignKey(Paper, null=False)
    author = models.ForeignKey(Author, null=False)

    class Meta:
        unique_together = ('paper', 'author')


class PaperRequests(models.Model):
    paper = models.ForeignKey(Paper, null=False, unique=True)
    pcm = models.ForeignKey(CustomUser, null=False)

    class Meta:
        unique_together=("paper", "pcm")

    def is_paper_requested(paper, pcm):
        return PaperRequests.objects.filter(Q(paper=paper) & Q(pcm=pcm)).exists()


class Reviews(models.Model):
    paper = models.ForeignKey(Paper, null=False, blank=False)
    reviewer = models.ForeignKey(CustomUser, verbose_name="reviewer", null=False)
    comment = models.CharField(verbose_name="comment", max_length=2000, null=False, blank=False)
    rate = models.IntegerField(verbose_name="rating", null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = ('paper', 'reviewer')

    def update_review(review):
        reviews = Reviews.objects.filter(paper=review.paper_id, reviewer=review.reviewer)
        reviews.update_or_create(paper=reviews.paper, reviewer=reviews.reviewer, comment=review.comment, rate=review.rate)


class PaperAssigned(models.Model):
    paper=models.ForeignKey(Paper, null=False)

    def assign_papers(self):
        paper= Paper.objects.all()
        pcm=PCM.objects.all()
        pcm_interested = PaperRequests.is_paper_requested(paper, pcm)
        other_pcm = PCM.objects.filter(~Q(author=pcm))
        all_pcm = pcm_interested + list(set(other_pcm) - set(pcm_interested))
        return all_pcm

