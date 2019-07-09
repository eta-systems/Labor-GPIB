# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 15:02:53 2019

@author: simon

Copyright (c) 2019 eta systems GmbH. All rights reserved.

This Software is distributed WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY 
or FITNESS FOR A PARTICULAR PURPOSE. 
"""

import json
import numpy as np

"""
https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
"""
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

class Exporter:
    def __init__(self):
        self.asdf = 1
        
    # Writes a dict in json format to a file
    def dump_to_json_file(self, filename, data):
    	with open(filename, 'w', encoding='utf-8') as fh:
    		json.dump(data, fh, indent=4, sort_keys=True, cls=NumpyEncoder)

    
    
    
    