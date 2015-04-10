import logging
from pygithub3 import Github

from django.conf import settings
from github_log.models import ErrorLog


class GitHubIssueHandler(logging.Handler):
    """Register error as an github issue"""

    def emit(self, record):
        log, is_created = ErrorLog.create_from_record(record)
        gitlog_settings = settings.GITLOG_SETTINGS
        github = Github(user=gitlog_settings['USER'], repo=gitlog_settings['REPO'], token=gitlog_settings['TOKEN'])
        if log.signature.issue_number:
            issue = github.issues.get(log.signature.issue_number)
            if issue.state != 'open':
                issue.update(data=dict(status='open'))
            github.issues.comments.create(log.signature.issue_number, log.body)
        else:
            issue = github.issues.create(dict(title=log.title, body=log.body))
            log.signature.issue_number = issue.number
            log.signature.save()
