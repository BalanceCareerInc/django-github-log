from celery import shared_task
from django.conf import settings

from pygithub3 import Github


@shared_task
def shoot_to_github(error_log):
    gitlog_settings = settings.GITHUB_LOG_SETTINGS
    github = Github(user=gitlog_settings['USER'], repo=gitlog_settings['REPO'], token=gitlog_settings['TOKEN'])
    if error_log.signature.issue_number:
        issue = github.issues.get(error_log.signature.issue_number)
        if issue.state != 'open':
            github.issues.update(issue.number, dict(state='open'))
        github.issues.comments.create(error_log.signature.issue_number, error_log.body)
    else:
        issue = github.issues.create(dict(
            title=error_log.title,
            body=error_log.body,
            labels=gitlog_settings.get('LABELS', [])
        ))
        error_log.signature.issue_number = issue.number
        error_log.signature.save()
