""" MultiQC module to parse output from Lima """

import logging

from multiqc.modules.base_module import BaseMultiqcModule

# Initialise the logger
log = logging.getLogger(__name__)

# Import HUMID submodules
from . import stats, neighbours

class MultiqcModule(BaseMultiqcModule):
    def __init__(self):
        # Initialse the parent object
        super(MultiqcModule, self).__init__(
            name="HUMID",
            anchor="humid",
            href="https://github.com/jfjlaros/HUMID",
            info=" is a fast, reference free tool to remove (UMI) duplicates from sequencing data",
            # No publication / DOI // doi=
        )
        self.stats = None
        self.neighbours = None

        # Look for stats files
        stats.parse_reports(self)

        # Look for neighbour files
        neighbours.parse_reports(self)

        if all(not(x) for x in [self.stats, self.neighbours]):
            raise UserWarning


