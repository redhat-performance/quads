#!/usr/bin/sh
# Gather CPU performance and boot interface infos
# from Dell machines # and generate an HTML file with them.
# not used in 1.1.0

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
env=$1

cat <<EOF
<style type="text/css">
    .TFtable{
        width:100%;
        border-collapse:collapse;
    }
    .TFtable td{
        padding:7px; border:#4e95f4 1px solid;
    }
    /* provide some minimal visual accomodation for IE8 and below */
    .TFtable tr{
        background: #b8d1f3;
    }
    /*  Define the background color for all the ODD background rows  */
    .TFtable tr:nth-child(odd){
        background: #b8d1f3;
    }
    /*  Define the background color for all the EVEN background rows  */
    .TFtable tr:nth-child(even){
        background: #dae5f4;
    }
</style>
EOF

#for cloud in $($quads --summary | awk -F: '{ print $1 }' | grep -v cloud01) ; do
    cloud=$env
    #echo "<h><b>System Settings for $cloud</b></h>"
    #echo "<br>"
    echo "<table class=\"TFtable\">"
    echo "<tr>"
    echo "<th>Name</th>"
    echo "<th>CPU Setting</th>"
    echo "<th>Boot Order</th>"
    echo "</tr>"
    for h in $($quads --cloud-only $cloud | egrep 'r620|r630|r720|r730|r930') ; do
        echo "<tr>"
        echo "<td>$h</td>"
        profile=$(ssh -o passwordauthentication=no -o connecttimeout=3 mgmt-$h racadm get BIOS.SysProfileSettings.SysProfile 2>/dev/null| egrep -i ^sysp | awk -F= '{ print $2 }')
        bootorder=$(ssh -o passwordauthentication=no -o connecttimeout=3 mgmt-$h racadm get bios.BiosBootSettings.bootseq 2>/dev/null| egrep -i ^bootseq | awk -F= '{ print $2 }')
        if [ "$profile" == "PerfPerWattOptimizedDapc" ] ; then
            echo "<td bgcolor=\"red\">$profile</td>"
        else
            echo "<td>$profile</td>"
        fi
        case $(echo $h | awk -F. '{ print $1 }' | awk -F- '{ print $3 }') in
            'r620')
                echo "<td>$bootorder</td>" | sed -e 's,NIC.Integrated.1-3-1,<b>NET 5 (Foreman)</b>,g' -e 's,NIC.Slot.2-4,<b>NET 2 (Director)</b>,g' -e 's,HardDisk.List.1-1,<b>Hard Drive</b>,g'
                echo "</tr>"
                ;;
            'r630')
                echo "<td>$bootorder</td>" | sed -e 's,NIC.Slot.2-1-1,<b>NET 5 (Foreman)</b>,g' -e 's,NIC.Integrated.1-2-1,<b>NET 2 (Director)</b>,g' -e 's,HardDisk.List.1-1,<b>Hard Drive</b>,g'
                echo "</tr>"
                ;;
            'r720xd')
                echo "<td>$bootorder</td>" | sed -e 's,NIC.Integrated.1-3-1,<b>NET 5 (Foreman)</b>,g' -e 's,NIC.Slot.4-2-1,<b>NET 2 (Director)</b>,g' -e 's,HardDisk.List.1-1,<b>Hard Drive</b>,g'
                echo "</tr>"
                ;;
            'r730xd')
                echo "<td>$bootorder</td>" | sed -e 's,NIC.Integrated.1-3-1,<b>NET 5 (Foreman)</b>,g' -e 's,NIC.Slot.2-4,<b>NET 2 (Director)</b>,g' -e 's,HardDisk.List.1-1,<b>Hard Drive</b>,g'
                echo "</tr>"
                ;;
            'r930')
                echo "<td>$bootorder</td>" | sed -e 's,NIC.Integrated.1-3-1,<b>NET 5 (Foreman)</b>,g' -e 's,NIC.Integrated.1-2-1,<b>NET 2 (Director)</b>,g' -e 's,HardDisk.List.1-1,<b>Hard Drive</b>,g'
                echo "</tr>"
                ;;
        esac
    done
    echo "</table>"
    echo "<br>"
#done

