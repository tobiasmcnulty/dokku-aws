#!/usr/bin/env python
# Convenience code for generating copy/pastable Python code describing Xenial AMIs by region, for dokku_stack.py

import json
import re
from urllib import request

with request.urlopen('https://cloud-images.ubuntu.com/locator/ec2/releasesTable') as response:
    data = json.loads(response.read().decode('utf-8').replace('],\n]', ']\n]'))  # remove extra trailing comma

amis = []
for region, dname, _, arch, rootdev, _, link, _ in data['aaData']:
    if dname == 'xenial' and arch == 'amd64' and rootdev == 'hvm:ebs-ssd':
        ami = re.search('>([a-zA-Z0-9-]+)<', link).group(1)
        amis.append('    "%s": {"AMI": "%s"},' % (region, ami))

amis.sort()
print('\n'.join(amis))
