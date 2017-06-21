# -*- coding: utf-8 -*-

import re
import io
from enum import Enum
from oam.daylog import oamlog_write, get_errstream, timestamp, get_logfile

Tag = Enum('Tag', 'deansi dedot default multi timestamp dats')

LOGDEST = [
    ('eix-update',          'sync',   'error',   '- dats  -'),
    ('eix-remote',          'sync',   '-',       '- -     dats'),
    ('emaint --auto sync',  'sync',   'error',   '- dats  -'),
    ('layman',              'sync',   '-',       '- -     -'),
    ('glsa-check'           'glsa',   '-',       '- -     -'),
    ('emerge --fetchonly',  'merge',  'blocks',  '- dedot multi'),
    ('emerge',              'merge',  'blocks',  '- -     multi'),
    ('revdep-rebuild',      'merge',  'error'    '- -     -'),
    ('python-updater',      'merge',  'error',   '- -     -'),
    ('perl-cleaner',        'merge',  'error',   '- -     -'),
    ('eclean',              'clean',  'error',   '- dats  -'),
    ('xargs --verbose',     'expire', '-',       '- -     -'),
    ('default-catchall',    'misc',   'error',   '- -     -')
]

ANSI = r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?'

def dats(ins, outs):
    """filter out ansi escape code sequences"""
    ansi_filter = re.compile(ANSI)
    for line in ins:
        line = ansi_filter.sub('', line)
        outs.write('{} {}'.format(timestamp(), line))
        outs.flush()

def dedot(ins, outs):
    """pass through any line which doesn't contain '...'"""
    for line in ins:
        if not '...' in line:
            outs.write(line)
            outs.flush()

class LogSupervisor(object):

    def __init__(self):
        self.threads = []

    def finish(self):
        for thd in self.threads:
            thd.join()

    def do_wrap(self, stream, target):
        wrapstream = io.StringIO()
        thd = Thread(target=target, args=[wrapstream, stream])
        self.threads.add(thd)
        thd.start()
        return wrapstream

    def wrap(self, stream, tags):
        for tag in tags.split(','):
            if tag == 'dedot':
                stream = self.do_wrap(stream, dedot)
            elif tag == 'dats':
                stream = self.do_wrap(stream, dats)
        return stream

    def logdest(self, cmd):
        """Return a tuple of two open streams which can be used to log
           stdout, stderr from the cmd.
        """
        dest = self.classify(cmd)
        mergelog = 'multi' in dest[3]
        tags = dest[3].split(' ')

        stdout = open(get_logfile(dest[1], mergelog=mergelog), 'a')
        stdout = self.wrap(stdout, ','.join(tags[1:]))
        if dest[2] == '-':
            stderr = stdout
        else:
            stderr = open(get_logfile(dest[2], mergelog=mergelog), 'a')
            stderr = self.wrap(stderr, ','.join([tags[0], tags[2]]))

        return stdout, stderr

    def classify(self, cmd):
        for match in LOGDEST:
            if match[0] in cmd:
                return match
        return LOGDEST[-1]

LOGSUPERVISOR = LogSupervisor()

def logdest(cmd):
    return LOGSUPERVISOR.logdest(cmd)

def finish():
    return LOGSUPERVISOR.finish()
