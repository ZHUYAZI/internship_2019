import partridge as ptg
import networkx as nx
import pandas as pd
import osmnx as ox
import peartree as pt
from datetime import date
from typing import Tuple


class Feed_To_Routes():
        
    def __init__(self, path, the_date):
        self.feed = self.get_representative_feed(path,the_date)
        self.G = pt.load_feed_as_graph(self.feed, 0, 24*60*60)
    
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
      
    def get_shortest_path(self,a:list, b:list):
        from_node = ox.utils.get_nearest_node(self.G, a, return_dist=False)
        to_node = ox.utils.get_nearest_node(self.G, b, return_dist=False)
        return nx.dijkstra_path(self.G, from_node, to_node,weight='length')
        
