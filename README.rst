msgen
=====
msgen is a command-line client for the Microsoft Genomics service.
You can find more detailed documentation for it here: https://msgen.readthedocs.io/

Release notes
-------------

1. Submitting multiple FASTQ or multiple BAM files.
2. Filtering options for the ``list`` command.
3. Range limiting options for the ``list`` command.
4. Export to CSV of the ``list`` command output.
5. Bug fixes!

This version of msgen also introduces user interface changes compared to version 0.6.*.
If you would like to keep using an older version, you can downgrade back
to 0.6.15 by running the following command:

::

  pip install msgen==0.6.15

Otherwise, you may want to scroll down to `Breaking changes`_.

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

   REM Windows console
   msgen list ^
     --api-url-base <Genomics API URL> ^
     --access-key   <Genomics account access key>

.. code-block:: sh

   # Unix console
   msgen list \
     --api-url-base <Genomics API URL> \
     --access-key   <Genomics account access key>

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

Breaking changes from 0.6.15
----------------------------
Specifying commands
~~~~~~~~~~~~~~~~~~~
Previously, the operation you wanted to invoke was a parameter to the ``-command`` option.  Now, the desired command directly follows
the program name, ``msgen``. Below is a table comparing invocations of msgen 0.6.* and 0.7.* for cases when a configuration file is
not used.

+------------------------------+----------------------------+
|msgen 0.6.* (without config)  |msgen 0.7.* (without config)|
+==============================+============================+
|``msgen -command submit …``   |``msgen submit …``          |
+------------------------------+----------------------------+
|``msgen -command list …``     |``msgen list …``            |
+------------------------------+----------------------------+
|``msgen -command getstatus …``|``msgen status …``          |
+------------------------------+----------------------------+
|``msgen -command cancel …``   |``msgen cancel …``          |
+------------------------------+----------------------------+

Commands cannot be specified in the configuration file anymore and will be ignored if mentioned there. Below is a table comparing
invocations between msgen 0.6.* and 0.7.* for cases when a configuration file is used.

+--------------------------+------------------------------------+--------------------------------+
|Command in the config file|msgen 0.6.* (with command in config)|msgen 0.7.* (with config)       |
+==========================+====================================+================================+
|*command: submit*         |``msgen -f config.txt …``           |``msgen submit -f config.txt …``|
+--------------------------+------------------------------------+--------------------------------+
|*command: list*           |``msgen -f config.txt …``           |``msgen list -f config.txt …``  |
+--------------------------+------------------------------------+--------------------------------+
|*command: getstatus*      |``msgen -f config.txt …``           |``msgen status -f config.txt …``|
+--------------------------+------------------------------------+--------------------------------+
|*command: cancel*         |``msgen -f config.txt …``           |``msgen cancel -f config.txt …``|
+--------------------------+------------------------------------+--------------------------------+

Specifying other arguments
~~~~~~~~~~~~~~~~~~~~~~~~~~
Using the command line
^^^^^^^^^^^^^^^^^^^^^^
If you provide at least some required information via the command line arguments when interacting with the Microsoft Genomics service,
you will need to update your command invocation. All arguments are now provided either in the short format like ``-k`` or in the long
format like ``--access-key``. Note that arguments in the long format start with a double dash and that underscores between words
are replaced with dashes. Below is a table listing some of the submit arguments to illustrate this difference between msgen 0.6.* and
0.7.*.

+-------------------------------------+------------------------------------------+
|msgen 0.6.*                          |msgen 0.7.*                               |
+=====================================+==========================================+
|``-api_url_base``                    |``-u/--api-url-base``                     |
+-------------------------------------+------------------------------------------+
|``-subscription_key``                |``-k/--access-key``                       |
+-------------------------------------+------------------------------------------+
|``-input_storage_account_name``      |``-ia/--input-storage-account-name``      |
+-------------------------------------+------------------------------------------+
|``-input_storage_account_key``       |``-ik/--input-storage-account-key``       |
+-------------------------------------+------------------------------------------+
|``-input_storage_account_container`` |``-ic/--input-storage-account-container`` |
+-------------------------------------+------------------------------------------+
|``-input_blob_name_1``               |``-b1/--input-blob-name-1``               |
+-------------------------------------+------------------------------------------+
|``-input_blob_name_2``               |``-b2/--input-blob-name-1``               |
+-------------------------------------+------------------------------------------+
|``-output_storage_account_name``     |``-oa/--output-storage-account-name``     |
+-------------------------------------+------------------------------------------+
|``-output_storage_account_key``      |``-ok/--output-storage-account-key``      |
+-------------------------------------+------------------------------------------+
|``-output_storage_account_container``|``-oc/--output-storage-account-container``|
+-------------------------------------+------------------------------------------+
|``-process_args``                    |``-pa/--process-args``                    |
+-------------------------------------+------------------------------------------+

Using the configuration file
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
There are no changes here, apart from the fact that the command is going to be ignored and will need to be provided on the command line.
Your old configuration file can be re-used for all commands you want to use it with.

.. _Breaking changes: #breaking-changes-from-0615