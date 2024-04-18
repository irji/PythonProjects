from redminelib import Redmine

redmine = Redmine('https://redmine.rfdyn.ru', key="401a6b058962fbd1063c570fb0a1f99361c7e9b3")
project = redmine.project.get('group-gui')

#issues = redmine.issue.filter(project_id='group-gui')
issues = redmine.issue.get("85258")

print(len(issues))
