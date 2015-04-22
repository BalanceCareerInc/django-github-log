import logging

from github_log.tasks import shoot_to_github


class GitHubIssueHandler(logging.Handler):
    """Register error as an github issue"""

    def emit(self, record):
        from github_log.models import ErrorLog
        log = ErrorLog.create_from_record(record)
        shoot_to_github.delay(log)
