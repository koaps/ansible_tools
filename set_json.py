#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Koaps
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule

import json

try:
    import jsonpointer
except ImportError:
    jsonpointer = None

def main():
    module = AnsibleModule(
        argument_spec=dict(
            data=dict(required=True, type='dict'),
            set_data=dict(type='json'),
        ),
        supports_check_mode=True,
    )

    if jsonpointer is None:
        module.fail_json(msg='jsonpointer module is not available')

    data = module.params['data']
    j_data = json.loads(module.params['set_data'])

    for j in j_data:
        pointer = "/{}".format(j)
        s_data = j_data[j]

        msg = ("pointer: {} set_data: {}".format(pointer, s_data))

        try:
            data = jsonpointer.set_pointer(data, pointer, s_data)
        except jsonpointer.JsonPointerException as err:
            module.fail_json(msg=str(err))

    module.exit_json(changed=True, result=data)

if __name__ == '__main__':
    main()
