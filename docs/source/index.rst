==========================
Getting started with msgen
==========================

msgen is a command-line client for the Microsoft Genomics service.

On this site
------------
.. toctree::
   :maxdepth: 1

   self
   whatsnew
   faq
   migration

Installation
------------
msgen is compatible with Python 2.7. We recommend using version 2.7.12 or later. msgen can be installed from PyPI.

Linux
~~~~~
::

  sudo apt-get install -y build-essential libssl-dev libffi-dev libpython-dev python-dev python-pip
  sudo pip install --upgrade --no-deps msgen
  sudo pip install msgen

Windows
~~~~~~~
::

  pip install --upgrade --no-deps msgen
  pip install msgen


If you do not want to install msgen as a system-wide binary and modify system-wide python packages, use the
``--user`` flag with ``pip``. In that case you will need to add ``~/.local/bin`` to your path in Linux and
``%APPDATA%\Python`` in Windows.

Basic requirements
~~~~~~~~~~~~~~~~~~~
* `azure-storage`_
* `requests`_

You can install these packages using pip, easy_install or through standard
setup.py procedures. These dependencies will be automatically installed if
using a package-based installation or setup.py. The required versions of these
dependent packages can be found in ``setup.py``.

.. _azure-storage: https://pypi.python.org/pypi/azure-storage
.. _requests: https://pypi.python.org/pypi/requests


Basic usage
-----------
After installing msgen, a simple command to check connectivity is:

.. code-block:: bat
   :caption: Windows console

   msgen list ^
     --api-url-base     <Genomics API URL> ^
     --subscription-key <Genomics account access key>

.. code-block:: sh
   :caption: Unix console

   msgen list \
     --api-url-base     <Genomics API URL> \
     --subscription-key <Genomics account access key>

Values for both these arguments can be found in Azure Portal, on the Access keys blade of your Genomics account.

You can get a full list of available commands and arguments by running ``msgen help``, but generally you will
need to provide at least a command, ``--api-url-base``, and ``--access-key``, where the command is one
of the following:

==========  =====
``list``    Returns a list of jobs you have submitted. For arguments, see ``msgen help list``.
``submit``  Submits a workflow request to the service. For arguments, see ``msgen help submit``.
``status``  Returns the status of the workflow specified by ``--workflow-id``. See also ``msgen help status``.
``cancel``  Sends a request to cancel processing of the workflow specified by ``--workflow-id``. See also ``msgen help cancel``.
==========  =====

See also: :ref:`submit-fastq` and :ref:`config-file`