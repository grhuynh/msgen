==========================
Frequently asked questions
==========================

My commands stopped working after upgrading. What do I do?
----------------------------------------------------------
Most likely you have upgraded from msgen 0.6.* to 0.7.0. Please see the :ref:`breaking-changes` section for guidance. You can also downgrade to a previous
version by running the following command:

::

  pip install msgen==[version.to.use]

For example, the following command will install version 0.6.15:

::

  pip install msgen==0.6.15

Where do I get the value for ``--api-url-base``?
------------------------------------------------
During the preview, please use https://malibutest0044.azure-api.net. After the preview, there will be a new URL provided.

Where do I get the value for ``--subscription-key``?
----------------------------------------------------
Navigate to https://malibutest0044.portal.azure-api.net and log in to the Microsoft Genomics API portal. Click your name in
the top right corner of the page and choose *Profile*. You will see subscription details for the Microsoft Genomics service.
You need to provide either the primary or secondary key for the value of ``--subscription-key`` (highlighted in orange on the screenshot).

.. image:: _static/subscription-key.png

How do I upload files to Azure?
-------------------------------
The Microsoft Genomics service expects inputs to be stored as block blobs in an Azure storage account. It will also write output files as block blobs to
a user-specified container in an Azure storage account. The inputs and outputs can reside in different storage accounts.

Before using msgen, you will need to create a storage account or two in your Azure subscription and upload files there. If it’s
the first time you are doing it, you can use a tool like `Azure Storage Explorer <http://storageexplorer.com/>`_. Here are some links to get you started:

1. `Create a storage account <https://docs.microsoft.com/en-us/azure/storage/storage-create-storage-account>`_ — explains what a storage account is, what
   services it provides, and how to create one.
2. `Getting started with Storage Explorer <https://docs.microsoft.com/en-us/azure/vs-azure-tools-storage-manage-with-storage-explorer>`_ — explains how to
   connect to your storage account with Azure Storage Explorer and where to find storage account keys.
3. `Manage Azure Blob Storage resources with Storage Explorer <https://docs.microsoft.com/en-us/azure/vs-azure-tools-storage-explorer-blobs>`_ — explains
   how to create containers and upload blobs using Azure Storage Explorer.

Please make sure that you upload your files as **block blobs**. This is the most suitable type of blobs for the kind of processing we do and is expected
by the Microsoft Genomics service.

Why do you need my storage account keys?
----------------------------------------
msgen doesn’t send your storage account keys anywhere. Instead, they are used to create short-term access tokens for the Microsoft Genomics service to read
input files and to write outputs. The default token duration is 48 hours and can be changed with the ``-sas/--sas-duration`` option of the ``submit`` command;
the value is in hours.

.. _submit-fastq:

How do I submit a pair of FASTQ files for processing?
-----------------------------------------------------
Let’s assume you have two files, *reads_1.fq.gz* and *reads_2.fq.gz*, and you have uploaded them to your storage account *myaccount* in Azure as
https://myaccount.blob.core.windows.net/inputs/reads_1.fq.gz and https://myaccount.blob.core.windows.net/inputs/reads_2.fq.gz. You have the API URL and your API
subscription key. You want to have outputs in https://myaccount.blob.core.windows.net/outputs. 

Here is the minimal set of arguments that you will need to provide; line breaks are added for clarity:

.. code-block:: bat
   :caption: Windows console

   msgen submit ^
     --api-url-base https://malibutest0044.azure-api.net ^
     --subscription-key <API subscription key> ^
     --process-args R=grch37bwa ^
     --input-storage-account-name myaccount ^
     --input-storage-account-key <access key to "myaccount"> ^
     --input-storage-account-container inputs ^
     --input-blob-name-1 reads_1.fq.gz ^
     --input-blob-name-2 reads_2.fq.gz ^
     --output-storage-account-name myaccount ^
     --output-storage-account-key <access key to "myaccount"> ^
     --output-storage-account-container outputs

.. code-block:: sh
   :caption: Unix console

   msgen submit \
     --api-url-base https://malibutest0044.azure-api.net \
     --subscription-key <API subscription key> \
     --process-args R=grch37bwa \
     --input-storage-account-name myaccount \
     --input-storage-account-key <access key to "myaccount"> \
     --input-storage-account-container inputs \
     --input-blob-name-1 reads_1.fq.gz \
     --input-blob-name-2 reads_2.fq.gz \
     --output-storage-account-name myaccount \
     --output-storage-account-key <access key to "myaccount"> \
     --output-storage-account-container outputs

