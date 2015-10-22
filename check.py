#!/usr/bin/env python
import sys
import logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


with open(sys.argv[1], 'r') as handle:
    retcode = 0
    for lineno, line in enumerate(handle):
        if line.startswith('#'):
            continue

        try:
            data = line.split('\t')
            if len(data) == 5:
                log.error("[%s] Line less than 6 columns", lineno)
                retcode = 1

            if len(data) != 6:
                log.error("[%s] %s columns != 6 columns", len(data), lineno)
                retcode = 1

            keys = ['id', 'platform', 'arch', 'url', 'sha', 'alt_url']
            ld = {k: v for (k, v) in zip(keys, data)}

            for x in keys[0:5]:
                if ld.get(x, '').strip() == '':
                    log.error("[%s] Empty %s", lineno, x)
                    retcode = 1

            if ld['platform'] not in ('linux', 'windows', 'darwin', 'src'):
                log.error("[%s] Unknown platform %s", lineno, ld['platform'])
                retcode = 1

            if ld['arch'] not in ('x32', 'x64', 'all'):
                log.error("[%s] Unknown architecture %s", lineno, ld['arch'])
                retcode = 1

            if len(ld['sha']) != 64:
                log.error("[%s] Bad checksum %s", lineno, ld['sha'])
                retcode = 1

        except:
            log.error("[%s] Line not tabbed properly", lineno)
            retcode = 1
    sys.exit(retcode)