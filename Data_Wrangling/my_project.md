# OpenStreetMap Data Case Study

### Map Area
San Francisco, California, United States

- [http://www.openstreetmap.org/relation/111968](http://www.openstreetmap.org/relation/111968)
- [https://mapzen.com/data/metro-extracts/metro/san-francisco_california/](https://mapzen.com/data/metro-extracts/metro/san-francisco_california/)
I choose the city because i'm interested in high-tech in Silicon Valley.

## Problems Encountered in data waragging
The sample file is about one-tenth size of the origanial downloaded file.It was used the average sampling rate of 1/10. I met some problems in auditing the data,.I will focus on the following questions 


- In my case ,there exits one record that doesn't have the 'uid'.and 'id' = '60742947' were only one record in the nodes's records  

- Over-abbreviated tiger name type*('Pky','Brg','Pl','Blvd')*

- the sequence of words'location has some issue.*('Alameda de Las Pulgas','Alameda De Las','Buena Vista Avenue West')*

- Inconsistent in 'addr:street' *(“Street”, “St.”, “St”)*,*('avenue','Avenue')* and in the state data *('CA','ca')* 

- The tag contains problematic characters *("Hwy;Brg")* 

- the postal code have those problematic postcode *('CA','1078','94121-3131','95498')*. The zip code in San Francisco is 5-digit starting at '94'. The 4-digital is the address code in local city.The postal code '1078' may be the street code.

- Street names in second ­level `“k”` tags came from Tiger GPS data and divided into different segments.Tiger GPS street name type data was abbreviated.

	```XML
	<tag k="name" v="Colon Ave" />
	<tag k="tiger:name_base" v="Colon" />
	<tag k="tiger:name_type" v="Ave"/>
	```

### Over­abbreviated Street /State Names

when clean the element data,using the audit_name function update the "addr:street" of tags in nodes and "tiger:name_type" of tags in the ways   


```python 

mapping = {"Rd":"Road", "Rd.":'Road', "Ct":"Court",'ca':'CA',
			'Tunl':'Tunnel', 'Plz':'Plaza', 'Aly':'Alley',
			"Ave":"Avenue", "Ave.":"Avenue", "Cir":"Circle", 
			"CT":"Center","Blvd":"Boulevard", "Dr":"Drive",
			'Ln':'Lane',"St":"Street",'St.':'Street'}
			
def update_name(name, mapping):
	name = name.split()
	string = ''
	for i in range(len(name)):
	# Ignorecase's influence 
		key = name[i].capitalize()
		if key in mapping.keys():
			name[i] = mapping[key]
	string = ' '.join(i for i in name)
	return string

```

This updated all substrings in problematic strings, such that:
*“ Maxwelton Rd ”,'ca'*
becomes:
*“Maxwelton Road”,'CA'*

## Postal code
We use the regular expressions to collect the right zip code and output the relative messages of uncorrected zip code.Then we want to find the geography location in the nodes by checking the identical user's ID. 
```python
# use the regular expression to find problematic string
post = re.compile(r'\d{5}([-]\d{4})?')

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
```
{'changeset': '42114270', 'uid': '371121', 'timestamp': '2016-09-13T01:05:05Z',
'lon': '-122.4104786', 'version': '3', 'user': 'AndrewSnow', 'lat': '37.7793844'
, 'id': '1987955775'}{'k': 'addr:postcode', 'v': '1087'}
{'k': 'addr:postcode', 'v': 'CA'}

```
After update
```
{'changeset': '42114270', 'uid': '371121', 'timestamp': '2016-09-13T01:05:05Z',
'lon': '-122.4104786', 'version': '3', 'user': 'AndrewSnow', 'lat': '37.7793844'
, 'id': '1987955775'}{'k': 'addr:postcode', 'v': '94103'}

```
The first thing  is checking whether exist the user's latitude and longitude information in the dataset. We can locate the position's zip code to recorrect the postal code.But in the results, we only found the there is only one node has the geographical location in the sample nodes. As for the 9-digital code ,we only use the first 5-digital zip code and cut the last 4-digital code. The zip code in San Francisco,CA begin with '94',so the zip code of '95498' is not the CA's zip code. When checking the user's records, the one has many different postal code. it could means he doesn't in CA when he update the dateset.So I keep all the 5-digital zip code reserved.  

In searching the zip code of CA, the method of locating longitude and latitude only suit for the node's data or the way has reference nodes.As for other missed data,The method has no way to improve the data quality.

## File sizes

```
 example.osm        142 MB
 project.db         291 MB
 nodes.csv         0.81 MB
 nodes_tags.csv    0.98 MB
 ways.csv          5.11 MB
 ways_nodes.csv    19.6 MB
 ways_tags.csv      6.1 MB

```
```
In order to improve readability of results,I changed the sqlite's explain on.
```
## Number of nodes 
```sqlite3
SELECT COUNT(*) FROM nodes; 
```
9700

## Number of ways
```sqlite3
SELECT COUNT(id) FROM ways;
```
82142

## Number of unique user in nodes
```sqlite3
SELECT COUNT(*)
FROM (	SELECT uid 
		FROM nodes 
		GROUP BY uid
		HAVING COUNT(id) = 1)
```
288

## Number of unique user in ways
```sqlite3
SELECT COUNT(unique_way.id) 
FROM (	SELECT *	
		FROM ways 
		GROUP BY uid 
		HAVING COUNT(id) = 1) as unique_way
``` 
342
## Total number user in nodes
```sqlite3
sqlite> select count(uid) from (
	...> select uid,count(id) from nodes
	...> group by uid
	...> order by count(id) desc);

count(uid)
----------
587
```
## Total user number in ways
```sqlite3
sqlite> select count(uid) from (
	...> select uid,count(id) from ways
	...> group by uid
	...> order by count(id) desc);
count(uid)
----------
837
```
The unique users rate is 49.1% in nodes and that in  ways is 40.8%.

##	The most updated user  

```sqlite3
sqlite>
	...> SELECT uid,user,COUNT(id) AS number
	...> FROM nodes
	...> GROUP BY uid
	...> ORDER BY COUNT(id) DESC
	...> LIMIT 10;

uid         user          number
----------  ------------  ------
933797      oba510        1528
169004      oldtopos      718
371121      AndrewSnow    707
1295        robert        562
153669      dchiles       548
11154       beej71        400
481533      dbaron        370
14293       KindredCoda   332
28775       StellanL      330
22925       ELadner       301
```

##	The most reference nodes of ways_id   
```sqlite3
sqlite>
	...> SELECT id ,COUNT(node_id) as number
	...> FROM ways_nodes
	...> GROUP BY id
	...> ORDER BY COUNT(node_id) DESC
	...> LIMIT 10;
```
id          number
----------  -------
123074187   620
33116521    574
123075165   542
230750461   505
33170699    499
24286738    462
30086509    450
109826495   397
389520989   384
158622336   348
```

##	The most types and the most key in each of most types in ways'tags
```sqlite3
sqlite> SELECT type,key,max(num)as number
	...> FROM(
	...> 	SELECT type,key ,COUNT(value)AS num
	...> 	FROM ways_tags
	...> 	GROUP BY type,key
	...> 	ORDER BY COUNT(key) DESC)
	...> GROUP BY TYPE
	...> ORDER BY NUM DESC
	...> LIMIT 10;

type              key               number
----------------  ----------------  ----------
regular           building          67107
tiger             county            5352
addr              city              4178
redwood_city_ca   bld_gid           1860
turn              lanes             550
massgis           cat               426
building          levels            266
paloalto_ca       id                228
hgv               national_network  193
lanes             backward          171

```

``` 

## The user  who update the data frequently and which data they most updated.
```sqlite3
SELECT uid,type,key,COUNT(ways_tags.value) AS number
FROM ways_tags LEFT JOIN ways ON ways.id=ways_tags.id
GROUP BY uid,type,key
ORDER BY COUNT(ways_tags.value) DESC
LIMIT 10;

uid         type        key         number
----------  ----------  ----------  --------
94578       regular     building    17782
2226712     regular     building    6108
2219338     regular     building    4179
1330847     regular     highway     3718
1330847     tiger       county      3707
1330847     regular     name        3700
1330847     tiger       name_base   3637
1330847     tiger       cfcc        3602
1330847     tiger       name_type   3553
1240849     regular     building    3235

```
## The most Amenities  
```sqlite3
sqlite> select value,count(key) as number  
	...> from nodes_tags
	...> group by value   
	...> having key = 'amenity'
	...> order by count(id) desc
	...> limit 10;

value            number
---------------  -------
restaurant       126
bench            98
cafe             58
bank             49
drinking_water   41
school           36
fuel             34
post_box         25
toilets          25
fast_food        23
```
From the different view in the dataset ,we can found the most updated datatype is building and the number much bigger than other types of data.In nodes,there almost half of users is unique.the rate highter than that in ways.The restaurant and bench occupy the top two of the amenity. It represent the demand for delicious food and a short rest. The neighborhood may be a commercial area or other fast paced area because the cafe help people refresh themselves and the number of bank can partly reflect the intensity of the deal.The Tiger data could provide the precious location information to help others audit the dataset but it's not free. 


# Additional Ideas

## The most postal code 
```sqlite3
sqlite> select value,count(key)as number
   ...> from ways_tags
   ...> group by value
   ...> having key=='postcode'
   ...> order by count(key) desc
   ...> limit 10;
value     number
--------  ----------
94611     306
94122     250
94116     207
94610     124
94133     105
94118     104
94117     62
94127     52
94103     33
94109     28
```
The zip code of '94611' belongs Oakland,CA and the zip code of '94122' and '94116' in San Francisco city.The common point is they all have many Universities or Colleges.

## Most marked value in one of most keys   
```sqlite3
sqlite> select key, value ,count(ways.id) as number
	...> from ways join ways_tags on
	...> ways.id = ways_tags.id
	...> group by key,value
	...> order by count(ways.id) desc
	...> limit 10;
key         value                           number
----------  ------------------------------  ------
building    yes                             64906
cfcc        A41                             4511
height      6                               4073
highway     service                         3572
highway     residential                     3315
reviewed    no                              2859
oneway      yes                             2391
source      City of Redwood City, CA 1013   2047
city        Redwood City                    2046
county      Alameda, CA                     2030
```
## The most popular city
```sqlite3
sqlite>  select value,count(key)as number
   ...>  from ways_tags
   ...> group by value
   ...> having key ='city'
   ...> order by count(key) desc
   ...> limit 10;
value               number
------------------  ----------
Redwood City        2046
San Francisco       1009
Piedmont            389
Berkeley            219
Palo Alto           153
Richmond            120
Oakland             97
Albany              22
Walnut Creek        22
Union City          21
```
## The most popular address city  
```sqlite3
sqlite> select value,count(key)as number
   ...> from ways_tags
   ...> group by type,value
   ...> having key ='city' and type ='addr'
   ...> order by count(key) desc
   ...> limit 10;
value               number
------------------  ----------
Redwood City        2046
San Francisco       1000
Piedmont            384
Berkeley            217
Palo Alto           153
Richmond            111
Oakland             94
Alameda             53
Albany              22
Walnut Creek        22
```
```sqlite3
sqlite> select key,count(id)
	...> from ways_tags
	...> group by value,key
	...> having value like '%Redwood City%'
	...> order by count(id) desc
	...> limit 10;
key               count(id)
----------------  ----------
source            2047
city              2046
source            74
name              1
name              1
```
```sqlite3
sqlite> select key,count(id)
	...> from ways_tags
	...> group by value,key
	...> having value = 'San Francisco'
	...> order by count(id) desc
	...> limit 10;
key               count(id)
----------------  ----------
city              1000
county_name       7
backward          1
destination       1
```
From the aboving graphs,we can found the city of Redwood and San Francisco occupy the most amount of the city.In the Redwood City,it is famous as its human source 'City of Redwood City, CA 1013'.
As selecting the most city,I found it's necessary to add the constriction of type.Thought it doesn't have much influence in the first 7 city,but the last three city changed.so I think it's cartainly need to add limitation in accuracy.

# Conclusion
 In the data wraggling ,we could found there are many wrong data type.The over-abbreviated of tiger name_type string could create a lots of ambubiguity.I still don't understand the meaning of the part of strings appeared in the auditing.In my dataset,I met a tricky problem which a data record has id without uid and the trouble is the data record has no latitude and longitude information.It means hard to identify the user's id. As for improving the data quality,I found it's essential to provide the location information,it can help correct some missed data and cross-validating the postal code. The anticipuate issues is time-wasting and mannual correction. We have to do it by ourselves if we don't have the accurate latitude ,longitude and the corresponding postal code database. It also could define respective latitude and longitude area for different postal code numbers.But it's may be difficult whether we can found such clear boundry line.     

 
