Contributing to QUADS
=====================

## Contribution Basics
  - You can use the ```testing/quads-sandbox.sh``` tool to create a local sandbox for testing and development.
  - We use [Gerrit](https://review.gerrithub.io/q/project:redhat-performance%252Fquads) for code review
  - You can also find us on IRC at **#quads** on ```irc.freenode.net```

## How to Contribute
The QUADS project welcomes contributions from everyone!  Please read the below steps to see how you can contribute to QUADS.

### Clone our repository

```
git clone https://github.com/redhat-performance/quads
```

### Create a Tracking Issue
* Create a [Github issue](https://github.com/redhat-performance/quads/issues/new) to track your work.
  - Provide a meaningful explanation, citing code lines when relevant.
  - Explain what you are trying to fix, or what you're trying to contribute.


### Setup Github / Gerrit Account
* You'll need a Github account to proceed.
* Setup username/email for Github and Gerrithub (one time only):
  - Ensure Github and Gerrithub are linked by [signing into Gerrithub via Github](https://review.gerrithub.io/login)
  - match ```gitreview.username``` to your Github username
  - match ```user.name``` to your real name or how you want credit for commits to display in Git history.
  - match ```user.email``` to your email address associated with Github.


* Setup Inside Cloned QUADS Repo
  - Setup your username, email address as needed
  - Set your `gitreview.username`
```
git config user.email "venril@karnors-castle.com"
git config user.name "Venril Sathir"
git config --add gitreview.username "vsathir"
```

### Start Hacking
* Make any changes you'd like to your repository, this may be easier by using a new branch.

```
cd quads
git branch my_change
git checkout my_change
vi lib/Quads.py
```
### Make a Commit, Submit Review
* Add a local commit with a meaningful, short title followed by a space and a summary (you can check our [commit history](https://github.com/redhat-performance/quads/commits/master) for examples.
* Add a line that relates to a new or existing github issue, e.g. ```fixes: https://github.com/redhat-performance/quads/issues/5``` or ```related-to: https://github.com/redhat-performance/quads/issues/25```


```
git add lib/Quads.py
git commit
```
#### Integrate Git Review (First Time Only)
* Install git-review and run it for first time.

```
yum install git-review
git review -s
```

* Now submit your patchset with git review (future patches you only need to run ```git review```)
  - A Change-ID will be generated when you create your first patchset, make sure this is the last line in the commit message preceded by an empty line.

```
git review
```

* If you want to make changes to your patchset you can run the ```git commit --amend``` command.

```
vi lib/Quads.py
git commit --amend
git review
```

### Monitor your Patchset Lifecycle
* Keep an eye on your patchset in Gerrithub, this is where CI will run, where we'll provide feedback and where you can monitor changes and status.  Your git review command will print the correct URL to your patchset.

### Continuous Integration (CI)
Jenkins CI pipeline currently checks the following for every submitted patchset:
  - shellcheck - checks for common shell syntax errors and issues
  - flake8 - checks Python tools for common syntax errors and issues
  - quads sandbox test - instantiates a full QUADS in containers and runs common QUADS operations with fake data
    * We currently do not expose CI logs externally, please reply on your patchset comments if you'd like a paste of it.
  - You can trigger CI to run again by commenting on your patchset in gerrit with `retrigger`

#### QUADS CI Architecture

![quads-ci](/image/quads-ci.png?raw=true)

