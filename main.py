__author__ = 'cwdillon'

# The inspiration for this program comes from a paper by J. Xie, S. Sreenivasan, G. Korniss, W. Zhang, C. Lim and
# K. Szymanski on "Social Consensus Through the Influence of Committed Minorities", published in Physical Review E 84(1)
# 011130, July 2011 (8 pages). The primary purpose of this program is to compare performance times of the model running
# in native python, using the popular iGraph modeling and analysis library, which holds a network graph in memory, to a
# model that reads and writes to the neo4j graph database.
#
# The hypothosis is that the iGraph model may be faster for a small number of nodes/edges (e.g., <10,000 nodes with <10%
# probability for a connection to another node) but that the neo4j version will be faster >10,000 nodes and >10% edge
# probability; that the graph database model will compute very large graphs---1 Million nodes, for example---and that the
# iGraph model cannot compute.

import csv
import timing
import datetime 
from time import clock
from time import sleep
from time import time
import random
from igraph import *
from py2neo import neo4j, node, rel, cypher


N = 1000            # Number of n graph nodes 1M
EP = .03            # Probability of relationship in Erdos-Renyi random graph
P = int(N * .05)    # Proportion of nodes that start off with opinion 'B'


def main():
    # pass
    RUN = getTimeStampString()
    
def getTimeStampString():
    """
    Thanks to Vince Kane for this helpful function, amended here to include microseconds, when necessary
    :rtype : str
    :return: string with current timestamp with hours, minutes, seconds
    """
    dt = datetime.datetime.now()    
    timestamp_str = str(dt.year) + "-" + str("%02d"%dt.month) + "-"
    timestamp_str += str("%02d"%dt.day) + " " + str("%02d"%dt.hour)
    timestamp_str += str("%02d"%dt.minute) + str("%02d"%dt.second) + ":"
    # timestamp_str += str("%02d"%dt.microsecond)
    return timestamp_str

def tweet(message):
    time = RUN 
    file = "c-mLog_", time, ".log"
    file.writelines(self, message)

def ishareOpinion(speakerNode, listenerNode):
    """
    :param speakerNode:
    :param listenerNode:
    :return:
    """
    speakerOpinion = speakerNode["hasOpinion"]
    listenerOpinion = listenerNode["hasOpinion"]

    # "...the probability of the interaction listed in row eight [of Table 1] (AB -A-> B ==> AB-AB) is equal to the
    # probability that a node is state B is chose as listener (nABnA) times the probability that the speaker voices
    # opinion A (1/2)." p.2  So, there are even odds that speaker with opinion AB voices one or the other.
    if speakerOpinion == 'AB':
        speakerOpinion = random.choice(['A', 'B'])

    if speakerOpinion == 'A':
        if listenerOpinion == 'A':
            return
        elif listenerOpinion == 'AB':
            listenerNode["hasOpinion"] = 'B'
            return
        elif listenerOpinion == 'B':
            listenerNode["hasOpinion"] = 'AB'
            return
        else:
            message = "At timestamp ", time(), " Node ", listenerNode, " had anomolous opinion ", listenerOpinion
            tweet(message)
            return

    elif speakerOpinion == 'B':
        if listenerOpinion == 'B':
            return
        elif listenerOpinion == 'AB':
            listenerNode["hasOpinion"] = 'B'
            return
        elif listenerOpinion == 'A':
            listenerNode["hasOpinion"] = 'AB'
            return
        else:
            message = "At timestamp " + time() + " Node " + listenerNode + " had anomolous opinion " + listenerOpinion
            tweet(message)
            return

    else:
        message = "At timestamp " + time() + " speaker Node " + speakerNode + " had anomolous opinion " + speakerOpinion
        tweet(message)
        return

def nShareOpinion(elements):
    """
    :param elements: list of return elements from the cypher query
    :return: null
    """
    speakerOpinion = elements[0]
    listenerNode = elements[1]
    listenerOpinion = elements[2]

    # "...the probability of the interaction listed in row eight [of Table 1] (AB -A-> B ==> AB-AB) is equal to the
    # probability that a node is state B is chose as listener (nABnA) times the probability that the speaker voices
    # opinion A (1/2)." p.2  So, there are even odds that speaker with opinion AB voices one or the other.
    if speakerOpinion == 'AB':
        speakerOpinion = random.choice(['A', 'B'])

    if speakerOpinion == 'A':
        if listenerOpinion == 'A':
            return
        elif listenerOpinion == 'AB':
            listenerNode["hasOpinion"] = 'B'
            return
        elif listenerOpinion == 'B':
            listenerNode["hasOpinion"] = 'AB'
            return
        else:
            message = "At timestamp ", time(), " Node ", listenerNode, " had anomolous opinion ", listenerOpinion
            tweet(message)
            return

    elif speakerOpinion == 'B':
        if listenerOpinion == 'B':
            return
        elif listenerOpinion == 'AB':
            listenerNode["hasOpinion"] = 'B'
            return
        elif listenerOpinion == 'A':
            listenerNode["hasOpinion"] = 'AB'
            return
        else:
            message = "At timestamp " + time() + " Node " + listenerNode + " had anomolous opinion " + listenerOpinion
            tweet(message)
            return

    else:
        message = "At timestamp " + time() + " speaker Node " + speakerNode + " had anomolous opinion " + speakerOpinion
        tweet(message)
        return

