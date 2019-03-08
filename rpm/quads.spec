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

%define name quads
%define version 1.0.99
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
Requires: mongodb >= 2.6.12
Requires: mongodb-server >= 2.6.12
Requires: python3-cherrypy >= 8.9
Requires: python3-jinja2 >= 2.0
Requires: python3-passlib >= 1.7
Requires: python3-PyYAML >= 3.0
Requires: python3-requests >= 2.0
Requires: git
Requires: ipmitool
Requires: python3-paramiko >= 2.3
Requires: python3-wordpress-xmlrpc >= 2.2
Requires: python3-pexpect >= 4.2

Url: http://github.com/redhat-performance/quads

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
%autosetup -n %{name}-master

%install
rm -rf %{buildroot}
mkdir %{buildroot}%{prefix} -p
mkdir %{buildroot}/etc/systemd/system/ -p
mkdir %{buildroot}/etc/profile.d/ -p
tar cf - bin quads/*.py quads/tools/*.py quads/templates/* quads/*.py conf | ( cd %{buildroot}%{prefix} ; tar xvpBf - )
cp -rf systemd/quads-server.service %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/var/www/html/visual/
cp -p image/{texture*,button*}.png  %{buildroot}/var/www/html/visual/
echo 'export PATH="/opt/quads/bin:$PATH"' > %{buildroot}/etc/profile.d/quads.sh
echo 'export PYTHONPATH="$PYTHONPATH:/opt/quads/"' >> %{buildroot}/etc/profile.d/quads.sh

%clean
rm -rf %{buildroot}

%files
/etc/systemd/system/quads-server.service
/etc/profile.d/quads.sh
/opt/quads/bin/*
/opt/quads/quads/*
/opt/quads/quads/tools/*
/opt/quads/quads/templates/*
/var/www/html/visual/*
%config(noreplace) /opt/quads/conf/quads.yml
%config(noreplace) /opt/quads/conf/vlans.yml
%config(noreplace) /opt/quads/conf/idrac_interfaces.yml

%post
systemctl enable quads-server
systemctl enable mongod

%preun
if [ "$1" -eq 0 ]; then
  systemctl stop quads-server
  systemctl disable quads-server
fi;
:;

%changelog

* Mon Feb 25 2019 - 1.0.99: Will Foster <wfoster@redhat.com>
- Initial packaging work for 1.1 beta
- This is a work-in-progress, full 1.1 changes will arrive when this fully
  builds.

* Wed Feb 13 2019 - 1.0.2: Will Foster <wfoster@redhat.com>
- Bump version to match 1.0.2 tag
- Bug fixes in wiki generation and VLAN stub creation
- Removal of bin/quads.py in lieu of quads-cli
- Lots of documentation updates and additions
- Fixes to Juniper automation to rollback uncommitted changes

* Thu Nov 22 2018 - 1.0.1: Will Foster <wfoster@redhat.com>
- Bump version to match 1.0.1 tag
- PDU control feature added - issue #100
- Public VLAN management added into cloud definitions - issue #192
- We can now check against broken hosts in Foreman if broken_state
  host parameter is set before allowing those machines to be scheduled - issue #190

* Fri Apr 20 2018 - 1.0.0: Will Foster <wfoster@redhat.com>
- Bump version to match 1.0.0 tag

* Fri Oct 20 2017 - 0.99.2: Will Foster <wfoster@redhat.com>
- Add httpd dependency and visualization image files

* Wed Aug 30 2017 - 0.99: Will Foster <wfoster@redhat.com>
- Initial spec file and package into RPM
- This will be available in Fedora COPR, updated in sync with master
  - https://copr.fedorainfracloud.org/coprs/quadsdev/QUADS/
