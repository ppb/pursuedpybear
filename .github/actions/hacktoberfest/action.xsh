#!/usr/bin/xonsh
import sys
sys.path.insert(0, "/opt/action")


source /etc/xonshrc
import tags

HACKTOBERFEST_LABEL = "Hacktoberfest"


if $GITHUB_EVENT['action'] == 'deleted':
    sys.exit()


issue_id = $GITHUB_EVENT['issue']['node_id']
labels = {
    # node id: name
    l['node_id']: l['name']
    for l in $GITHUB_EVENT['issue']['labels']
}

has_followed = bool($INPUT['label'] in labels.values())
has_hacktoberfest = bool(HACKTOBERFEST_LABEL in labels.values())

if has_followed == has_hacktoberfest:
    print("No changes needed")
    sys.exit()

if not has_followed and has_hacktoberfest:
    # Remove the hacktoberfest label
    hack_label_id = next(k for k, v in labels if v == HACKTOBERFEST_LABEL)
    res = tags.del_label(label=hack_label_id, target=issue_id)
    assert not res.errors, repr(res.errors)

elif has_followed and not has_hacktoberfest:
    # Add the hacktoberfest label
    res = tags.get_label(repo=$GITHUB_EVENT['repository']['node_id'], name=HACKTOBERFEST_LABEL)
    assert not res.errors, repr(res.errors)
    hack_label_id = res.data['node']['label']['id']
    res = tags.add_label(label=hack_label_id, target=issue_id)
    assert not res.errors, repr(res.errors)

else:
    raise RuntimeError("No idea how we got here.")
