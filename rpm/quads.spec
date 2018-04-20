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
%define version 1.0.0
%define build_timestamp %{lua: print(os.date("%Y%m%d"))}

Summary: Automated future scheduling, documentation, end-to-end provisioning and assignment of servers and networks.
Name: %{name}
Version: %{version}
Release: %{build_timestamp}
Source0: https://github.com/redhat-performance/quads/archive/master.tar.gz#/%{name}-%{version}-%{release}.tar.gz
License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: /opt/quads
BuildArch: noarch
Vendor: QUADS
Packager: QUADS
# required for quads-1.1+
#Requires: epel-release
Requires: PyYAML >= 3.10
Requires: ansible >= 2.3
Requires: expectk >= 5.0
Requires: python2-aexpect >= 1.4
Requires: python-requests >= 2.6
Requires: httpd >= 2.4
# required for quads-1.1+
#Requires: python-mongoengine >= 0.8
#Requires: mongodb >=2.6.12
#Requires: mongodb-server >=2.6.12
Url: http://github.com/redhat-performance/quads

%description

Create and manage a date/time based YAML schedule for machine allocations
Drive system provisioning and network switch changes based on workload assignment via external commands
Automated network and provisioning validation prior to delivering sets of machines/networks to users.
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
tar cf - bin lib/*.py conf ansible | ( cd %{buildroot}%{prefix} ; tar xvpBf - )
cp -rf systemd/quads-daemon.service %{buildroot}/etc/systemd/system/
mkdir -p %{buildroot}/var/www/html/visual/
cp -p image/{texture*,button*}.png  %{buildroot}/var/www/html/visual/
echo 'export PATH="/opt/quads/bin:$PATH"' > %{buildroot}/etc/profile.d/quads.sh

%clean
rm -rf %{buildroot}

%files
/etc/systemd/system/quads-daemon.service
/etc/profile.d/quads.sh
/opt/quads/ansible/*
/opt/quads/bin/*
/opt/quads/lib/*
/var/www/html/visual/*
%config /opt/quads/conf/quads.yml

%post
systemctl enable quads-daemon
# will be required for quads-1.1+
#systemctl enable mongod
[ ! -d /opt/quads/log ] && mkdir /opt/quads/log || true
[ ! -f /opt/quads/log/quads.log ] && touch /opt/quads/log/quads.log || true
[ ! -d /var/log/quads ] && mkdir /var/log/quads || true
:;

%preun
if [ "$1" -eq 0 ]; then
  systemctl stop quads-daemon
  systemctl disable quads-daemon
fi;
:;

%changelog

* Fri Apr 20 2018 - 1.0.0: Will Foster <wfoster@redhat.com>
- Bump version to match 1.0.0 tag

* Fri Oct 20 2017 - 0.99.2: Will Foster <wfoster@redhat.com>
- Add httpd dependency and visualization image files

* Wed Aug 30 2017 - 0.99: Will Foster <wfoster@redhat.com>
- Initial spec file and package into RPM
- This will be available in Fedora COPR, updated in sync with master
  - https://copr.fedorainfracloud.org/coprs/quadsdev/QUADS/
