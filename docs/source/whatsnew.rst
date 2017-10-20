=========================
What's new in msgen 0.7.*
=========================

This version of msgen allows multiple file submission and adds new functionality for the ``list`` command. Previously, it was possible to
submit only a pair of FASTQ files or a single BAM file, and users had no options to control the output of the ``list`` command.

.. _new-functionality:

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