def iReport():
     # Print out the ratio of nodes with opinion A vs AB vs B as percentages
     try:
         a_nodes = len(erGraph.vs.select(hasOpinion_eq = 'A'))
     except:
         a_nodes = 0
     try:
         b_nodes = len(erGraph.vs.select(hasOpinion_eq = 'B'))
     except:
         b_nodes = 0
     try:
         ab_nodes = len(erGraph.vs.select(hasOpinion_eq = 'AB'))
     except:
         ab_nodes = 0

     a_ratio = (a_nodes * 1.0)/(N * 1.0)
     b_ratio = (b_nodes * 1.0)/(N * 1.0)
     ab_ratio = (ab_nodes * 1.0)/(N * 1.0)

     report = [a_ratio, ab_ratio, b_ratio]
     return report

def nReport():
    """
    Takes no input parameters and returns ratios in list format
    :return: list of ratios for agents with opinion A, opinion B and opinion AB
    :rtype: list
    """
    a_query = "MATCH (a:Agents {hasOpinion:'A'}) RETURN count(a)"
    b_query = "MATCH (a:Agents {hasOpinion:'B'}) RETURN count(a)"
    ab_query = "MATCH (a:Agents {hasOpinion:'AB'}) RETURN count(a)"
    queries = [a_query, ab_query, b_query]   # Must be in the correct order or confusing things happen
    report = []
    for q in queries:
        response = cypher.execute(nGraph, q)
        r, = response[0]
        r = r[0]
        report.append((r * 1.0) / (N * 1.0))
    return report

def iInteract():
    # Grab 100 random nodes (speakers) and for each of those speakers we grab a listener
    active_nodes = random.sample(erGraph.vs, 100)
    for a in active_nodes:
        ishareOpinion(a, random.choice(a.successors()))

def nInteract():
    """
    Grab 100 random relations in the form: 'speaker opinion', 'listener', 'listener opinion' and pass them to the
    nShareOpinion method. I use the py2neo cypher methods to pass the following query to the database.
    MATCH (a:Agents)-[SpeaksTo]->(b:Agents)
    WITH a, b, rand() AS c
    ORDER BY c
    RETURN a.hasOpinion,b,b.hasOpinion
    LIMIT 100;
    :return: list in the order of the RETURN statement
    """
    query = "MATCH (a:Agents)-[SpeaksTo]->(b:Agents) WITH a, b, rand() AS c ORDER BY c RETURN a.hasOpinion,b,b.hasOpinion LIMIT 100;"
    cypher.execute(nGraph, query, row_handler=nShareOpinion)


