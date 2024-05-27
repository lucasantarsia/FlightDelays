import networkx as nx

from database.DAO import DAO
from model.model import Model

mymodel = Model()
mymodel.buildGraph(5)
mymodel.printGraphDetails()

