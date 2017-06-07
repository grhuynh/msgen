=========================
What's new in msgen 0.7.0
=========================

This version of msgen introduced user interface changes. This document explains what to expect, what changes you must make, and
the new functionality for this release. If you have installed msgen for the first time, you can skip the breaking changes section and
go straight to :ref:`new-functionality`. If you would like to keep using an older version, you can downgrade back to 0.6.15 by running the
following command:

::

  pip install msgen==0.6.15

.. _breaking-changes:

Breaking changes
----------------
Specifying commands
~~~~~~~~~~~~~~~~~~~
Previously, the operation you wanted to invoke was a parameter to the ``-command`` option.  Now, the desired command directly follows
the program name, ``msgen``. Below is a table comparing invocations of msgen 0.6.* and 0.7.0 for cases when a configuration file is
not used.

.. cssclass:: table-bordered

+------------------------------+----------------------------+
|msgen 0.6.* (without config)  |msgen 0.7.0 (without config)|
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
invocations between msgen 0.6.* and 0.7.0 for cases when a configuration file is used.

.. cssclass:: table-bordered

+--------------------------+------------------------------------+--------------------------------+
|Command in the config file|msgen 0.6.* (with command in config)|msgen 0.7.0 (with config)       |
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
format like ``--subscription-key``. Note that arguments in the long format start with a double dash and that underscores between words
are replaced with dashes. Below is a table listing some of the submit arguments to illustrate this difference between msgen 0.6.* and
0.7.0.

.. cssclass:: table-bordered

+-------------------------------------+------------------------------------------+
|msgen 0.6.*                          |msgen 0.7.0                               |
+=====================================+==========================================+
|``-api_url_base``                    |``-u/--api-url-base``                     |
+-------------------------------------+------------------------------------------+
|``-subscription_key``                |``-k/--subscription-key``                 |
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

.. _new-functionality:

New functionality
-----------------
This version of msgen allows multiple file submission and adds new functionality for the ``list`` command. Previously, it was possible to
submit only a pair of FASTQ files or a single BAM file, and users had no options to control the output of the ``list`` command.

Submitting multiple FASTQ or multiple BAM files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can now submit multiple FASTQ files or multiple BAM files at once, if they come from the same sample. Note that you still cannot
mix FASTQ and BAM files in the same submission, even if they originate from the same sample; you would have to bring them all to a single
format. Instructions on how to submit multiple files are here: :ref:`submit-multiple`

Filtering options
~~~~~~~~~~~~~~~~~
You can now filter completed workflows by their outcome and all workflows by their description and process name. Below is a table showing
all filtering options.

.. cssclass:: table-bordered

+-------------------------------------+----------------------------------------------------------------------------+
|Argument of the ``list`` command     |Explanation                                                                 |
+=====================================+============================================================================+
|``-o/--outcome`` ``fail`` \| ``pass``|Show only completed workflows that failed (``fail``) or succeeded (``pass``)|
+-------------------------------------+----------------------------------------------------------------------------+
|``-d/--with-description`` *substring*|Show any workflows that contain *substring* in their description            |
+-------------------------------------+----------------------------------------------------------------------------+
|``-p/--with-process`` *substring*    |Show any workflows that contain *substring* in their process name           |
+-------------------------------------+----------------------------------------------------------------------------+

Range limiting options
~~~~~~~~~~~~~~~~~~~~~~
You can now limit the list of workflows returned by the service using a Python-like slice notation. Imagine that all your workflows
constitute a list starting with the oldest workflow and ending with the most recently submitted one. In that case, your oldest workflow will
have index *0*, and your most recent, index *-1*. Here are some examples.

.. cssclass:: table-bordered

+------------------------+-------------------------------------------------------------------------------------------------+
|Value of -r/--in-range  |Explanation                                                                                      |
+========================+=================================================================================================+
|``-r/--in-range :10``   |List ten oldest workflows                                                                        |
+------------------------+-------------------------------------------------------------------------------------------------+
|``-r/--in-range -10:``  |List ten most recent workflows                                                                   |
+------------------------+-------------------------------------------------------------------------------------------------+
|``-r/--in-range 1:10``  |List nine workflows starting from the second oldest                                              |
+------------------------+-------------------------------------------------------------------------------------------------+
|``-r/--in-range -10:-1``|List nine workflows starting from the tenth most recent and excluding the very last one submitted|
+------------------------+-------------------------------------------------------------------------------------------------+
|``-r/--in-range 0``     |List only the first workflow                                                                     |
+------------------------+-------------------------------------------------------------------------------------------------+
|``-r/--in-range -1``    |List only the last workflow                                                                      |
+------------------------+-------------------------------------------------------------------------------------------------+
|``-r/--in-range 5:-5``  |Error; such values are not allowed                                                               |
+------------------------+                                                                                                 |
|``-r/--in-range -5:5``  |                                                                                                 |
+------------------------+                                                                                                 |
|``-r/--in-range 5:15:2``|                                                                                                 |
+------------------------+-------------------------------------------------------------------------------------------------+

Note that this notation is not as powerful as the full Python slice notation. For example, we do not accept increments, and you can only work
with one end of the range at a time, i.e. either with the most recent workflows or with the oldest ones.

Another important thing is that range is applied after filtering. For example, if your command line includes these arguments, ``-o fail -r -10:``,
first, all failing workflows will be selected, and then the ten most recent of those will be returned.

Export to CSV
~~~~~~~~~~~~~
You can now save a list of workflows into the CSV format. You can either print it to the screen or save it to a file.

.. cssclass:: table-bordered

+--------------------------------+------------------------------------------------------------------------------------------------------------+
|Argument of the ``list`` command|Explanation                                                                                                 |
+================================+============================================================================================================+
|``-e/--export-to csv``          |Currently, the only allowed value is ``csv``. If this option is omitted, the list will be printed as before.|
+--------------------------------+------------------------------------------------------------------------------------------------------------+
|``-of/--output-file`` *file*    |Saves output (CSV or plaintext) to a given *file*.                                                          |
+--------------------------------+------------------------------------------------------------------------------------------------------------+
