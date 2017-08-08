#!/bin/bash 
if [ ! -e $(dirname $0)/load-config.sh ]; then
    echo "$(basename $0): could not find load-config.sh"
    exit 1
fi
source $(dirname $0)/load-config.sh
quads=${quads["install_dir"]}/bin/quads.py
openstack_installer=${quads["install_dir"]}/bin/openstack.py
install_dir=${quads["install_dir"]}
bin_dir=${quads["install_dir"]}/bin
data_dir=${quads["data_dir"]}
infrared_dir=${quads["infrared_directory"]}
ssh_priv_key=${quads["private_key_location"]}
json_web_path=${quads["json_web_path"]}
openstack_templates_dir=${quads["openstack_templates"]}
openstack_templates_git=https://github.com/smalleni/automated-openstack-templates.git

# trap to make sure 
function finish {
  rm ${data_dir}/postconfig/${env}-${owner}-${ticket}-${1}-start
}
trap finish EXIT

# function that does the undercloud and overcloud deploy

function apply_post_config() {
   setup_infrared
   pushd $infrared_dir/infrared
   source .venv/bin/activate
   delete_workspace $1
   create_workspace $1
   undercloud=$($quads --cloud-only $1 | head -1)
   setup_inventory $1 $undercloud
   version=$($openstack_installer -c $1 -q | head -1)
   build=$($openstack_installer -c $1 -q | tail -1)
   # defaults to em2 interface and enables cleaning of nodes by default
   IR_WORKSPACE=$1 ir tripleo-undercloud --version 11 --build GA --config-options DEFAULT.local_interface=em2 --config-options DEFAULT.clean_nodes=true
   $openstack_installer -c $1 -i $2 -t $3 -uc $undercloud
   # wait for the openstack install script to write out appropriate
   # instackenv.json and for it to be available 
   sleep 120
   IR_WORKSPACE=$1 ir tripleo-undercloud --images-task rpm
   # introspect
   IR_WORKSPACE=$1 ir tripleo-overcloud --introspect yes --tag yes --version $version --instackenv-file $2 --deployment-files $3
   # wait for nodes to be cleaned; need more comprehensive checks in the future
   sleep 600
   # deploy
   IR_WORKSPACE=$1 ir tripleo-overcloud --introspect yes --tag yes --deploy yes --version $version --instackenv-file $2 --deployment-files $3
   if [ "$?" -eq 0 ]; then
       touch ${data_dir}/postconfig/${env}-${owner}-${ticket}-${1}-success
   fi
}



# since our workspace name is just cloudname we will keep reusing names, so we
# need to delete existing workspaces, export them and start fresh

function delete_workspace() {
    workspace=$(ir wokspace list | grep -q $1)
    if [  "$workspace" != "" ]
    then
        if [ ! -d $infrared_dir/backup ]; then
           mkdir $infrared_dir/backup
        fi
    infrared workspace export $1 --dest $infrared_dir/backup/$1-$(date +"%s")
    infrared workspace cleanup $1
    fi
}



# Create workspace for infrared specific to cloudname
function create_workspace() {
    infrared workspace create $1
}


# Pass cloudname as 1st argument and FQDN of undercloud as 2nd argument
function setup_inventory() {
    cat <<EOF > $infrared_dir/infrared/.workspaces/$1/hosts
$2 ansible_ssh_host=$2 ansible_ssh_user=root ansible_ssh_private_key_file=$ssh_priv_key
localhost ansible_connection=local ansible_python_interpreter=python

[undercloud]
$2

[local]
localhost
EOF
}

# Installs and sets up infrared on the QUADS host if its hasn't been done

function setup_infrared() {
    if [ ! -d $infrared_dir/infrared]; then
        git clone https://github.com/redhat-openstack/infrared.git $infrared_dir/infrared
        pushd $infrared_dir/infrared
        virtualenv .venv && source .venv/bin/activate
        pip install --upgrade pip
        pip install --upgrade setuptools
        pip install .
        popd
    fi

}

# Directory for all post-config related state (to track clouds with deployments
# in progress vs undeployed clouds vs clouds that have had successful
# deployments
if [ ! -d ${data_dir}/postconfig ]; then
    mkdir ${data_dir}/postconfig
fi


# Pass "openstack" as 1st argument to this script

for env in $($quads --summary --post-config $1 ; do
    owner=$($quads --ls-owner --cloud-only $env)
    ticket=$($quads --ls-ticket --cloud-only $env)
    if [ "$owner" != "nobody" -a "$owner" -a "$ticket" ]; then
        if [ -f $data_dir/release/${env}-${owner}-${ticket} ]; then
                if [ ! -f
                    ${data_dir}/postconfig/${env}-${owner}-${ticket}-${1}-start ] && [ ! -f ${data_dir}/postconfig/${env}-${owner}-${ticket}-${1}-success ]; then
                touch ${data_dir}/postconfig/${env}-${owner}-${ticket}-${1}-start
                # Clone OpenStack Templates
                cloud_specific_templates=${openstack_templates_dir}/${env}-${owner}-${ticket}/automated-openstack-templates
                if [ ! -d ${cloud_specific_templates} ]; then
                    mkdir ${cloud_specific_templates}
                fi
                git clone  https://github.com/smalleni/automated-openstack-templates  $cloud_specific_templates
                apply_post_config $env $json_web_path/${env}_instackenv.json $cloud_specific_templates
            fi
        fi
    fi
done

