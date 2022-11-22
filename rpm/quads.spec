#### NOTE: if building locally you may need to do the following:
####
#### yum install rpmdevtools -y
#### spectool -g -R rpm/quads.spec
####
#### At this point you can use rpmbuild -ba quads.spec
#### (this is because our Source0 is a remote Github location
####
#### Our upstream repository is located here:
#### https://copr.fedorainfracloud.org/coprs/quadsdev/QUADS
####
#### Note: quads-dev = latest master branch
####       quads     = latest stable release

%define name quads-dev
%define reponame quads
%define version 1.1.6
%define build_timestamp %{lua: print(os.date("%Y%m%d"))}

Summary: Automated future scheduling, documentation, end-to-end provisioning and assignment of servers and networks.
Name: %{name}
Version: %{version}
Release: %{build_timestamp}
Source0: https://github.com/redhat-performance/quads/archive/master.tar.gz#/%{name}-%{version}-%{release}.tar.gz
License: GPLv3
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: /opt/quads
BuildArch: noarch
Vendor: QUADS Project
Packager: QUADS Project
Requires: httpd >= 2.4
Requires: python3-mongoengine >= 0.8
Requires: python3-cherrypy >= 8.9
Requires: python3-jinja2 >= 2.0
Requires: python3-passlib >= 1.7
Requires: python3-PyYAML >= 3.0
Requires: python3-requests >= 2.0
Requires: python3-aiohttp >= 3.1
Requires: git >= 2.1
Requires: ipmitool >= 1.8.0
Requires: python3-paramiko >= 2.3
Requires: python3-flask >= 1.0
Requires: python3-flask-bootstrap >= 3.3.7.1
Requires: python3-flask-wtf >= 0.12
Requires: python3-wtforms >= 2.2.0
Requires: python3-wordpress-xmlrpc >= 2.2
Requires: python3-pexpect >= 4.2
Requires: python3-ipdb >= 0.10
Requires: python3-argcomplete >= 1.9.5
Requires: haveged >= 1.8
Requires: python3-GitPython >= 2.0
Requires: logrotate >= 3.0

Url: https://quads.dev

%description

Create and manage a date/time based schedule for machine allocations
Drive system provisioning and network switch changes based on workload assignment via external commands
Automated network and provisioning validation prior to delivering sets of machines/networks to users.
Provide user-views of bare-metal systems in Foreman.
Manage PDU power sockets for connected bare-metal systems.
Generates instackenv.json for each OpenStack environment.
Automatically generate documentation to illustrate current status, published to a Wordpress instance
 * Current system details
 * Current workloads and assignments
 * Current ownership and resource utilization links (grafana/collectd)
 * Total duration and time remaining in system assignments
Query scheduling data to determine future availability
Generates a monthly, auto-updated calendar of machine assignments
Generates a per-month visualization map for per-machine allocations to assignments.
RT (or similiar ticketing system) integration.
IRC bot and email notifications for new provisioning tasks and ones ending completion

%prep
%autosetup -n %{reponame}-master

