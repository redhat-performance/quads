Contributing to QUADS
=====================

## How to Contribute
The QUADS project welcomes contributions from everyone!  Please read the below steps to see how you can contribute to QUADS.

## Contribution Basics
  * We use [Gerrit](https://review.gerrithub.io/q/project:redhat-performance%252Fquads) for code review
  * You can also find us on IRC at **#quads** on ```irc.freenode.net```

### QUADS Development Setup
  - Clone `master` branch for latest, or a specific release branch e.g. `1.1`

```
git clone --single-branch --branch master https://github.com/redhat-performance/quads /opt/docker/quads/
```

  - Change directory to the code and create your own branch to work
```
cd quads/docker
git branch yourname_change
git checkout !$
```

  - Instantiate the QUADS containers

```
docker-compose -f docker-compose.yml up
```
  - This will not background the docker orchestration, so open other terminals to work.
  - You can now test locally, it's useful to set a bashrc alias for the `bin/quads-cli` commmand

```
echo 'alias quads="docker exec -it quads bin/quads-cli"' >> ~/.bashrc
```

### Create a Tracking Issue
* Create a [Github issue](https://github.com/redhat-performance/quads/issues/new) to track your work.
  - Provide a meaningful explanation, citing code lines when relevant.
  - Explain what you are trying to fix, or what you're trying to contribute.

### Setup Github / Gerrit Account (one-time only)
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
* Make any changes you'd like to your repository.

```
cd quads
git branch my_change
git checkout my_change
vi lib/Quads.py
```

#### Reloading Environment after Changes
* Since we're using containers, any changes you make in the checked out repo and local branch in `/opt/docker/quads` can be reloaded via Docker.

```
docker-compose -f docker-compose.yml down
```

* Now bring it up again with your new code since the `/opt/docker/quads` volume is mapped.

```
docker-compose -f docker-compose.yml up -d
```

### Make a Commit, Submit Review
* Add a local commit with a meaningful, short title followed by a space and a summary (you can check our [commit history](https://github.com/redhat-performance/quads/commits/master) for examples.
* Add a line that relates to a new or existing github issue, e.g. ```fixes: https://github.com/redhat-performance/quads/issues/5``` or ```related-to: https://github.com/redhat-performance/quads/issues/25```


```
git add quads/api_v2.py
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

#### Managing Git Review Patchsets

* If you want to make changes to your patchset you can run the ```git commit --amend``` command.

```
vi quads/api_v2.py
git commit --amend
git review
```

* If you just want to checkout an existing patchset in Gerrit you can use the `git review -d $CHANGEID` command.

```
cd /opt/docker/quads
git review -d $CHANGEID
```

### Monitor your Patchset Lifecycle
* Keep an eye on your patchset in Gerrithub, this is where CI will run, where we'll provide feedback and where you can monitor changes and status.  Your git review command will print the correct URL to your patchset.

### Continuous Integration (CI)
Jenkins CI pipeline currently checks the following for every submitted patchset:
  - shellcheck - checks for common shell syntax errors and issues
  - flake8 - checks Python tools for common syntax errors and issues
  - You can trigger CI to run again by commenting on your patchset in gerrit with `retrigger`

#### QUADS CI Architecture

![quads-ci](/image/quads-ci.png?raw=true)

