"""
.. See the NOTICE file distributed with this work for additional information
   regarding copyright ownership.

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

from __future__ import print_function

import os
import pyBigWig

from dmp import dmp
from dm_generator.GenerateSampleBigBed import GenerateSampleBigBed


class bigbed_reader(object):  # pylint: disable=invalid-name
    """
    Class related to handling the functions for interacting directly with the
    BigBed files. All required information should be passed to this class.
    """

    def __init__(self, user_id, file_id, cnf_loc=''):
        """
        Initialise the module and

        Parameters
        ----------
        user_id : str
            Identifier to uniquely locate the users files. Can be set to
            "common" if the files can be shared between users or 'test' for a
            dummy file
        file_id : str
            Location of the file in the file system
        """

        # Open the bigbed file
        if user_id == 'test':
            resource_path = os.path.join(
                os.path.dirname(__file__),
                "../tests/data/sample.bb"
            )
            if os.path.isfile(resource_path) is False:
                gsa = GenerateSampleBigBed()
                gsa.main()
            self.file_handle = pyBigWig.open(resource_path, 'r')
        else:
            dm_handle = dmp(cnf_loc)
            file_obj = dm_handle.get_file_by_id(user_id, file_id)
            self.file_handle = pyBigWig.open(file_obj["file_path"], 'r')

    def close(self):
        """
        Tidy function to close file handles

        Example
        -------
        .. code-block:: python
           :linenos:

           from reader.bigbed import bigbed_reader
           bbr = bigbed_reader('test')
           bbr.close()
        """
        self.file_handle.close()

    def get_chromosomes(self):
        """
        List the chromosome names and lengths

        Returns
        -------
        chromosomes : dict
            Key value pair of chromosome name and the value is the length of the
            chromosome.

        """

        return self.file_handle.chroms()

    def get_header(self):
        """
        Get the bigBed header

        Returns
        -------
        header : dict
        """
        return self.file_handle.header()

    def get_range(self, chr_id, start, end, file_type="bed"):
        """
        Get entries in a given range

        Parameters
        ----------
        chr_id : str
            Chromosome name
        start : int
            Start of the region to query
        end : int
            End of the region to query
        file_type : string (OPTIONAL)
            `bed` format returning the whole file as a string is the default
            option. `list` will return the bed rows but as a list of lists.

        Returns
        -------
        bed : str (DEFAULT)
            List of strings for the rows in a bed file
        bed_array : list
            List of lists of each row for the bed file format

        """

        print("GET RANGE:", str(chr_id), int(start), int(end), file_type)
        try:
            bb_features = self.file_handle.entries(str(chr_id), int(start), int(end))
        except RuntimeError:
            bb_features = []

        if bb_features is None:
            bb_features = []

        if file_type == "bed":
            bed_array = []
            for feature in bb_features:
                row = str(chr_id) + "\t" + str(feature[0]) + "\t"
                row += str(feature[1]) + "\t" + feature[2]
                bed_array.append(row)

            return "\n".join(bed_array) + "\n"

        bed_array = []
        for feature in bb_features:
            row = [chr_id, feature[0], feature[1]] + feature[2].split("\t")
            bed_array.append(row)

        return bed_array
