import os
import linecache

from hashlib import sha256

from django.conf import settings
from django.db import models
import json


class Request(models.Model):
    path = models.CharField(max_length=255)
    get_json = models.TextField()
    post_json = models.TextField()
    cookies_json = models.TextField()
    meta_json = models.TextField()

    def __str__(self):
        pass

    @classmethod
    def create_from_request(cls, request):
        meta_dict = dict((k, v) for k, v in request.META.iteritems() if k.startswith('HTTP_'))
        return cls.objects.create(
            path=request.META['PATH_INFO'].split('?')[0],
            get_json=json.dumps(request.GET),
            post_json=json.dumps(request.POST),
            cookies_json=json.dumps(request.COOKIES),
            meta_json=json.dumps(meta_dict)
        )


class Signature(models.Model):
    hash = models.CharField(max_length=64, unique=True)
    file_name = models.CharField(max_length=255)
    line = models.CharField(max_length=255)
    line_number = models.IntegerField()
    issue_number = models.IntegerField(null=True)

    def __repr__(self):
        return '<Signature: "%s">' % str(self)

    def __str__(self):
        return self.make_string(self.file_name, self.line)

    @staticmethod
    def make_string(file_name, line):
        return '%s#%s' % (file_name, line)

    @classmethod
    def get_or_create_from_frame(cls, error_frame):
        error_frame = get_error_frame(error_frame)
        file_name = error_frame.f_code.co_filename
        line_number = error_frame.f_lineno
        line = linecache.getline(file_name, line_number).strip()
        short_file_name = file_name[len(os.getcwd()):]
        hash_ = sha256(cls.make_string(short_file_name, line)).hexdigest()
        return cls.objects.get_or_create(hash=hash_, defaults=dict(file_name=short_file_name, line=line, line_number=line_number))


class ErrorLog(models.Model):
    type = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    signature = models.ForeignKey(Signature)
    request = models.OneToOneField(Request)
    stack_trace = models.TextField()
    logged_at = models.DateTimeField(auto_now_add=True)

    @property
    def title(self):
        return '%s: %s' % (self.type, self.message)

    @property
    def body(self):
        return '''## Error Info
Error on %(filename)s:%(line_no)d
%(line)s
```
%(stack_trace)s
```
## Request Info
```
%(request)s
```
Logged at: %(logged_at)s''' % dict(
            filename=self.signature.file_name,
            line_no=self.signature.line_number,
            line=self.signature.line,
            stack_trace=self.stack_trace,
            logged_at=self.logged_at,
            request=str(self.request)
        )

    @classmethod
    def create_from_record(cls, record):
        signature, is_created = Signature.get_or_create_from_frame(record.exc_info[2])
        log = cls.objects.create(
            type=record.exc_info[0].__name__,
            message=str(record.exc_info[1]),
            signature=signature,
            request=Request.create_from_request(record.request),
            stack_trace=record.exc_text
        )
        return log, is_created


def get_error_frame(initial_tb):
    def is_controllable(tb):
        filename = tb.tb_frame.f_code.co_filename
        for app_name in settings.INSTALLED_APPS:
            expected_path = os.path.join(os.getcwd(), app_name.replace('.', os.path.sep))
            if os.path.exists(expected_path) and filename.startswith(expected_path):
                return True
        return False

    current_tb = initial_tb
    while current_tb.tb_next and is_controllable(current_tb.tb_next):
        current_tb = current_tb.tb_next

    return current_tb.tb_frame
