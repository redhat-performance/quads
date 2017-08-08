from oslo_config import cfg

control_group = cfg.OptGroup(name='control',
                         title='Controller Options')
ceph_group = cfg.OptGroup(name='ceph',
                         title='Ceph Options')
compute_group = cfg.OptGroup(name='compute',
                         title='Compute Options')

control_opts = [
    cfg.IntOpt('priority_r930', default=100,
                help=('Priority for R930 nodes')),

    cfg.IntOpt('priority_r730', default=90,
                help=('Priority for R730 nodes')),

    cfg.IntOpt('priority_r630', default=50,
                help=('Priority for R630 nodes')),

    cfg.IntOpt('priority_r620', default=30,
                help=('Priority for R620 nodes')),

    cfg.IntOpt('priority_6048r', default=20,
                help=('Priority for 6048R nodes')),

    cfg.IntOpt('priority_6018r', default=10,
                help=('Priority for 6018R nodes')),

]

ceph_opts = [
    cfg.IntOpt('priority_r930', default=90,
                help=('Priority for R930 nodes')),

    cfg.IntOpt('priority_r730', default=50,
                help=('Priority for R730 nodes')),

    cfg.IntOpt('priority_r630', default=20,
                help=('Priority for R630 nodes')),

    cfg.IntOpt('priority_r620', default=10,
                help=('Priority for R620 nodes')),

    cfg.IntOpt('priority_6048r', default=100,
                help=('Priority for 6048R nodes')),

    cfg.IntOpt('priority_6018r', default=10,
                help=('Priority for 6018R nodes')),

]

compute_opts = [
    cfg.IntOpt('priority_r930', default=10,
                help=('Priority for R930 nodes')),

    cfg.IntOpt('priority_r730', default=20,
                help=('Priority for R730 nodes')),
    cfg.IntOpt('priority_r630', default=90,
                help=('Priority for R630 nodes')),

    cfg.IntOpt('priority_r620', default=100,
                help=('Priority for R620 nodes')),

    cfg.IntOpt('priority_6048r', default=50,
                help=('Priority for 6048R nodes')),

    cfg.IntOpt('priority_6018r', default=70,
                help=('Priority for 6018R nodes')),

]


CONF = cfg.CONF
CONF.register_group(control_group)
CONF.register_group(ceph_group)
CONF.register_group(compute_group)

CONF.register_opts(control_opts, control_group)
CONF.register_opts(ceph_opts, ceph_group)
CONF.register_opts(compute_opts, compute_group)

cli_opts = [
    cfg.StrOpt('cloud',
                short='c',
                required=True,
                default='cloud01',
                help='Name of cloud'),
    cfg.StrOpt('undercloud',
               short='uc',
               default=None,
               help='hostname of undercloud'),
    cfg.StrOpt('instackenv',
               short='i',
               default=None,
               help='path to instackenv'),
    cfg.StrOpt('templates',
               short='t',
               default=None,
               help='path to templates'),
    cfg.BoolOpt('query',
                short='q',
                default=False,
                help='Run script in query mode'),
    cfg.BoolOpt('debug',
                short='d',
                default=False,
                help='Print debugging output.'),
]
CONF.register_cli_opts(control_opts, control_group)
CONF.register_cli_opts(compute_opts, compute_group)
CONF.register_cli_opts(ceph_opts, ceph_group)
CONF.register_cli_opts(cli_opts)
