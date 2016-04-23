
import logging

OAM_VERBOSE="--verbose --verbose-conflicts"
OAM_EMERGE_OPTS="--backtrack=50 --deep "

steps = {
    'sync': {
        'cmd': 'emaint --auto sync',
        'log': 'sync',               # portage step checks this log to see if portage should be merged first
        'exclude': ['lxcs']
        },
    'layman': {
        'cmd': 'layman --sync=ALL --nocolor',
        'log': 'layman'
        },
    'eix': {
        'cmd': 'eix-update --nocolor',
        'log': 'eix'
        },
    'glsa': {
        'cmd': 'glsa-check --test --verbose --nocolor all',
        'log': 'security',
        'level': logging.WARNING
        },
    'fetch': {
        'cmd': 'emerge --fetchonly {} --update world'.format(OAM_EMERGE_OPTS),
        'log': 'fetch',
        'exclude': ['lxcs']
        },
    'portage': {
        'cmd': 'emerge --update {} sys-apps/portage'.format(OAM_VERBOSE),
        'log': 'merge'
        },
    'update': {
        'cmd': 'emerge {} {} --update world'.format(OAM_EMERGE_OPTS. OAM_VERBOSE),
        'log': 'merge'
        },
    'revdep': {
        'cmd': 'revdep-rebuild --nocolor --ignore',
        'log': 'revdep'
        },
    'python': {
        'cmd': 'python-updater -eall',
        'log': 'python'
        },
    'perl': {
        'cmd': 'perl-cleaner --all',
        'log': 'perl'
        },
    'preserved': {
        'cmd': 'emerge --keep-going {} @preserved-rebuild'.format(OAM_VERBOSE),
        'log': 'merge'
        },
    'eclean-distfiles': {
        'cmd': 'eclean --nocolor distfiles',
        'log': 'clean',
        'exclude': ['lxcs']
        },
    'eclean-kernel': {
        'cmd': 'eclean-kernel --num=3 --exclude=config --no-mount',
        'log': 'clean',
        'exclude': ['lxcs']
        },
    'qcheck': {
        'cmd': "qcheck --all --nomtime --nocolor | egrep 'AKF|MD5-DIGEST' | sort",
        'log': 'qcheck'
        },
    }

flows = {
    'sync'  : ['sync', 'layman', 'eix', 'glsa', 'fetch' ],
    'update': ['portage', 'update', 'revdep', 'python', 'perl', 'preserved'],
    'clean' : ['eclean-distfiles', 'eclean-kernel'. 'qcheck']
    }

flows['weekly'] = flows['sync'] + flows['update'] + flows['clean']

flows['officenet'] = [
    [flows['sync']],
    [flows['update'], {'server1': flows['weekly'] } ]
    [flows['clean']],
]
