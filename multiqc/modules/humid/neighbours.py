import logging
from collections import OrderedDict
from multiqc import config
from multiqc.plots import linegraph 

log = logging.getLogger(__name__)

def parse_reports(self):
    # To store the summary data
    self.neighbours = dict()

    # Parse the output files
    parse_log_files(self)

    # Remove filtered samples
    self.neighbours = self.ignore_samples(self.neighbours)

    log.info(f"Found {len(self.neighbours)} reports")
    self.write_data_file(self.neighbours, "multiqc_humid_neighbours")

    add_to_humid_section(self)


def parse_log_files(self):
    for f in self.find_log_files("humid/neighbours"):
        # There is no sample name in the log, so we use the root of the
        # file as sample name (since the filename is always stats.dat
        s_name = self.clean_s_name(f["root"], f)

        # process the file content
        d = {}
        for line in f["contents_lines"]:
            nr_neighbours, count = line.strip('\n').split(' ')
            d[int(nr_neighbours)] = int(count)

        # Got this far, data must be good
        if s_name in self.neighbours:
            log.debug("Duplicate sample name found! Overwriting: {}".format(s_name))
        self.neighbours[s_name] = d
        self.add_data_source(f, s_name)

def add_to_humid_section(self):
    # Figure configuration
    plot_config = {
        "id": "humid-neighbours",
        "title": "HUMID: Neighbour statistics",
        "ylab": "Number of sequences",
        "xlab": "Number of neighbours",
        "logswitch": True,
        "logswitch_active": True,
        "hide_zero_cats": False,
    }
    self.add_section(
        name="Neighbour statistics",
        anchor="humid-neighbour-section",
        description="""
            Neighbour statistics per sample. For every unique read in the input data,
            the number of neighbours in the graph has been determined.
            """,
        plot=linegraph.plot(self.neighbours, plot_config),
    )