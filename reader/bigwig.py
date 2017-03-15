"""
.. Copyright 2017 EMBL-European Bioinformatics Institute

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

import os, json, pyBigWig

from dmp import dmp


class bigbed:
    """
    Class related to handling the functions for interacting directly with the
    BigBed files. All required information should be passed to this class.
    """
    
    test_file = '../sample.bw'
    
    
    def __init__(self, user_id = 'test', file_id = '', resolution = None):
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
        resolution : int (Optional)
            Level of resolution. This is optional, but only the functions
            get_resolutions() and set_resolutions() can be called. Once the
            resolution has been set then all functions are callable.
        """
        
        self.test_file = '../sample.bw'
        
        # Open the bigbed file
        if user_id == 'test':
            resource_path = os.path.join(os.path.dirname(__file__), self.test_file)
            self.f = pyBigWig.open(resource_path, "r")
        else:
            cnf_loc=os.path.dirname(os.path.abspath(__file__)) + '/mongodb.cnf'
            da = dmp(cnf_loc)
            file_obj = da.get_file_by_id(user_id, file_id)
            self.f = pyBigWig.open(file_obj['file_path'], 'r')

    
    def get_chromosomes(self):
        """
        List the chromosome names and lengths

        Returns
        -------
        chromosomes : dict
            Key value pair of chromosome name and the value is the length of the
            chromosome.

        """

        return f.chroms()

    
    def get_header(self):
        """
        Get the bigBed header

        Returns
        -------
        header : dict
        """
        return f.header()

    
    def get_range(self, chr_id, start, end, format="wig"):
        """
        Get entries in a given range

        Parameters
        ----------
        chr_id : str
        start : int
        end : int
        format : string (OPTIONAL)
            `wig` format returning the whole file as a string is the default
            option. `list` will return the wig rows but as a list of lists.

        Returns
        -------
        wig : str (DEFAULT)
            List of strings for the rows in a wig file
        wig_array : list
            List of lists of each row for the wig file format

        """
        bw_features = self.f.intervals(chr_id, start, end)

        if format == "wig":
            wig_array = []
            for feature in bw_features:
                wig_array.append("\t".join(feature))

            return "\n".join(wig_array)

        return bw_features