If you prefer using a configuration file, here is what it would contain:

.. code-block:: yaml
   :caption: config.txt

   api_url_base:                     https://malibutest0044.azure-api.net
   subscription_key:                 <API subscription key>
   process_args:                     R=grch37bwa
   input_storage_account_name:       myaccount
   input_storage_account_key:        <access key to "myaccount">
   input_storage_account_container:  inputs
   input_blob_name_1:                reads_1.fq.gz
   input_blob_name_2:                reads_2.fq.gz
   output_storage_account_name:      myaccount
   output_storage_account_key:       <access key to "myaccount">
   output_storage_account_container: outputs

And you would submit it with this invocation: ``msgen submit -f config.txt``.

How do I submit a BAM file for processing?
------------------------------------------
The basics are the same as when submitting FASTQ files, but you will provide only one input file, as
a value of the ``-b1/--input-blob-name-1`` argument.

.. _submit-multiple:

.. role:: orange

.. role:: green

.. role:: blue

How do I submit *multiple* FASTQ and BAM files for processing?
--------------------------------------------------------------
Starting with the version 0.7.0, msgen lets you submit multiple FASTQ or BAM files coming from the same
sample. Keep in mind, however, that you **cannot mix FASTQ and BAM files in the same submission**.

FASTQ files
===========

Let’s say you have these six FASTQ files **all coming from the same sample** and uploaded to your storage
account *myaccount* in Azure:

* :orange:`ERR194158_1.fastq.gz`
* :orange:`ERR194158_2.fastq.gz`
* :green:`ERR194159_1.fastq.gz`
* :green:`ERR194159_2.fastq.gz`
* :blue:`ERR194160_1.fastq.gz`
* :blue:`ERR194160_2.fastq.gz`

Note that files highlighted with the same color form pairs; these are files with paired reads and
should be processed together. Below are examples of how you would do that when submitting from a command line
in Windows, in Unix, and using a configuration file. Note the order of file names when they are 
passed to arguments ``-b1/--input-blob-name-1`` and ``-b2/--input-blob-name-2``. Line breaks are
added for clarity.

.. code-block:: bat
   :caption: Windows console

   msgen submit ^
     --api-url-base https://malibutest0044.azure-api.net ^
     --subscription-key <API subscription key> ^
     --process-args R=grch37bwa ^
     --input-storage-account-name myaccount ^
     --input-storage-account-key <access key to "myaccount"> ^
     --input-storage-account-container inputs ^
     --input-blob-name-1 ERR194158_1.fastq.gz ERR194159_1.fastq.gz ERR194160_1.fastq.gz ^
     --input-blob-name-2 ERR194158_2.fastq.gz ERR194159_2.fastq.gz ERR194160_2.fastq.gz ^
     --output-storage-account-name myaccount ^
     --output-storage-account-key <access key to "myaccount"> ^
     --output-storage-account-container outputs

.. code-block:: sh
   :caption: Unix console

   msgen submit \
     --api-url-base https://malibutest0044.azure-api.net \
     --subscription-key <API subscription key> \
     --process-args R=grch37bwa \
     --input-storage-account-name myaccount \
     --input-storage-account-key <access key to "myaccount"> \
     --input-storage-account-container inputs \
     --input-blob-name-1 ERR194158_1.fastq.gz ERR194159_1.fastq.gz ERR194160_1.fastq.gz \
     --input-blob-name-2 ERR194158_2.fastq.gz ERR194159_2.fastq.gz ERR194160_2.fastq.gz \
     --output-storage-account-name myaccount \
     --output-storage-account-key <access key to "myaccount"> \
     --output-storage-account-container outputs

.. code-block:: yaml
   :caption: config.txt

   api_url_base:                     https://malibutest0044.azure-api.net
   subscription_key:                 <API subscription key>
   process_args:                     R=grch37bwa
   input_storage_account_name:       myaccount
   input_storage_account_key:        <access key to "myaccount">
   input_storage_account_container:  inputs
   input_blob_name_1:                ERR194158_1.fastq.gz ERR194159_1.fastq.gz ERR194160_1.fastq.gz
   input_blob_name_2:                ERR194158_2.fastq.gz ERR194159_2.fastq.gz ERR194160_2.fastq.gz
   output_storage_account_name:      myaccount
   output_storage_account_key:       <access key to "myaccount">
   output_storage_account_container: outputs

