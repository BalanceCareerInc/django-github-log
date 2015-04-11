# django-github-log
Create an issue on github when django raise error

## Installation
Add following settings dictionary in your settings.py (LABELS is optional)
```python
GITHUB_LOG_SETTINGS = {
    'USER': 'REPOSITORY-OWNER',
    'REPO': 'REPOSITORY-NAME',
    'TOKEN': 'GITHUB-API-TOKEN',
    'LABELS': [
        'priority:normal',
        'status:done',
    ]
}
```

And in Logging['handlers'], add
```python
'github': {
    'level': 'ERROR',
    'class': 'github_log.log.GitHubIssueHandler'
},
```
