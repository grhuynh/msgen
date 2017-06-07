# ----------------------------------------------------------
#  Copyright (c) Microsoft Corporation. All rights reserved.
#  Licensed under the MIT License. See LICENSE.rst in the
#  project root for license information. If LICENSE.rst
#  is missing, see https://opensource.org/licenses/MIT
# ----------------------------------------------------------

"""Custom argument parsing actions"""
import argparse
import itertools
import os
import re
import sys
from malibucommon import ODataArguments, ORDER_ASC, ORDER_DESC

class MaxLengthValidator(argparse.Action):
    """String length validator"""
    def __init__(self, option_strings, max_length, *args, **kwargs):
        super(MaxLengthValidator, self).__init__(option_strings, *args, **kwargs)
        self.max_length = max_length

    def __call__(self, parser, namespace, values, option_string=None):
        if values is not None and len(values) > self.max_length:
            print "Maximum length for the '{0}' field is {1}. Your value will be truncated.".format(self.dest, self.max_length)
            values = values[:self.max_length]
        setattr(namespace, self.dest, values)

class PositiveIntValidator(argparse.Action):
    """Positive integer validator"""
    def __call__(self, parser, namespace, values, option_string=None):
        try:
            positive = int(values)
        except ValueError as e:
            raise argparse.ArgumentError(self, e.message)
        if positive <= 0:
            raise argparse.ArgumentError(self, "expected a positive value")
        setattr(namespace, self.dest, positive)

class RangeValidator(argparse.Action):
    """Range validator for listing workflows"""
    def __call__(self, parser, namespace, values, option_string=None):
        value = values.strip()

        if not value or value == ":":
            raise argparse.ArgumentError(self, "an index or a range is expected")

        if ":" not in value:
            single = int(value)
            if single < 0:
                setattr(namespace, self.dest, ODataArguments(orderby=ORDER_DESC, skip=abs(single)-1, top=1))
            else:
                setattr(namespace, self.dest, ODataArguments(orderby=ORDER_ASC, skip=single, top=1))
            return

        start, stop = [s.strip() for s in value.split(":", 1)]

        try:
            start = int(start) if start else None
            stop = int(stop) if stop else None
        except ValueError as e:
            raise argparse.ArgumentError(self, e.message)

        # start and stop cannot both be None here, this would raise a parser error above
        if start is None and stop < 0:
            setattr(namespace, self.dest, ODataArguments(orderby=ORDER_DESC, skip=abs(stop), top=None))
            return
        elif start is None and stop >= 0:
            setattr(namespace, self.dest, ODataArguments(orderby=ORDER_ASC, skip=None, top=stop))
            return
        elif start < 0 and stop is None:
            setattr(namespace, self.dest, ODataArguments(orderby=ORDER_DESC, skip=None, top=abs(start)))
            return
        elif start >= 0 and stop is None:
            setattr(namespace, self.dest, ODataArguments(orderby=ORDER_ASC, skip=start, top=None))
            return
        elif start >= 0 and stop >= 0:
            # OK to have negative $top, our controller returns [] in that case, like in Python
            setattr(namespace, self.dest, ODataArguments(orderby=ORDER_ASC, skip=start, top=max(0, stop-start)))
            return
        elif start < 0 and stop < 0:
            # OK to have negative $top, our controller returns [] in that case, like in Python
            setattr(namespace, self.dest, ODataArguments(orderby=ORDER_DESC, skip=abs(stop), top=max(0, abs(start)-abs(stop))))
            return
        else:
            raise argparse.ArgumentError(self, "when a range is specified, its ends should be both non-negative or both negative")