The above configuration file would be used with this invocation: ``msgen submit -f config.txt``.

.. raw:: html

    <script type="text/javascript">
    $('div.highlight pre').html(
    function(i,h){
        return h.replace(/(ERR194158_[12]\.fastq\.gz)/g,'<span class="orange">$1</span>')
                .replace(/(ERR194159_[12]\.fastq\.gz)/g,'<span class="green">$1</span>')
                .replace(/(ERR194160_[12]\.fastq\.gz)/g,'<span class="blue">$1</span>');
    });
    </script>

BAM files
=========

You can submit multiple BAM files by passing all their names to the ``-b1/--input-blob-name-1``
argument. Note that all files should come from the same sample, but their order is not important.
Below are example submissions from a command line in Windows, in Unix, and using a configuration file.

.. code-block:: bat
   :caption: Windows console
   :emphasize-lines: 8

   msgen submit ^
     --api-url-base https://malibutest0044.azure-api.net ^
     --subscription-key <API subscription key> ^
     --process-args R=grch37bwa ^
     --input-storage-account-name myaccount ^
     --input-storage-account-key <access key to "myaccount"> ^
     --input-storage-account-container inputs ^
     --input-blob-name-1 ERR194158.bam ERR194159.bam ERR194160.bam ^
     --output-storage-account-name myaccount ^
     --output-storage-account-key <access key to "myaccount"> ^
     --output-storage-account-container outputs

.. code-block:: sh
   :caption: Unix console
   :emphasize-lines: 8

   msgen submit \
     --api-url-base https://malibutest0044.azure-api.net \
     --subscription-key <API subscription key> \
     --process-args R=grch37bwa \
     --input-storage-account-name myaccount \
     --input-storage-account-key <access key to "myaccount"> \
     --input-storage-account-container inputs \
     --input-blob-name-1 ERR194158.bam ERR194159.bam ERR194160.bam \
     --output-storage-account-name myaccount \
     --output-storage-account-key <access key to "myaccount"> \
     --output-storage-account-container outputs

.. code-block:: yaml
   :caption: config.txt
   :emphasize-lines: 7

   api_url_base:                     https://malibutest0044.azure-api.net
   subscription_key:                 <API subscription key>
   process_args:                     R=grch37bwa
   input_storage_account_name:       myaccount
   input_storage_account_key:        <access key to "myaccount">
   input_storage_account_container:  inputs
   input_blob_name_1:                ERR194158.bam ERR194159.bam ERR194160.bam
   output_storage_account_name:      myaccount
   output_storage_account_key:       <access key to "myaccount">
   output_storage_account_container: outputs

The above configuration file would be used with this invocation: ``msgen submit -f config.txt``.

What genome references can I use?
---------------------------------
We currently support these references:

.. cssclass:: table-bordered

+-----------------------+---------------------------------+
|Reference              |Value of ``-pa/--process-args``  |
+=======================+=================================+
|GRCh37                 |``R=grch37bwa``                  |
+-----------------------+---------------------------------+
|GRCh38 (no ALT contigs)|``R=grch38_NoAltAnalysisSet_bwa``|
+-----------------------+---------------------------------+
|hg19                   |``R=hg19bwa``                    |
+-----------------------+---------------------------------+

Where do I learn more about available commands and options?
-----------------------------------------------------------
Use the ``msgen help`` command. If no further arguments are provided, it will show a list of available help sections, one for each of
``submit``, ``list``, ``cancel``, and ``status``.

To get help for a specific command, type ``msgen help command``; for example, ``msgen help submit`` will list all of the submit options.

.. _config-file:

How do I create a config file for msgen?
----------------------------------------
msgen understands configuration files in the following format:

1.    All options are provided as key-value pairs with values separated from keys by a colon.
2.    Whitespace is ignored.
3.    Lines starting with ``#`` are ignored.

Any command-line argument in the long format can be converted to a key by stripping its leading dashes and replacing dashes between words
with underscores. Here are some conversion examples:

.. cssclass:: table-bordered

+----------------------------------+---------------------------+
|Command line argument             |Configuration file line    |
+==================================+===========================+
|``-u/--api-url-base https://url`` |*api_url_base: https://url*|
+----------------------------------+---------------------------+
|``-k/--subscription-key KEY``     |*subscription_key: KEY*    |
+----------------------------------+---------------------------+
|``-pa/--process-args R=grch37bwa``|*process_args: R=grch37bwa*|
+----------------------------------+---------------------------+