if __name__ == '__main__':
    main()

    # ###########
    # Study Cases
    # ###########
    # From the paper Section II, A. we look first at Complete Graph, infinite network size limit


    # Section II, B. Finite network size: Scaling results for consensus times


    # Section III. Erdos-Renyi exponential random graph, sparse networks
    # For iGraph, Erdos_Renyi(n, p, m, directed=False, loops=False) generates a graph based on the Erdos-Renyi model.
    # Initial values for n = 25,000 and p = .51. Graph generation consumes 4:53.206 processor time.

    # With all other applications closed, asking iGraph to generate an ER graph of 50,000 nodes fails. Generating a graph
    # with 35,000 nodes consumes (1.3GiB of 15.6Gib RAM, baseline for OS and PyCharm, etc) up to 15.3 GiB RAM with
    # intermitant drops to Swap space (on a 6Gibps SSD). Execution time is 9:47.906m (processor time, not clock time).
    # 40,000 nodes fails.
    #
    # Because edges consume more memory than nodes, another run with 50,000 nodes and edge p = .21 generates an ER graph in
    # 8:18.195 processor time.

    # I use iGraph to generate an Erdos-Renyi random graph using the experiment parameters for number of nodes and edge
    # probability. Each node gets an attribute "hasOpinion", set by default to 'A' and a percentage are changed to 'B'.
    #
    print "Generating Erdos-Renyi random graph with iGraph. Note: time to completion in next time stamp."
    erGraph = Graph.Erdos_Renyi(N, EP, directed=True, loops=False)
    erGraph.vs["hasOpinion"] = 'A'

    # Give a random sample of nodes the minority opinion
    b_list = random.sample(range(N), P)
    for b in b_list:
        erGraph.vs[b]["hasOpinion"] = 'B'

    # Print time stamp for graph creation
    timing.log(clock())

    # # REPL Timeout may have been root cause of occasional 137 exits on graphs with 100K+ nodes; snooze to prevent.
    # print "Sleeping for 60 seconds before starting the model..."
    # sleep(60)
    # timing.log(clock())

    # g = erGraph # Copy the Erdos-Renyi random graph to a working copy; don't want to destroy raw data
    # #
    iReport()

    data = []

    while iReport()[2] != 0.0 and iReport()[2] != 1.0:
        iInteract()
        data.append(iReport())
        print "Current ratios for A/AB/B are: ", iReport()[0], "/", iReport()[1], "/", iReport()[2]


    # Check time stamp after the model has resolved for the iGraph version
    timing.log(clock())

    fname = "data/iGraph_" + getTimeStampString() + ".csv"

    with open(fname, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["A ratio", "AB ratio", "B ratio"])
        writer.writerows(data)

    print "The network is resolved for the iGraph version."

    timing.log(clock())
    # Section IV. Generate 100k nodes in Neo4j

    # Set the connection to the graph database server
    nGraph = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")
    session = cypher.Session()

    # Define the agents index
    # agents = nGraph.get_or_create_index(neo4j.Node, "Agents")
    #
    # # Define the edges
    # #speaksTo = nGraph.get_or_create_index(neo4j.Relationship, "SpeaksTo")
    #
    # # Initiate a batch. This is a temporary collection for batch processing.
    # batch = neo4j.WriteBatch(nGraph)
    # i = 0
    # for v in erGraph.vs:
    #     # name = "N" + str(v.index)
    #     opinion = v["hasOpinion"]
    #     # n = batch.create({"name": name, "hasOpinion": opinion})
    #     n = batch.create({"hasOpinion": opinion})
    #     #batch.add_indexed_node("Agents", "name", name, n)
    #     # if opinion == 'A':
    #     #     batch.add_indexed_node("a_list", "hasOpinion", "A", n)
    #     # elif opinion == 'B':
    #     #     batch.add_indexed_node("b_list", "hasOpinion", "B", n)
    #     # else:
    #     #     batch.add_indexed_node("ab_list", "hasOpinion", "AB", n)
    #
    #     if i % 1000 == 0:
    #         batch.submit()
    #         batch = neo4j.WriteBatch(nGraph)
    #     i += 1
    # batch.submit()
    # Submit the batch to the server and dissolve the collection

    # Time check after node creation
    # timing.log(clock())

    # new_node_ref = index.get("hasOpinion", "B")

    # nGraph.create(rel(speaker, "SpeaksTo", listener)
    # batch = neo4j.WriteBatch(nGraph)
    # l = 10000
    # i = 0
    # for ep in erGraph.get_edgelist():
    #     speaker = nGraph.node(ep[0])
    #     listener = nGraph.node(ep[1])
    #     batch.create(rel(speaker, "SpeaksTo", listener))
    #     # These seems to be some limitations on the batch size. Thanks to Nigel Small for the answer on SO
    #     # http://stackoverflow.com/questions/24657190/py2neo-neo4j-batch-submit-error?rq=1
    #     if i % 10000 == 0:                       # Batches of 500 work on my machine. Let's try 1,000
    #         batch.submit()                      # Submit this batch, dissolve the collection
    #         batch = neo4j.WriteBatch(nGraph)    # Initiate a new batch collection
    #         sleep(1)
    #     print "Have loaded  ", l/75000000.0, "% of 75,000,000 edges."
    #     i += 1
    #     l += 1
    #     if l % 1000000 == 0:
    #         timing.log(clock())
    #     # timing.log(clock())
    # batch.submit()                              # Submit the final batch
    # # batch.clear()
    # # Check the time after the neo4j edges have been created
    # timing.log(clock())
    #
    # print "...and....done!"

    nReport()

    data = []

    while nReport()[2] != 0.0 and nReport()[2] != 1.0:
        nInteract()
        data.append(nReport())
        print "Current ratios for A/AB/B are: ", nReport()[0], "/", nReport()[1], "/", nReport()[2]

    # Gruppo compacto, so we take the final time stamp
    timing.log(clock())

    fname = "data/nGraph_" + getTimeStampString() + ".csv"

    with open(fname, 'wb') as f:
        writer = csv.writer(f)
        writer.writerow(["A ratio", "AB ratio", "B ratio"])
        writer.writerows(data)

    print "The network is resolved for the Neo4j version."



