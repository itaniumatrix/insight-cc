import networkx as nx
import json, sys
import datetime as dt
from tweets_cleaned import clean_text_escape, clean_text_unicode

def main(argv):
    """Main function, requires 3 inputs in commandline following call to average_degree.py:
    argv[1]: input filename
    argv[2]: output filename
    argv[3]: Time Window in seconds, to maintain graph nodes & edges
    """
    in_file = sys.argv[1]
    out_file = sys.argv[2]
    # Need to convert input string to integer
    time_secs = int(sys.argv[3])
    build_graph(in_file, out_file, time_secs)


def get_nodes(hashtag_list):
    """Return a list of hashtags in lowercase
    
    hashtag_list: list passed from the JSON line ['entities']['hashtags']. Need to extract the 
    'text' field from this list (dictionary in Python).
    """
    # Extract text and set to lower case, put in a list (using list comprehension)
    # Modify here: to change case-(in)sensitivity for hashtags.
    out = [tag['text'].lower() for tag in hashtag_list]
    return out

def compute_edges(node_list):
    """Generate a list of pairs (tuples), each defining an edge
     
    node_list: a list of nodes (hashtags)
    
    The resulting edge_list should be a triangular number (n*(n-1)/2), where n is the number of nodes
    """
    num_nodes = len(node_list)
    edge_list = []
        
    """
    Ie. 2 nodes -> 1 edge. 3, 4, 5, 6 nodes --> 3, 6, 10, 15 edges etc.
    
    Iterate through the 'other' nodes (ones we have not built edges with already)
    Basically visit each tuple, ij to build the triangular edge matrix (i = node1, j = node2)
    """ 
    for i in range(num_nodes):
        #print (str(i),': ',node_list[i])
        for j in range(i+1, num_nodes):
            
            #print(node_list[i],node_list[j])
            edge_list.append((node_list[i], node_list[j]))
    return edge_list

def make_datetime(time_str):
    """Convert string to a Python datetime object, needed for comparison and math on times.
    
    time_str: a Twitter time format string (stored in 'created_at')
    Ex. Fri Oct 30 15:29:44 +0000 2015    #Note:(Twitter always gives time as UTC +0000)
    """
    out = dt.datetime.strptime(time_str, '%a %b %d %H:%M:%S +0000 %Y')
    return out

def make_time_window(timestamp, num_secs):
    """Computes datetime - num_secs to serve as time boundary
    """
    time_minus_delta = timestamp - dt.timedelta(0, num_secs)
    return time_minus_delta

def find_avg_degree(graph):
    """Returns average degree of all nodes in graph
    """
    total = 0
    degree_dict = graph.degree()
    for degree in degree_dict.values():
        total += degree
    num_nodes = graph.number_of_nodes()
    if (num_nodes == 0):
        return 0
    else:
        return total/graph.number_of_nodes()

def trim_graph(graph, latest_time, num_secs):
    """Remove nodes and edges from graph older than latest_time - num_secs
    
    graph: input NetworkX Graph to be trimmed
    latest_time: datetime object of the most recent tweet
    num_secs: number of seconds of tweets to include in graph
    """
    time_boundary = make_time_window(latest_time, num_secs)
    
    #Iterate through Nodes first
    nodes_dict = nx.get_node_attributes(graph, 'datetime')
    for node in nodes_dict:
        node_time = nodes_dict[node]

        #Remove expired nodes (prunes some edges natively in NetworkX)
        if (node_time < time_boundary):
            graph.remove_node(node)
       
    #Now remove edges that are old, on nodes that remain current in time window
    edges_dict = nx.get_edge_attributes(graph, 'timestamp')
    for edge in edges_dict:
        edge_time = edges_dict[edge]

        if (edge_time < time_boundary):
            #print('*yoyo*', edge)
            #Edge is a tuple (u, v), so pass u, v to remove_edge()
            graph.remove_edge(edge[0], edge[1])

def trim_node_list(nodes):
    """Cleans up text strings and removes from nodes list if resulting string is empty. (After removing Unicode
        characters, some strings / hashtags become empty. Discard - we should not form an unnamed node, which could
        connect every other hashtag in the tweet.
        As per Feature 1, cleaning = removing Unicode > ASCII 127, and replacing whitespace / escape characters.
    
    nodes: list of strings, possibly with Unicode (straight ouf or JSON 'hashtags')
    """
    out_list = []
    for node in nodes:
        cleaned_string = clean_text_escape(node)
        cleaned_string = clean_text_unicode(cleaned_string)
        #Add to out_list only if cleaned_string is not empty
        if (len(cleaned_string) > 0):
            out_list.append(cleaned_string)
    return out_list


def build_graph(in_file, out_file, time_window):
    """Reads in entries in in_file, builds the graph, prunes the nodes and edges 
    to those within time_window of the last read entry, computes average edge degree,
    and save to out_file.

    in_file: input filename
    out_file: output filename
    time_window: Time Window in seconds, to maintain graph nodes & edges (longer means bigger graph and runtime)
    """

    import time
    t0 = time.time()

    # NetworkX object stores everything for the graph (as dictionary of dictionaries) nodes[edges]
    g = nx.Graph()
    print(out_file)
    with open(in_file) as tweetfile:
        f=open(out_file, 'w+')

        for line in tweetfile:
            data = json.loads(line)

            """Try block to anticipate misformed entries in tweets.txt. Sometimes the Twitter API does not pass
            properly formed JSON lines, and passes error codes instead. This will cause a KeyError when trying to access
            'entities' in the JSON object.
            """
            try:
                entities = data['entities']
                hashtags = entities['hashtags']
                #print('length', len(entities['hashtags']))
                ##Continue to process if JSON line contained at least 1 hashtag
                if (hashtags):
                    datetime_obj = make_datetime(data['created_at'])
                    
                    # Create nodes, edges if # of Hashtags > 1. (Nodes with 1 hashtag, 0 connectivity are ignored)
                    if (len(hashtags) > 1):
                        nodes = get_nodes(entities['hashtags'])
                        #print(nodes)
                        nodes = trim_node_list(nodes)
                        edges = compute_edges(nodes)
                        #print('Edges: ', edges)
                        g.add_nodes_from(nodes, datetime = datetime_obj)
                        g.add_edges_from(edges, timestamp = datetime_obj)

                    # Remove outdated nodes and edges from graph
                    trim_graph(g, datetime_obj, time_window)

                #Now compute the degree, after graph is trimmed(updated)
                avg_degree = find_avg_degree(g)
                
                #Trim to 2 digits, print to file

                print("%.2f" % avg_degree, file=f)
        
            except KeyError:
                """ Handle errors when the JSON line is Twitter error code. (Does not have the fields
                'created_at' or 'entities' or 'hashtags') --> throws KeyError
                """
                pass
            
            # Catch all other exceptions to allow script to continue running
            except:
                pass
        # Close output file.
        f.close()

    t1 = time.time()

    total = t1-t0
    print(total)

# Run this main program if the file is being called (not imported)
if __name__ == "__main__":
   main(sys.argv[1:])