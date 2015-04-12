# django-github-log
Create an issue group by error on github when django raises error

## Installation
1. Add following settings dictionary in your settings.py (LABELS is optional)

    ```python
    GITHUB_LOG_SETTINGS = {
        'USER': 'REPOSITORY-OWNER',
        'REPO': 'REPOSITORY-NAME',
        'TOKEN': 'GITHUB-API-TOKEN',
        'LABELS': [
            'priority:normal',
            'type:error',
            ...
        ]
    }
    ```
    
2. Add "github_log" in INSTALLED_APPS
3. Add logging handler in settings.Logging['handlers']

    ```python
    'github': {
        'level': 'ERROR',
        'class': 'github_log.log.GitHubIssueHandler'
    },
    ```
    
4. ``python manage.py syncdb``
