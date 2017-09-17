Dokku AWS
=========

This is a simple CloudFormation stack for deploying a `Dokku <http://dokku.viewdocs.io/dokku/>`_
instance to EC2 using an Ubuntu 16.04 LTS AMI. The instance is configured with an Elastic IP, so the
IP will stay the same in case of stack updates that require the instance to be replaced.

The CloudFormation templates are written in `troposphere <https://github.com/cloudtools/troposphere>`_,
which allows for some validation at build time and simplifies the management of several related
templates.

You can launch a new instance by clicking the Launch Stack button below or by pointing CloudFormation
to the `underlying template`_ manually.

|dokku-stack|_

.. |dokku-stack| image:: https://s3.amazonaws.com/cloudformation-examples/cloudformation-launch-stack.png
.. _dokku-stack: https://console.aws.amazon.com/cloudformation/home?#/stacks/new?stackName=my-dokku-stack&templateURL=https://s3.amazonaws.com/dokku-aws/dokku_stack.json
.. _underlying template: https://s3.amazonaws.com/dokku-aws/dokku_stack.json

For help deploying to your new instance after it's created, please refer to the `Dokku documentation 
<http://dokku.viewdocs.io/dokku/deployment/application-deployment/>`_.

Copyright 2017 Tobias McNulty.
