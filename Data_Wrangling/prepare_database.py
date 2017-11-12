#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs

import cerberus
import schema

import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re

OSM_PATH = "example.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"



LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+',re.IGNORECASE)
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
EXPECTED_RE = re.compile(r'[9][4]\d{3}([-]\d{4})?')
TYPES = defaultdict(set)
SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', "uid", 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', "uid", 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

# updating street mapping 
mapping = { "Rd":"Road", "Rd.":'Road', "Ct":"Court", 'Tunl':'Tunnel', 'Plz':'Plaza',
			"Ave":"Avenue", "Ave.":"Avenue", "Cir":"Circle", "Dr":"Drive", 'Aly':'Alley',
			"CT":"Center","Blvd":"Boulevard", 'Ln':'Lane', "St":"Street",'St.':'Street',
			"Expy":"ExportPassway","1078":'94103'}


# 94115-4620  94121-3131,94122-1515


def update_name(name, mapping):
	name = name.split()
	string = ''
	for i in range(len(name)):
		key = name[i].capitalize()
		if key in mapping.keys():
			name[i] = mapping[key]
	string = ' '.join(i for i in name)
	return string

def update_postcode(name):
	if len(name)==10:
		return name[:5]
	if len(name) ==5:
		return name
	elif name =='1078':
		name = '94103'
		return name
	else:
		return ''


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
	problem_chars=PROBLEMCHARS, default_tag_type='regular'):
	"""Clean and shape node or way XML element to Python dict"""
	node_attribs = dict()
	way_attribs = dict()
	way_nodes = []
	tags = []


	# My CODE HERE
	if element.attrib['id']=='60742947':
		element.attrib['uid'] = 0

	keys = element.attrib.keys()
	ID = int(element.attrib['id'])
	UID = int(element.attrib['uid'])
	x = {}
	if element.tag == 'node':
		for key in node_attr_fields:
			if key in keys:
				node_attribs[key] = element.attrib[key]
			else:
				node_attribs[key] = ''
		node_attribs['id'] = ID
		node_attribs["uid"] = UID
		node_attribs['lat'] = float(node_attribs['lat'])
		node_attribs['lon'] = float(node_attribs['lon'])
		node_attribs['changeset']  = int(node_attribs['changeset'])

		if (element.find('tag')!=None):
			for tag in element.iter('tag'):
				if (problem_chars.search(tag.attrib['k'])==None):
					k = tag.attrib['k']
					v = tag.attrib['v']
					x['id'] = ID
					x['key'] = k 
					x['type'] = default_tag_type
					x['value'] = update_name(v,mapping)
					if LOWER_COLON.search(k):
						word = k
						pos = word.find(':')
						x['type'] = word[0:pos]
						pos = pos + 1
						x['key'] = word[pos:]
					if k =='addr:postcode':
						x['value'] = update_postcode(v)	
					tags.append(x)        
			return {'node': node_attribs, 'node_tags': tags}

	elif element.tag == 'way':
		for key in way_attr_fields:
			if key in keys:
				way_attribs[key] = element.attrib[key]
		way_attribs['id'] = ID
		way_attribs["uid"] = UID
		
		for tag in element.iter('tag'):
			x = {}
			if problem_chars.search(tag.attrib['k'])== None:
				k = tag.attrib['k']
				v = tag.attrib['v']
				x['id'] = ID
				x['key'] = k
				x['type'] = default_tag_type
				x['value'] = update_name(v,mapping)
				if LOWER_COLON.search(k):
					word = k
					pos = word.find(':')
					x['type'] = word[0:pos]
					x['key'] = word[pos+1:]
				if k == 'addr:postcode':
					x['value'] = update_postcode(v)
				tags.append(x)  
		
		count = 0
		for nodes in element.iter('nd'):
			d1 = dict(zip(WAY_NODES_FIELDS,[ID,int(nodes.attrib['ref']),count]))
			count += 1
			way_nodes.append(d1)
		return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
		"""Yield element if it is the right type of tag"""

		context = ET.iterparse(osm_file, events=('start', 'end'))
		_, root = next(context)
		for event, elem in context:
				if event == 'end' and elem.tag in tags:
						yield elem
						root.clear()


def validate_element(element, validator, schema=SCHEMA):
		"""Raise ValidationError if element does not match schema"""
		if validator.validate(element, schema) is not True:
				field, errors = next(validator.errors.iteritems())
				message_string = "\nElement of type '{0}' has the following errors:\n{1}"
				error_string = pprint.pformat(errors)
				
				raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
		"""Extend csv.DictWriter to handle Unicode input"""

		def writerow(self, row):
				super(UnicodeDictWriter, self).writerow({
						k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
				})

		def writerows(self, rows):
				for row in rows:
						self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #

def process_map(file_in, validate):
	"""Iteratively process each XML element and write to csv(s)"""

	with codecs.open(NODES_PATH, 'w') as nodes_file, \
		 codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
		 codecs.open(WAYS_PATH, 'w') as ways_file, \
		 codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
		 codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

		nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
		node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
		ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
		way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
		way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

		nodes_writer.writeheader()
		node_tags_writer.writeheader()
		ways_writer.writeheader()
		way_nodes_writer.writeheader()
		way_tags_writer.writeheader()

		validator = cerberus.Validator()

		for element in get_element(file_in, tags=('node', 'way')):
			el = shape_element(element)
			if el:
				if validate is True:
					validate_element(el, validator)

				if element.tag == 'node':
					nodes_writer.writerow(el['node'])
					node_tags_writer.writerows(el['node_tags'])
				elif element.tag == 'way':
					ways_writer.writerow(el['way'])
					way_nodes_writer.writerows(el['way_nodes'])
					way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
	# Note: Validation is ~ 10X slower. For the project consider using a small
	# sample of the map when validating.    
	process_map(OSM_PATH, validate=True)

