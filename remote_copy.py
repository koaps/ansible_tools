#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright: (c) 2017, Koaps
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = '''
---
module: remote_copy
short_description: Remote recursive copy
'''

from ansible.module_utils.basic import AnsibleModule

import shutil
import os

def copyfile(src, dst, changed=False, result=[]):
  if not os.path.exists(dst) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
    shutil.copy2(src, dst)
    result.append(dst)
    changed = True
  return changed, result

def copytree(src, dst, changed=False, result=[]):
  if os.path.isdir(src):
    if not os.path.exists(dst):
      os.makedirs(dst)
      result.append(dst)
      changed = True
    for item in os.listdir(src):
      s = os.path.join(src, item)
      d = os.path.join(dst, item)
      if os.path.isdir(s):
        changed, result = copytree(s, d, changed, result)
      else:
        changed, result = copyfile(s, d, changed, result)
  else:
    changed, result = copyfile(src, dst, changed, result)
  return changed, result

def main():
  module = AnsibleModule(
    argument_spec=dict(
      dest=dict(required=True, type='str'),
      src=dict(required=True, type='str')
    ),
    supports_check_mode=False,
  )

  dest = module.params['dest']
  src = module.params['src']

  changed, result = copytree(src, dest)

  if changed:
    module.exit_json(changed=True, msg="files copied successfully", meta=result)
  else:
    module.exit_json(changed=False, msg="no files changed", meta=result)

if __name__ == '__main__':
  main()
