Dokku AWS
=========

This is a simple CloudFormation stack for deploying a `Dokku <http://dokku.viewdocs.io/dokku/>`_
instance to EC2 using an Ubuntu 16.04 LTS AMI. The instance is configured with an Elastic IP, so the
IP will stay the same in case of stack updates that require the instance to be replaced.

If you wish to use your Dokku instance with S3, RDS, ElastiCache, and/or Elasticsearch, you should
use `aws-web-stacks <https://github.com/caktus/aws-web-stacks>`_ instead.

The CloudFormation templates are written in `troposphere <https://github.com/cloudtools/troposphere>`_,
which allows for some validation at build time and simplifies the management of several related
templates.

You can launch a new instance by clicking the Launch Stack button below or by pointing CloudFormation
to the `underlying template`_ manually. Before launching a stack, make sure to upload your SSH public key
to the `Key Pairs <https://console.aws.amazon.com/ec2/v2/home#KeyPairs:sort=keyName>`_ section of the
AWS console (this will be used both to allow logins to the ``ubuntu`` user on your EC2 instance and
to allow deploys via the ``dokku`` user).

|dokku-stack|_

.. |dokku-stack| image:: https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png
.. _dokku-stack: https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=my-dokku-stack&templateURL=https://s3.amazonaws.com/dokku-aws/dokku_stack.json
.. _underlying template: https://s3.amazonaws.com/dokku-aws/dokku_stack.json

Using the default values in this template (a ``t2.micro`` instance and 30 GB of disk space), your new
Dokku instance should fit within the `free tier <https://aws.amazon.com/free/>`_ on AWS.

DNS
---

After the stack is created, you'll want to inspect the Outputs for the PublicIP of the instance and
create a DNS ``A`` record (possibly including a wildcard record, if you're using vhost-based apps)
for your chosen domain.

For help creating a DNS record, please refer to the `Dokku DNS documentation
<http://dokku.viewdocs.io/dokku/configuration/dns/>`_.

Deployment
----------

Dokku may take 5-10 minutes to install, even after the stack has finished creating. Once that's complete,
create a new app on the remote server::

    ssh dokku@<your domain or IP> apps:create python-sample

and deploy Heroku's Python sample to that app::

    git clone https://github.com/heroku/python-sample.git
    cd python-sample
    git remote add dokku dokku@<your domain or IP>:python-sample
    git push dokku master

You should be able to watch the build complete in the output from the ``git push`` command. If the
deploy completes successfully, you should be able to see "Hello world!" at
http://python-sample.your.domain/

For additional help deploying to your new instance, please refer to the `Dokku documentation
<http://dokku.viewdocs.io/dokku/deployment/application-deployment/>`_.

Let's Encrypt
-------------

We might as well get a free SSL certificate from Let's Encrypt, while we're at it::

    ssh ubuntu@<your domain or IP> sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
    ssh dokku@<your domain or IP> config:set --no-restart python-sample DOKKU_LETSENCRYPT_EMAIL=your@email.tld
    ssh dokku@<your domain or IP> letsencrypt python-sample

The Python sample app should now be accessible over HTTPS at https://python-sample.your.domain/

Good luck and have fun!

Copyright 2017 Tobias McNulty.
