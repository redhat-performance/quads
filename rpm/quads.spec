%define name quads
%define version 0.99
%define OWNER redhat-performance

%global commit0 aa494183c65141197a48961e921a7e52bbccbeb3
%global gittag0 GIT-TAG
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Summary: Automated future scheduling, documentation, end-to-end provisioning and assignment of servers and networks.
Name: %{name}
Version: %{version}
Release: %{shortcommit0}
Source0: https://github.com/%{OWNER}/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{version}-%{shortcommit0}.tar.gz
License: GPL3
Group: Applications/Internet
BuildRoot: %{_tmppath}/%{name}-buildroot
Prefix: /usr
BuildArchitectures: noarch
Vendor: QUADS
Packager: QUADS CI
Requires: PyYAML >= 3.10
Requires: ansible >= 2.3
Requires: expectk >= 5.0
Requires: python2-aexpect >= 1.4
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
%autosetup -n %{name}-%{commit0}

%install
rm -rf $RPM_BUILD_ROOT
mkdir $RPM_BUILD_ROOT/opt/quads -p
tar cf - bin lib/*.py conf ansible systemd | ( cd $RPM_BUILD_ROOT/opt/quads/ ; tar xvpBf - )

%clean
rm -rf %{buildroot}

%files
/opt/quads/ansible/*
/opt/quads/bin/*
/opt/quads/lib/*
/opt/quads/systemd/*
%config /opt/quads/conf/quads.yml

%changelog
