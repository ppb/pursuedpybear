#!/usr/bin/xonsh
$XONSH_SHOW_TRACEBACK = True

import sys
sys.path.insert(0, "/opt/action")


source /etc/xonshrc
import tags

import urllib

HACKTOBERFEST_LABEL = "Hacktoberfest"


import gqlmod.providers
assert gqlmod.providers.get_provider('github').token, "No token on provider"


if $GITHUB_EVENT['action'] == 'rerequested':
    sys.exit("Cannot process a rerun request (original event is lost)")
elif $GITHUB_EVENT['action'] == 'deleted':
    # Do nothing; issue is gone.
    sys.exit()

issue_id = $GITHUB_EVENT['issue']['node_id']
labels = {
    # node id: name
    l['node_id']: l['name']
    for l in $GITHUB_EVENT['issue']['labels']
}

print("Found labels", ', '.join(labels.values()))

has_followed = bool($INPUT['LABEL'] in labels.values())
has_hacktoberfest = bool(HACKTOBERFEST_LABEL in labels.values())


if has_followed == has_hacktoberfest:
    print("No changes needed")
    sys.exit()

if not has_followed and has_hacktoberfest:
    print(f"Removing label: {HACKTOBERFEST_LABEL}")
    # Remove the hacktoberfest label
    hack_label_id = next(k for k, v in labels if v == HACKTOBERFEST_LABEL)
    res = tags.del_label(label=hack_label_id, target=issue_id)
    assert not res.errors, repr(res.errors)

elif has_followed and not has_hacktoberfest:
    print(f"Adding label: {HACKTOBERFEST_LABEL}")
    # Add the hacktoberfest label
    try:
        res = tags.get_label(repo=$GITHUB_EVENT['repository']['node_id'], name=HACKTOBERFEST_LABEL)
    except urllib.error.HTTPError as exc:
        print(exc.read())
        raise
    assert not res.errors, repr(res.errors)
    hack_label_id = res.data['node']['label']['id']
    res = tags.add_label(label=hack_label_id, target=issue_id)
    assert not res.errors, repr(res.errors)

else:
    raise RuntimeError("No idea how we got here.")
