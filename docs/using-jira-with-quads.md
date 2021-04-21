
Using Optional JIRA Library and Tools
======================================

Internally we use the [JIRA](https://www.atlassian.com/software/jira) as is
common with a lot of development/devops organizations.  To this end we are
providing some tools and libraries within QUADS with the hope it's useful to
others.

![jira](../image/jira.jpg?raw=true)
  * [Requirements for JIRA QUADS Automation](#requirements-for-jira-quads-automation)
  * [Perfoming API Activities with jira.py](#API-activities-with-jira.py)
  * [Applying Labels and Adding Watchers](#applying-labels-and-adding-watchers)
  * [Common JIRA Labels](#common-jira-labels)
## Requirement for JIRA QUADS automation
  * JIRA API user with admin capability for your JIRA project.
  * Placing JIRA credentials in `/opt/quads/conf/quads.yml`
```
ticket_url: https://projects.engineering.example.com/browse
# (optional ticket queue name) this is typically the ticket queue
# name or abbreviation in the case of JIRA
ticket_queue: SCALELAB
# Jira Specific Variables
jira_url: https://projects.engineering.example.com/rest/api/2
jira_username: admin
jira_password: password
```

## API activities with jira.py
  * Library: `/opt/quads/quads/tools/jira.py`
  * The `jira.py` library in QUADS helps with auto-updating JIRA tickets using the API user.
  * If you are using `--host-list` for en-masse scheduling this will be called to update the
    ticket template found in `/opt/quads/quads/templates/jira_ticket_assignment`

## Applying labels and adding watchers
  * Tool: `/opt/quads/quads/tools/jira_watchers.py`
  * The `jira_watchers.py` tool will assist you with ad-hoc (perhaps run out of cron or systemd timer)
    batch processing to do the following:
    * Ensure the person submitting the request is added as a _watcher_ in JIRA
    * Checking the viability of extension request with appropriate labels, e.g. `CAN_EXTEND` or `CANNOT_EXTEND`
  * Below is a reference of how we use labels in JIRA.

## Common JIRA Labels
  * Below is a chart of common labels we use in JIRA with `jira.py` managing/automating this aspect of
    our request workflow.

| Label Name       |Category    | Purpose of Label                                                |
|------------------|------------|-----------------------------------------------------------------|
| EXTENSION        |  Assignment| Label for existing assignment extension                         |
| EXPANSION        |  Assignment| Request for expansion of existing assignment                    |
| CAN_EXTEND       |  Viability | Label indicating assignment could be extended with no conflicts |
| CANNOT_EXTEND    |  Viability | Label indicating a conflict in at least one system for extension|

