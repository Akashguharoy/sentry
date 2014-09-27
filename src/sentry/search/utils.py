from __future__ import absolute_import, division, print_function

from sentry.constants import STATUS_CHOICES
from sentry.utils.auth import find_users


def parse_query(query, user):
    # TODO(dcramer): make this better
    tokens = query.split(' ')

    results = {'tags': {}, 'query': []}

    tokens_iter = iter(tokens)
    for token in tokens_iter:
        if ':' not in token:
            results['query'].append(token)
            continue

        key, value = token.split(':', 1)
        if value[0] == '"':
            nvalue = value
            while nvalue[-1] != '"':
                try:
                    nvalue = tokens_iter.next()
                except StopIteration:
                    break
                value = '%s %s' % (value, nvalue)

            if value.endswith('"'):
                value = value[1:-1]

        if key == 'is':
            try:
                results['status'] = STATUS_CHOICES[value]
            except KeyError:
                pass
        elif key == 'assigned':
            if value == 'me':
                results['assigned_to'] = user
            else:
                try:
                    results['assigned_to'] = find_users(value)[0]
                except IndexError:
                    pass
        else:
            results['tags'][key] = value

    results['query'] = ' '.join(results['query'])

    return results
