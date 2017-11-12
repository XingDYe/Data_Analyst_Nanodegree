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

street_re = re.compile(r'\b\S+\.?$',re.IGNORECASE)
types = defaultdict(set)

expected =['Road','Avenue','Lane',
			'Place','Street','Court',
			'Drive','Boulevard','Way',
			'Terrace','Commons','Broadway',
			'Park','Parkway','Highway','Spencer']

#UPDATE THIS VARIABLE
mapping = { "CT":"Center","Rd":"Road","Ct":"Court","Expy":"ExportPassway",
			"Ave":"Avenue","Cir":"Circle","Dr":"Drive",'Alio':'Alioto',
			"Blvd":"Boulevard",'Ln':'Lane',"Rd.":'Road',"St":"Street"}


def audit_street_type(types,name):
	m = street_re.search(name)
	if m:
		street_type = m.group()
		if types[street_type] not in expected:
			types[street_type].add(name)


def is_name(elem,value):
		return(elem.attrib['k'] == value)

def audit(tag1,kvalue):
	for event, elem in ET.iterparse(osm_file, events=("start",)):
		if elem.tag == tag1:
			for tag in elem.iter('tag'):
				if is_name(tag,kvalue):
					audit_street_type(types,tag.attrib['v'])
	return types
	

def update_name(name, mapping):
	name = name.split()
	string = ''
	for i in range(len(name)):
		key = name[i].capitalize()
		if key in mapping.keys():
			name[i] = mapping[key]
	string = ' '.join(i for i in name)
	return string

if __name__=='__main__':
	NTtypes = audit('way','tiger:name_type')
	pprint.pprint(sorted(NTtypes))

	
