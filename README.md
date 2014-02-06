TrafficMap
==========

Show traffic on map

Version: 1.0
Purpose: load history traffic data into a map view for inspection

Environment: 
  Python 2.7 
  PIL 1.1.7 for Python 2.7

Description:
  Program is easy to use, you can do the following:
	  drag the map to another place
	  set new coordinates and press update to move map
	  set zoom level and press update to zoom the map
	  you can press load button to load history traffic data
	  you can press show/hide button to show/hide traffic display

Attention:
	This program doesn't handle cache well yet, so, it may generate more network traffic than it needs
	This program doesn't handle cities well yet.
	To get it work with city other than beijing, you need to:
		1. Replace point.dat and poffset.dat file in Res directory manually
		2. Then, restart the program
	This program has not smoothen the line along the road yet.
	We found there are more than 2 traffic lines (positive/negative direction), it may due to side road along high-way.

