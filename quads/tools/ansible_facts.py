import shutil

from ansible.constants import DEFAULT_LOCAL_TMP
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.module_utils.common.collections import ImmutableDict
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager
from ansible import context


class ResultsCollectorJSONCallback(CallbackBase):
    def __init__(self, *args, **kwargs):
        super(ResultsCollectorJSONCallback, self).__init__(*args, **kwargs)
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        host = result._host
        self.host_unreachable[host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        host = result._host
        self.host_ok[host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        host = result._host
        self.host_failed[host.get_name()] = result


def get_host_interfaces(host_list):
    options = dict(
        syntax=False,
        timeout=30,
        connection='ssh',
        forks=10,
        remote_user='root',
        verbosity=1,
        check=False,
        diff=False,
        gathering='implicit',
        remote_tmp='/tmp/.ansible'
    )
    context.CLIARGS = ImmutableDict(options)
    sources = ','.join(host_list)
    if len(host_list) == 1:
        sources += ','

    loader = DataLoader()
    passwords = dict(vault_pass='secret')
    results_callback = ResultsCollectorJSONCallback()

    inventory = InventoryManager(loader=loader, sources=sources)
    variable_manager = VariableManager(loader=loader, inventory=inventory)

    tqm = TaskQueueManager(
        inventory=inventory,
        variable_manager=variable_manager,
        loader=loader,
        passwords=passwords,
        stdout_callback=results_callback,
    )

    play_source = dict(
        name="Ansible Play",
        hosts=host_list,
        gather_facts='no',
        tasks=[
            dict(action=dict(module='setup')),
        ]
    )

    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    try:
        tqm.run(play)
    finally:
        tqm.cleanup()
        if loader:
            loader.cleanup_all_tmp_files()

    shutil.rmtree(DEFAULT_LOCAL_TMP, True)

    results = {}
    for host, result in results_callback.host_ok.items():
        facts = result._result.get('ansible_facts')
        if facts:
            interfaces = facts.get('ansible_interfaces')
            if interfaces:
                interfaces_dict = {}
                for interface in sorted(interfaces):
                    interface_obj = facts.get('ansible_%s' % interface)
                    if interface_obj:
                        interfaces_dict[interface] = interface_obj.get('ipv4')
                results[host] = interfaces_dict

    return results
