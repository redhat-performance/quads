import json
import os
import shutil
from collections import namedtuple
from pathlib import Path

from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.plugins.callback import CallbackBase
from ansible.vars.manager import VariableManager

from quads.config import conf
from quads.model import Cloud


class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        host = result._host
        print(json.dumps({host.name: result._result}, indent=4))


def main():
    data_dir = conf["data_dir"]
    facts_dir = os.path.join(data_dir, "/ansible_facts")
    ansible_facts_web_path = conf["ansible_facts_web_path"]
    if not os.path.exists(facts_dir):
        Path(facts_dir).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(ansible_facts_web_path):
        Path(ansible_facts_web_path).mkdir(parents=True, exist_ok=True)
    _clouds = Cloud.objects()
    _cloud_names = [cloud.name for cloud in _clouds]

    Options = namedtuple('Options', ['connection', 'forks', 'become', 'become_method', 'become_user', 'check', 'diff'])
    options = Options(connection='local', forks=10, become=None, become_method=None, become_user=None, check=False,
                      diff=False)

    loader = DataLoader()

    results_callback = ResultCallback()

    inventory = InventoryManager(loader=loader, sources=",".join(_cloud_names))

    variable_manager = VariableManager(loader=loader, inventory=inventory)

    play_source = dict(
        name="Ansible Play",
        hosts='localhost',
        gather_facts='no',
        tasks=[
            dict(action=dict(module='setup', args='--tree out/ all'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}')))
        ]
    )

    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            stdout_callback=results_callback,
        )
        result = tqm.run(play)
        print(result)
    finally:
        if tqm is not None:
            tqm.cleanup()


if __name__ == "__main__":
    main()
