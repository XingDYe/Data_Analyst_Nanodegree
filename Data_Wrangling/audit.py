#! /usr/bin/env python
#-*- coding: utf-8 -*-

import xml.etree.cElementTree  as ET
from collections import defaultdict
import pprint 
import re

# data problem first, the data overabbreviated like
# " Broadway Street; Mason Street "
# have the wrong data type in addr:street

osm_file = 'example.osm'

expected_re = re.compile(r'\d{5}$')
types = defaultdict(set)

def audit(tag1,kvalue):
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == tag1:
			for tag in elem.iter('tag'):
				if tag.attrib['k'] == kvalue:
					name = tag.attrib['v']
					m = expected_re.search(name)
					if (not m):
						types[tag1].add(name)				
	return types

if __name__=='__main__':
	audit('node','addr:postcode')
	audit('way','addr:postcode')
	print(types)
	
