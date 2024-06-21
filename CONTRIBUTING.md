[![Gerrit](https://quads-ci.scalelab.redhat.com/job/Quads-2.0/badge/icon)](https://quads-ci.scalelab.redhat.com/job/Quads-2.0/)

Contributing to QUADS
=====================

## How to Contribute
The QUADS project welcomes contributions from everyone!  Please read the below steps to see how you can contribute to QUADS.

## Contribution Basics
  * We do not use the Github Pull Request system.
  * We use [Gerrit](https://review.gerrithub.io/q/project:redhat-performance%252Fquads) for code review
  * You can also find us on IRC at **#quads** on ```irc.libera.chat``` [webchat](https://web.libera.chat/?channels=#quads)

### QUADS Development Setup
  - Clone `latest` branch for latest.

```
git clone --single-branch --branch latest https://github.com/redhat-performance/quads /opt/container/quads/
```

  - Change directory to the code and create your own branch to work
```
cd /opt/container/quads/container
git branch name_of_change
git checkout !$
```

#### Podman on Linux or a Linux VM

  - Instantiate the QUADS containers

```
podman-compose -f /opt/container/quads/container/container-compose.yml up
```
  - This will not background the podman orchestration, so open other terminals to work.
  - You can now test locally, it's useful to set a bashrc alias for the `/usr/bin/quads` commmand

```
echo 'alias quads="podman exec -it quads /usr/bin/quads"' >> ~/.bashrc
```

#### MAC OSX Specific

  - Make the directory structure for your mapped database data
```
mkdir -p /opt/container/quads/container/{data_db,wiki_db,wordpress_data}
```
  - Instantiate the podman compose
```
podman compose -f /opt/container/quads/container/container-compose-osx.yml up
```
  - If you're using Docker on Mac OSX you may want to switch to the [overlay2 driver](https://stackoverflow.com/questions/39455764/change-storage-driver-for-docker-on-os-x#39737553)  This is not strictly a requirement but can significantly improve performance on a Mac for the local driver.  For more details see this [article](https://markshust.com/2017/03/02/making-docker-mac-faster-overlay2-filesystem/).  Local driver mapped content is stored in ~/Library/Containers/com.docker.docker/Data/vms/0/ in a disk image.

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
vim src/quads/web/app.py
```

#### Reloading Environment after Changes
* Since we're using containers, any changes you make in the checked out repo and local branch in `/opt/container/quads` can be reloaded via Podman.

```
podman-compose -f container-compose.yml down
```

* Now bring it up again with your new code since the `/opt/container/quads` volume is mapped.

```
podman-compose -f container-compose.yml up -d
```

### Make a Commit, Submit Review
* Add a local commit with a meaningful, short title followed by a space and a summary (you can check our [commit history](https://github.com/redhat-performance/quads/commits/latest) for examples.
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

* If you are adding new functionality or methods you'll need to also include unit tests or CI will get upset.

#### Managing Git Review Patchsets

* If you want to make changes to your patchset you can run the ```git commit --amend``` command.

```
vim /src/quads/quads_api.py
git commit --amend
git review
```

* If you just want to checkout an existing patchset in Gerrit you can use the `git review -d $CHANGEID` command.

```
cd /opt/container/quads
git review -d $CHANGEID
```

### Monitor your Patchset Lifecycle
* Keep an eye on your patchset in Gerrithub, this is where CI will run, where we'll provide feedback and where you can monitor changes and status.  Your git review command will print the correct URL to your patchset.

### Continuous Integration (CI)
Jenkins CI pipeline currently checks the following for every submitted patchset:
  - shellcheck - checks for common shell syntax errors and issues
  - flake8 - checks Python tools for common syntax errors and issues
  - [unit tests](https://github.com/redhat-performance/quads/tree/latest/tests)
  - You can trigger CI to run again by commenting on your patchset in gerrit with `retrigger`

#### QUADS CI Architecture

![quads-ci](/image/quads-ci.png?raw=true)