class ConfigFileReader(argparse.Action):
    """Configuration file reader"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)
        if not values or not os.path.isfile(values):
            print >> sys.stderr, "Path '{0}' is not a file or doesn't exist, not reading settings from it".format(values)
        else:
            expected_settings, expected_list_settings = self.__get_expected_config_setting_names(parser)
            with open(values) as f:
                options_list = self.__read_options_from_file(f, expected_settings, expected_list_settings)
                for option in options_list:
                    action = parser._option_string_actions.get(option, None)
                    # Ignore arguments from other subparsers
                    if not action:
                        pass
                    # Prevent specifying a config file from the config we are reading
                    if action == self:
                        pass
                    # Check if we have seen this setting yet in the command line, and act on it, if not
                    if getattr(namespace, action.dest) is None:
                        raw_value = options_list[option]
                        # Convert the raw value to the target type; need to handle lists explicitly
                        if isinstance(raw_value, list):
                            converted_value = [parser._get_value(action, v) for v in raw_value]
                        else:
                            converted_value = parser._get_values(action, [raw_value])
                        action(parser, namespace, converted_value, option)
                        # The following is a hack: since ArgumentParser checks for whether values were provided
                        # by keeping a registry (inaccessible to us) istead of checking the namespace,
                        # mark the action as not required
                        action.required = False

    def __get_expected_config_setting_names(self, parser):
        """Returns a list of settings that we can expect to find in a config file"""
        all_options = self.__collect_settings_by_filter(parser)
        list_options = self.__collect_settings_by_filter(parser, lambda a: a.nargs is not None)
        return all_options, list_options

    def __collect_settings_by_filter(self, parser, condition=lambda a: True):
        options = set()
        options.update(itertools.chain.from_iterable(a.option_strings for a in parser._actions if condition(a)))
        return set(option[2:] for option in filter(lambda o: o.startswith("--"), options))

    def __read_options_from_file(self, file_object, expected_settings, expected_list_settings):
        """Reads expected settings from the provided config file
        file_object: File object for the config file
        expected_settings: settings we expect to find in the config"""
        if not file_object:
            raise Exception("file cannot be None")
        options = {}
        for line in file_object:
            line = line.strip() if line else ""
            if not line or line.startswith("#"):
                continue
            columns = line.split(':', 1)
            if len(columns) == 2:
                key = columns[0].strip().replace("_", "-")
                if key in expected_list_settings:
                    # We can do this because whitespace is not allowed
                    options["--" + key] = columns[1].strip().split()
                elif key in expected_settings:
                    value = columns[1].strip()
                    if value:
                        options["--" + key] = value
        return options

def nstr(value):
    """String converter that checks for contents"""
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("a non-empty, non-whitespace string is expected")
    return value

def to_bool(value):
    """String converter that checks for contents"""
    value = value.strip().lower()
    error = "a 'true' or 'false' is expected"
    if not value:
        # Keep default values when parsing empty strings from config
        return None
    elif value == "true":
        return True
    elif value == "false":
        return False
    raise argparse.ArgumentTypeError(error)

BAD_INPUT_BLOB_CHARS = re.compile("[^A-Za-z0-9._/-]")
BAD_OUTPUT_BASENAME_CHARS = re.compile("[^A-Za-z0-9._-]")

def _blob_name_validator(value, regex, isinput):
    """Blob name validator based on regular expression"""
    # Name length 1-1024 (https://docs.microsoft.com/en-us/azure/guidance/guidance-naming-conventions#naming-rules-and-restrictions)
    # Characters: alphanumeric, dot, dash, and underscore
    value = value.strip()
    if not value:
        raise argparse.ArgumentTypeError("empty or whitespace-only names are not allowed; found [{}]".format(value))
    if len(value) > 1024:
        raise argparse.ArgumentTypeError("maximum length is 1024 characters; found a value of length {0}".format(len(value)))
    if bool(regex.search(value)):
        error = "each name should contain only alphanumeric characters, dot, dash, underscore"
        if isinput:
            error = error + ", slash"
        raise argparse.ArgumentTypeError(error + "; found [{0}]".format(value))
    # We will not allow a leading slash in a blob name
    if value.startswith("/"):
        raise argparse.ArgumentTypeError("input blob names cannot start with a slash; found [{0}]".format(value))
    return value

def input_validator(value):
    """Input blob name validator"""
    return _blob_name_validator(value, BAD_INPUT_BLOB_CHARS, isinput=True)

def output_validator(value):
    """Output blob name validator"""
    if not value or not value.strip():
        return None
    return _blob_name_validator(value.strip(), BAD_OUTPUT_BASENAME_CHARS, isinput=False)

BAM_SAM_FILE = re.compile(r"^.+\.(b|s)am$", re.IGNORECASE)
FASTQ_FILE = re.compile(r"^.+\.f(ast)?q(\.gz)?$", re.IGNORECASE)

def differ_in_at_most_one(first, second):
    """Check if two strings differ in at most one position."""
    # Check if length differences make it possible
    if abs(len(first) - len(second)) > 1:
        return False

    if len(first) > len(second):
        longer, shorter = first, second
    else:
        longer, shorter = second, first

    one_found = False
    l, s = 0, 0
    long_length = len(longer)
    short_length = len(shorter)
    while l < long_length and s < short_length:
        if longer[l] != shorter[s]:
            if one_found: # found second difference
                return False
            else:
                one_found = True
                # skip one, if we have different lengths
                # position in shorter string should stay in place in that case
                if long_length != short_length:
                    l += 1
                else:
                    l += 1
                    s += 1
        else:
            l += 1
            s += 1
    return True

_name_mismatch_error = """File names [{0}] and [{1}] differ in more than one character.
This may mean that reads in them are not paired which will cause an error during alignment.
If you are sure that these two files contain paired reads, you can suppress this message by provding an argument -sf/--suppress-fastq-validation with a value 'true'"""

def validate_namespace(parser, namespace):
    """Do additional checks on the whole set of parsed arguments. Only those checks that cannot be performed
    in single argument validators (e.g. dependency between arguments apart from mutual exclusion) should be
    done here."""
    if namespace.command != "submit":
        return namespace

    # 0. Make sure we have something as input.
    if not namespace.input_blob_name_1:
        namespace.input_blob_name_1 = []
    if not namespace.input_blob_name_2:
        namespace.input_blob_name_2 = []
    all_blob_names = namespace.input_blob_name_1 + namespace.input_blob_name_2
    if len(all_blob_names) == 0:
        raise parser.error("no inputs provided")

    # 1. Make sure we don't mix BAM/SAM and FASTQ files in a single submission.
    bam_sam = any(BAM_SAM_FILE.match(b) != None for b in all_blob_names)
    fastq = any(FASTQ_FILE.match(b) != None for b in all_blob_names)
    if bam_sam and fastq:
        raise parser.error("cannot mix both FASTQ and BAM/SAM files in inputs")
    elif not (bam_sam or fastq):
        raise parser.error("neither FASTQ nor BAM/SAM files were provided as inputs")
    elif fastq:
        # 2. Make sure that if we use FASTQ files, we have them in pairs
        if len(namespace.input_blob_name_1) != len(namespace.input_blob_name_2):
            raise parser.error("each FASTQ file provided in -b1/--input-blob-name-1 should be paired with a FASTQ file in -b2/--input-blob-name-2 at the same position")
        # 3. If names in each pair don't match, show a warning
        for first, second in zip(namespace.input_blob_name_1, namespace.input_blob_name_2):
            if first == second:
                raise parser.error("the same file is used at the same position in both -b1/--input-blob-name-1 and -b2/--input-blob-name-2: [{0}]".format(first))
            if not differ_in_at_most_one(first, second) and not namespace.suppress_fastq_validation:
                print >> sys.stderr, _name_mismatch_error.format(first, second)

    return namespace