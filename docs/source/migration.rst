=====================================
Migration from version 0.6.* to 0.7.*
=====================================

Version 0.7.0 of msgen introduced user interface changes. This document explains what to expect and what changes you must makeif you have 
been using version 0.6.* before. If you would like to keep using an older version, you can downgrade back to 0.6.15 by running the
following command:

::

  pip install msgen==0.6.15

.. _breaking-changes:

Breaking changes
----------------
Specifying commands
~~~~~~~~~~~~~~~~~~~
Previously, the operation you wanted to invoke was a parameter to the ``-command`` option.  Now, the desired command directly follows
the program name, ``msgen``. Below is a table comparing invocations of msgen 0.6.* and 0.7.* for cases when a configuration file is
not used.

.. cssclass:: table-bordered

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

.. cssclass:: table-bordered

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

.. cssclass:: table-bordered

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