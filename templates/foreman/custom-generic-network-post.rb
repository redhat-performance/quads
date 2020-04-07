<%
os_major = @host.operatingsystem.major.to_i
%>
# default interface names may get overridden due to foreman templates
# basically this is getting used as a default value.  If we don't know
# what the actual names are for these for a particular node type for
# both RHEL7 and RHEL8 (or any other OS we want to support such as fedora),
# then the NIC will likely not exist and we will fail to setup the
# necessary private networks with the 172.x.x.x addressing, and therefore
# will fail our network connectivity tests (if we care).  This mostly
# matters for quads hosts, and validation testing.
#
# Note: these interfaces should line up with what is documented here:

nic1=nic1
nic2=nic2
nic3=nic3
nic4=nic4

<% if os_major == 7 %>
<% if @host.shortname =~ /1029p/ %>
nic1=enp94s0f0
nic2=enp94s0f1
nic3=enp94s0f2
nic4=enp94s0f3
<% end -%>
<% if @host.shortname =~ /1029u/ %>
nic1=enp175s0f0
nic2=enp175s0f1
nic3=enp216s0f0
nic4=enp216s0f1
<% end -%>
<% if @host.shortname =~ /5039ms/ %>
nic1=enp1s0f0
nic2=enp1s0f1
nic3=enp2s0f1
<% end -%>
<% if @host.shortname =~ /6018r/ %>
nic1=enp4s0f0
nic2=enp4s0f1
nic3=enp4s0f2
nic4=enp4s0f3
<% end -%>
<% if @host.shortname =~ /6048r/ %>
nic1=enp4s0f0
nic2=enp4s0f1
nic3=enp131s0f0
nic4=enp131s0f1
<% end -%>
<% if @host.shortname =~ /6049p/ %>
nic1=enp175s0f0
nic2=enp175s0f1
nic3=enp216s0f0
nic4=enp216s0f1
<% end -%>
<% if @host.shortname =~ /r620/ %>
nic1=p2p3
nic2=p2p4
nic3=em1
nic4=em2
<% end -%>
<% if @host.shortname =~ /r630/ %>
nic1=em1
nic2=em2
nic3=em3
nic4=em4
<% end -%>
<% if @host.shortname =~ /r640/ %>
nic1=p3p1
nic2=p3p2
nic3=p2p1
nic4=p2p2
<% end -%>
<% if @host.shortname =~ /r730xd/ %>
nic1=em1
nic2=em2
nic3=p4p1
nic4=p4p2
<% end -%>
<% if @host.shortname =~ /r930/ %>
nic1=em1
nic2=em2
nic3=p1p1
nic4=p1p2
<% end -%>
<% if @host.shortname =~ /b01-fc640/ %>
nic1=em2
nic2=p8p1
nic3=p8p2
<% end -%>
<% if @host.shortname =~ /b02-fc640/ %>
nic1=em2
nic2=p4p1
nic3=p4p2
<% end -%>
<% if @host.shortname =~ /b03-fc640/ %>
nic1=em2
nic2=p6p1
nic3=p6p2
<% end -%>
<% if @host.shortname =~ /b04-fc640/ %>
nic1=em2
nic2=p2p1
nic3=p2p2
<% end -%>

<% end -%>

<% if os_major == 8 %>
<% if @host.shortname =~ /1029p/ %>
nic1=ens2f0
nic2=ens2f1
nic3=ens2f2
nic4=ens2f3
<% end -%>
<% if @host.shortname =~ /1029u/ %>
nic1=ens1f0
nic2=ens1f1
nic3=ens2f0
nic4=ens2f1
<% end -%>
<% if @host.shortname =~ /5039ms/ %>
nic1=enp1s0f0
nic2=enp1s0f1
nic3=enp2s0f1
<% end -%>
<% if @host.shortname =~ /6018r/ %>
# FILL ME IN
<% end -%>
<% if @host.shortname =~ /6048r/ %>
# FILL ME IN
<% end -%>
<% if @host.shortname =~ /6049p/ %>
nic1=ens3f0
nic2=ens3f1
nic3=ens2f0
nic4=ens2f1
<% end -%>
<% if @host.shortname =~ /r620/ %>
nic1=enp66s0f2
nic2=enp66s0f3
nic3=eno1
nic4=eno2
<% end -%>
<% if @host.shortname =~ /r630/ %>
nic1=eno1
nic2=eno2
nic3=eno3
nic4=eno4
<% end -%>
<% if @host.shortname =~ /r640/ %>
nic1=ens3f0
nic2=ens3f1
nic3=ens2f0
nic4=ens2f1
<% end -%>
<% if @host.shortname =~ /r730xd/ %>
# FILL ME IN
<% end -%>
<% if @host.shortname =~ /r930/ %>
# FILL ME IN
<% end -%>
<% if @host.shortname =~ /b01-fc640/ %>
nic1=ens2f0
nic2=ens2f1
nic3=eno2
<% end -%>
<% if @host.shortname =~ /b02-fc640/ %>
nic1=ens2f0
nic2=ens2f1
nic3=eno2
<% end -%>
<% if @host.shortname =~ /b03-fc640/ %>
nic1=ens2f0
nic2=ens2f1
nic3=eno2
<% end -%>
<% if @host.shortname =~ /b04-fc640/ %>
nic1=ens2f0
nic2=ens2f1
nic3=eno2
<% end -%>
<% end -%>

nics=($nic1 $nic2 $nic3 $nic4)
vlans=(101 102 103 104)
commonvlan=200
octets=(16 17 18 19)
taggedoctets=(20 21 22 23)
commonoctets=(24 25 26 27)

for index in 0 1 2 3 ; do
  interface=${nics[$index]}
  vlan=${vlans[$index]}
  octet=${octets[$index]}
  taggedoctet=${taggedoctets[$index]}
  commonoctet=${commonoctets[$index]}
  if ip a show $interface 1>/dev/null 2>&1 ; then
    cat > /etc/sysconfig/network-scripts/ifcfg-$interface <<EOF
DEVICE=$interface
NAME=$interface
TYPE=Ethernet
BOOTPROTO=static
DEFROUTE=no
ONBOOT=yes
IPADDR=172.$octet.$o3.$o4
NETMASK=255.255.0.0
EOF
    cat > /etc/sysconfig/network-scripts/ifcfg-$interface.$vlan <<EOF
DEVICE=$interface.$vlan
NAME=$interface.$vlan
VLAN=yes
BOOTPROTO=static
DEFROUTE=no
ONBOOT=yes
IPADDR=172.$taggedoctet.$o3.$o4
NETMASK=255.255.0.0
EOF
    cat > /etc/sysconfig/network-scripts/ifcfg-$interface.$commonvlan <<EOF
DEVICE=$interface.$commonvlan
NAME=$interface.$commonvlan
VLAN=yes
BOOTPROTO=static
DEFROUTE=no
ONBOOT=yes
IPADDR=172.$commonoctet.$o3.$o4
NETMASK=255.252.0.0
EOF

  fi
done
