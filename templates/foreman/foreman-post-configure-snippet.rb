# Custom post bits to run at the end for the scalelab
## define foreman template definitions here
<%
os_major = @host.operatingsystem.major.to_i
%>
# <% os_major -%>
## end foreman template definitions
mask2cdr ()
{
   # Assumes there's no "255." after a non-255 byte in the mask
   local x=${1##*255.}
   set -- 0^^^128^192^224^240^248^252^254^ $(( (${#1} - ${#x})*2 )) ${x%%.*}
   x=${1%%$3*}
   echo $(( $2 + (${#x}/4) ))
}


cdr2mask ()
{
   # Number of args to shift, 255..255, first non-255 byte, zeroes
   set -- $(( 5 - ($1 / 8) )) 255 255 255 255 $(( (255 << (8 - ($1 % 8))) & 255 )) 0 0 0
   [ $1 -gt 1 ] && shift $1 || shift
   echo ${1-0}.${2-0}.${3-0}.${4-0}
}

def_interface=$(ip route  | egrep ^default | awk '{ print $5 }' | head -1)
def_gateway=$(ip route  | egrep ^default | awk '{ print $3 }' | head -1)
#def_network=$(ip route  | egrep -v ^default | grep $def_interface | grep -v 169.254 | awk '{ print $1 }')
def_address=$(ip a show $def_interface | grep "inet " | awk '{ print $2 }'| awk -F/ '{ print $1 }')
def_network_address=$(netstat -rn | egrep -v 'Destination|169.254|^0.0.0.0|^Kernel'  | grep $def_interface | awk '{ print $1 }')
#def_network_cidr=$(echo $def_network | awk -F/ '{ print $2 }')
def_network_netmask=$(netstat -rn | egrep -v 'Destination|169.254|^0.0.0.0|^Kernel' | grep $def_interface | awk '{ print $3 }' | grep -v 255.255.255.255 )

### try and make EL8 not drop this as it doesn't extrapolate correctly for netmask

<% if os_major != 7 || @host.operatingsystem.name != 'Fedora' %>
cat > /etc/sysconfig/network-scripts/ifcfg-$def_interface <<EOF
DEVICE=$def_interface
NAME=$def_interface
TYPE=Ethernet
BOOTPROTO=dhcp
DEFROUTE=yes
ONBOOT=yes
EOF

<% else %>

cat > /etc/sysconfig/network-scripts/ifcfg-$def_interface <<EOF
DEVICE=$def_interface
NAME=$def_interface
TYPE=Ethernet
BOOTPROTO=static
DEFROUTE=yes
ONBOOT=yes
IPADDR=$def_address
NETMASK=$def_network_netmask
GATEWAY=$def_gateway
EOF
<% end -%>

<% if os_major != 7 || @host.operatingsystem.name != 'Fedora' %>
cat > /etc/sysconfig/network <<EOF
# We leave this blank for DHCP
EOF

<% else %>

cat > /etc/sysconfig/network <<EOF
NETWORKING=yes
GATEWAY=$def_gateway
EOF

<% end -%>

### update NTP or chronyd depending on OS

<% if os_major != 7 || @host.operatingsystem.name != 'Fedora' %>
cat > /etc/chrony.conf <<EOF
pool foreman.rdu2.scalelab.example.com iburst
driftfile /var/lib/chrony/drift
makestep 1.0 3
rtcsync
keyfile /etc/chrony.keys
leapsectz right/UTC
logdir /var/log/chrony
EOF

<% else %>

cat > /etc/ntpd.conf <<EOF
server foreman.rdu2.scalelab.example.com iburst
driftfile /var/lib/ntp/drift
restrict default nomodify notrap nopeer noquery
restrict 127.0.0.1
restrict ::1
includefile /etc/ntp/crypto/pw
keys /etc/ntp/keys
disable monitor
EOF

<% end -%>


cat > /etc/resolv.conf <<EOF
search rdu2.scalelab.example.com
nameserver 10.1.32.3
nameserver 10.1.32.4
EOF

# setup em1, em2, em3, and em4 and also ens3f0/1 or ens5f0/1 === WIP
o3=$(echo $def_address | awk -F. '{ print $3 }')
# use pipe awk line here as 4th octect, carriage return cause render issues
o4=$(echo $def_address | awk -F. '{ print $4 }' | awk '{ print $1 }')

# Attempt to break snippets out for network configs
<%= snippet 'custom-generic-network-post.rb' %>

