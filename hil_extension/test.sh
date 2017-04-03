#!/bin/sh

current_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
quads_dir="$(dirname "$current_dir")"
parent_dir="$(dirname "$quads_dir")"
hil_dir=${parent_dir}/hil

if [ ! -d "$hil_dir" ]; then
	echo "Couldn't find HIL directory. HIL directory should be ./../hil."
	exit
fi
start_hil_server(){
	cd $hil_dir
	rm haas/haas.db
	ps aux | grep '[h]aas serve 5000' | awk '{print $2}' | xargs kill -9 
	source .venv/bin/activate
	haas-admin db create
	haas serve 5000
}
start_hil_server &
sleep 1
echo HIL server was started in a child process.
sleep 1

start_hil_networks(){
        cd $hil_dir
        source .venv/bin/activate
        haas serve_networks
}
start_hil_networks &
sleep 1
echo HIL networks server was started in a child process.
sleep 1

./cli.py node_register host01.com mock host user password
./cli.py node_register_nic host01.com nic mac_address
./cli.py switch_register switch mock host user password
./cli.py port_register switch port
./cli.py port_connect_nic switch port host01.com nic
./cli.py project_create quads
./cli.py network_create_simple cloud01 quads
./cli.py network_create_simple cloud02 quads
./cli.py project_connect_node quads host01.com
./cli.py node_connect_network host01.com nic cloud01 null

rm -f -r /opt/quads
mkdir -p /opt/quads/log
touch /opt/quads/log/quads.log

quads=${quads_dir}/bin/quads.py

$quads --init
$quads --sync
$quads --define-cloud cloud01 --description cloud01
$quads --define-cloud cloud02 --description cloud02
$quads --define-host host01.com --default-cloud cloud01
$quads --add-schedule --host host01.com --schedule-start "2016-01-01 08:00" --schedule-end "2016-01-10 08:00" --schedule-cloud cloud02
$quads --sync
$quads --move-hosts --date "2016-01-02 09:00" --move-command ./move-and-rebuild-host-hil.sh
$quads --move-hosts --date "2016-01-12 09:00" --move-command ./move-and-rebuild-host-hil.sh

