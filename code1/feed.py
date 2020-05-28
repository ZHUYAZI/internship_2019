# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 16:20:41 2019

Add walk to feed to route 

version 2.0

@author: Yazi ZHU
"""

import partridge as ptg
import networkx as nx
import osmnx as ox
import peartree as pt
from datetime import date



class Feed_To_Routes():
        
    def __init__(self, path, the_date):
        self.feed = self.get_representative_feed(path,the_date)
        self.G = pt.load_feed_as_graph(self.feed, 0, 24*60*60)
        self.G_add_walk=self.add_edge_walk()
    
    def get_representative_feed(self,file_loc: str, the_date: str):
        year, month, day = map(int, the_date.split("/"))
        selected_date = date(year, month, day)
        # Extract service ids and then trip counts by those dates
        service_ids_by_date = ptg.read_service_ids_by_date(file_loc)
        trip_counts_by_date = ptg.read_trip_counts_by_date(file_loc) 
        # Make sure we have some valid values returned in trips
        if not len(trip_counts_by_date.items()):
            # Otherwise, error out
            raise InvalidGTFS('No valid trip counts by date '
                              'were identified in GTFS.')
        sub = service_ids_by_date[selected_date]
        feed_query = {'trips.txt': {'service_id': sub}}
        feeds=ptg.load_feed(file_loc, view=feed_query)
        return feeds
    
    def add_edge_walk(self):
        Graph=self.G.copy()
        for u in Graph.nodes:
            for v in Graph.nodes:
                if u!=v and not Graph.has_edge(u,v):
                    Graph.add_edge(u,v)
    
                    lat1=self.G.node[u]['x']
                    lng1=self.G.node[u]['y']
                    lat2=self.G.node[v]['x']
                    lng2=self.G.node[v]['y']
                    #we suppose the walk speed is 1.2 m/s
                    Graph[u][v][0]['length']=ox.utils.great_circle_vec(lat1,lng1,lat2,lng2)/1.2
                    Graph[u][v][0]['mode']='walk'
        
        return Graph
      
    def get_shortest_path(self,a:list, b:list):
        from_node = ox.utils.get_nearest_node(self.G, a, return_dist=False)
        to_node = ox.utils.get_nearest_node(self.G, b, return_dist=False)
        return nx.dijkstra_path(self.G_add_walk, from_node, to_node,weight='length')
        