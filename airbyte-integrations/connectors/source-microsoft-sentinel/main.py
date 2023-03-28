#
# Copyright (c) 2023 Airbyte, Inc., all rights reserved.
#


import sys

from airbyte_cdk.entrypoint import launch
from source_microsoft_sentinel import SourceMicrosoftSentinel

if __name__ == "__main__":
    source = SourceMicrosoftSentinel()
    launch(source, sys.argv[1:])