%install
rm -rf %{buildroot}
mkdir %{buildroot}%{prefix} -p
mkdir %{buildroot}/etc/systemd/system/ -p
mkdir %{buildroot}/etc/profile.d/ -p
mkdir %{buildroot}/etc/logrotate.d/ -p
tar cf - bin quads/*.py quads/tools/*.py quads/cli/* quads/templates/* quads/*.py conf web | ( cd %{buildroot}%{prefix} ; tar xvpBf - )
cp -rf systemd/quads-server.service %{buildroot}/etc/systemd/system/
cp -rf systemd/quads-web.service %{buildroot}/etc/systemd/system/
cp -rf conf/logrotate_quads.conf %{buildroot}/etc/logrotate.d/
mkdir -p %{buildroot}/var/www/html/visual/
echo 'export PATH="/opt/quads/bin:$PATH"' > %{buildroot}/etc/profile.d/quads.sh
echo 'export PYTHONPATH="$PYTHONPATH:/opt/quads/"' >> %{buildroot}/etc/profile.d/quads.sh
echo 'export PYTHONPATH="$PYTHONPATH:/opt/quads/"' >> %{buildroot}/etc/profile.d/quads.sh
echo 'eval "$(register-python-argcomplete quads-cli)"' >> %{buildroot}/etc/profile.d/quads.sh
%clean
rm -rf %{buildroot}

%files
/etc/systemd/system/quads-web.service
/etc/systemd/system/quads-server.service
/etc/profile.d/quads.sh
/opt/quads/bin/*
/opt/quads/web/*
/opt/quads/web/templates/*
/opt/quads/quads/*
/opt/quads/quads/cli/*
/opt/quads/quads/tools/*
/opt/quads/quads/templates/*
/opt/quads/conf/logrotate_quads.conf
%config(noreplace) /opt/quads/conf/quads.yml
%config(noreplace) /opt/quads/conf/vlans.yml
%config(noreplace) /opt/quads/conf/hosts_metadata.yml
%config(noreplace) /opt/quads/conf/idrac_interfaces.yml
%config(noreplace) /etc/logrotate.d/logrotate_quads.conf

%post
/usr/bin/systemctl enable quads-server
/usr/bin/systemctl enable quads-web
/usr/bin/systemctl enable mongod
/usr/bin/systemctl enable httpd
/usr/bin/systemctl enable haveged
source /etc/profile.d/quads.sh

%preun
if [ "$1" -eq 0 ]; then
  /usr/bin/systemctl stop quads-server
  /usr/bin/systemctl disable quads-server
  /usr/bin/systemctl stop quads-web
  /usr/bin/systemctl disable quads-web
fi;
:;

%changelog

* Thu Feb 03 2022 Will Foster <wfoster@redhat.com>
- 1.1.6 release
- added jira token auth
- added --skip-network to validate_env.py
- added ls_switch_conf.py tool
- added lshw.py tool
- autocomplete for via python3-argcomplete
- bug fixes
- refactoring

* Tue May 11 2021 Will Foster <wfoster@redhat.com>
- 1.1.5 release
- added JIRA integration/tools
- added --host-list for --add-schedule
- color coding and priority for --ls-available
- added --retire --unretire and --ls-retire feature
- bug fixes

* Thu Dec 17 2020 Will Foster <wfoster@redhat.com>
- 1.1.4.1 release
- added --extend and --shrink
- small set of bug fixes

* Tue Nov 24 2020 Will Foster <wfoster@redhat.com>
- 1.1.4 release
- bare-metal host metadata model implemented
- quads-cli now has --mod-cloud functionality
- quads-cli now has --extend-cloud functionality
- quads-cli manages broken systems now with
  --mark-broken, --mark-repaired and --ls-broken
- asyncio enhancements
- flask-based --ls-available ui tech preview, new
  service 'quads-web'
- --ls-available now has --filter capability
- bug fixes for quads and badfish

* Tue Apr 07 2020 Will Foster <wfoster@redhat.com>
- 1.1.3 release

* Wed Jan 08 2020 Will Foster <wfoster@redhat.com>
- 1.1.2 release

* Thu Oct 31 2019 Will Foster <wfoster@redhat.com>
- 1.1.1 release

* Fri Aug 23 2019 Will Foster <wfoster@redhat.com>
- 1.1.0 final release
- asyncio implemented for provisioning

* Thu Mar 21 2019 Will Foster <wfoster@redhat.com>
- 1.1.0 release version bump
- Remove mongodb and mongodb-server deps due to
  removal from Fedora30

* Fri Mar 08 2019 Will Foster <wfoster@redhat.com>
- Fixes for PYTHONPATH for quads-cli
- Bump minor release for COPR builds
- Remove unneeded libs, deprecated tools

* Mon Feb 25 2019 Will Foster <wfoster@redhat.com>
- Initial packaging work for 1.1 beta
- This is a work-in-progress, full 1.1 changes will arrive when this fully
  builds.

* Wed Feb 13 2019 Will Foster <wfoster@redhat.com>
- Bump version to match 1.0.2 tag
- Bug fixes in wiki generation and VLAN stub creation
- Removal of bin/quads.py in lieu of quads-cli
- Lots of documentation updates and additions
- Fixes to Juniper automation to rollback uncommitted changes

* Thu Nov 22 2018 Will Foster <wfoster@redhat.com>
- Bump version to match 1.0.1 tag
- PDU control feature added - issue #100
- Public VLAN management added into cloud definitions - issue #192
- We can now check against broken hosts in Foreman if broken_state
  host parameter is set before allowing those machines to be scheduled - issue #190

* Fri Apr 20 2018 Will Foster <wfoster@redhat.com>
- Bump version to match 1.0.0 tag

* Fri Oct 20 2017 Will Foster <wfoster@redhat.com>
- Add httpd dependency and visualization image files

* Wed Aug 30 2017 Will Foster <wfoster@redhat.com>
- Initial spec file and package into RPM
- This will be available in Fedora COPR, updated in sync with master
  - https://copr.fedorainfracloud.org/coprs/quadsdev/QUADS/
