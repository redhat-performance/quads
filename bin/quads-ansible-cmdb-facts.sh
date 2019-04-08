#!/usr/bin/sh
# generate ansible facts HTML page per cloud

if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi

source $(dirname $0)/load-config.sh

quads=${quads["install_dir"]}/bin/quads-cli
quads_url=${quads["quads_url"]}
data_dir=${quads["data_dir"]}
ansible_facts_web_path=${quads["ansible_facts_web_path"]}

function generate_facts(){
    name=$1
    owner=$2
    rt=$3
    cloud_specific_tag="${name}_${owner}_${rt}"
    facts_dir="${data_dir}/ansible_facts"
    # create directory to hold facts for ansible-cmdb consumption, if it doesn't exist
    if [ ! -d $facts_dir ]; then
        mkdir "$facts_dir"
    fi
    # create directory to serve the html contents out of, if it doesnt exist
    if [ ! -d "${ansible_facts_web_path}" ]; then
        mkdir "${ansible_facts_web_path}"
    fi
    pushd $facts_dir
    rm -rf $name
    # make cloud specific directory
    mkdir $name
    pushd $name
    # make hosts file for ansible
    $quads --cloud-only ${name} > "${cloud_specific_tag}_hosts"
    mkdir out
    # gather ansible facts and dump them into the out directory, store return code, timeout is present so that
    # command doesn't hang if hosts aren't reachable (due to new OS being installed
    # without the foreman public key for eexample. Also, ansible fact gathering is pretty
    # fast, for 30 hosts it took around 5 seconds.
    timeout 120 ansible -i "${cloud_specific_tag}_hosts" -m setup --tree out/ all
    facts_return=$?
    # ansible-cmdb command to generate the static html
    ansible-cmdb -i "${cloud_specific_tag}_hosts" out/ > "${cloud_specific_tag}_overview.html"
    # copy the html over to the directory served by apache only if previous command
    # was successful, otherwise the old copy is used
    if [ "${facts_return}" -eq 0 ]; then
        cp "${cloud_specific_tag}_overview.html" "${ansible_facts_web_path}/${cloud_specific_tag}_overview.html"
    fi
    popd
    popd
    return $facts_return
}

rpm -q ansible-cmdb
if [ "$?" -eq 0 ]; then
    generate_facts $1 $2 $3
    exit $?
else
    exit 1
fi

