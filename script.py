"""
Taken from nashmaniac/create-issue-action
"""

import os
import github

# extracting all the input from environments
title = os.environ['INPUT_TITLE']
token = os.environ['INPUT_TOKEN']
labels = os.environ['INPUT_LABELS']
assignees = os.environ['INPUT_ASSIGNEES']
body = os.environ['INPUT_BODY']
results_file = os.environ['INPUT_RESULTS']
should_close = os.environ['INPUT_SHOULD_CLOSE'] == 'true'

# as I said GitHub expects labels and assignees as list but we supplied as string in yaml as list are not supposed in
# .yaml format
if labels and labels != '':
    labels = labels.replace(" ", "").split(',')  # splitting by , to make a list
else:
    labels = []  # setting empty list if we get labels as '' or None

if assignees and assignees != '':
    assignees = assignees.split(',')  # splitting by , to make a list
else:
    assignees = []  # setting empty list if we get labels as '' or None

if not body:
    if results_file:
        with open(os.path.join(os.getcwd(), results_file)) as f:
            body = "".join(f.readlines())
github = github.Github(token)
# GITHUB_REPOSITORY is the repo name in owner/name format in Github Workflow
repo = github.get_repo(os.environ['GITHUB_REPOSITORY'])

if len(body) >= 65536:
    body = body[:65490] + "\n... (See pylint workflow for rest of errors)"

issues = repo.get_issues(state="open", labels=labels)
existing_issue = False
for issue in issues:
    if issue.title == title:
        if should_close:
            issue.edit(state='close')
        else:
            assignees += issue.assignees
            issue.edit(body=body, assignees=assignees)
        existing_issue = True
        break

if not existing_issue and not should_close:
    issue = repo.create_issue(
        title=title,
        body=body,
        assignees=assignees,
        labels=labels
    )
