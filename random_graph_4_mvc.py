#!/usr/bin/env python

import sys
import getopt
import random

#generate graph based on g_n_m model
def generate_random_graph(n ,m):
	g = []
	fullgraph = []
	for i in range(1 ,n+1):
		for j in range(i+1 ,n+1):
			fullgraph.append((i ,j))
	clen = len(fullgraph)
	m = min(clen ,m)
#print fullgraph
	g.append((n ,m))
	for i in range(0 ,m):
		rind = random.randint(0 ,clen-1)
		g.append(fullgraph[rind])
		fullgraph[rind] = fullgraph[clen-1]
		clen = clen - 1
	
	return g

def graph_hash(g):
	v = g[0][0]
	deg = [0] * (v+1)
	for e in g[1:]:
		deg[e[0]] = deg[e[0]] + 1
		deg[e[1]] = deg[e[1]] + 1
	deg_class = [0] * v
	for ve in range(1 ,v+1):
		deg_class[deg[ve]] = deg_class[deg[ve]] + 1
	g_hash = 0
	base = 1
	for d in range(0 ,v):
		g_hash = g_hash + base * deg_class[d]
		base = base * v
	return g_hash

def readGraph(filename):
	try:
		graph=[]
		edges=[]
		clq = 0
		fin = open(filename ,'r')
		for line in fin.readlines():
			ll = line.split()
			if ll[0] == 'c':
				if ll[1] == "mvc":
					clq = int(ll[2])
			elif ll[0] == 'p':
				v = int(ll[2])
				e = int(ll[3])
				graph.append((v,e,clq))
			elif ll[0] == 'e':
				graph.append((int(ll[1]),int(ll[2])))
		return graph
		print graph
	except IOError:
		print "IOError in open file"
		exit (0)


#count all min vertex cover in graph g
#return the number of mvc
def count_mvc(g):
#	print g
	v = g[0][0]
	e = g[0][1]
#	print len(g)
#	print e
	mvc = v
	res =[]
	vc_num = 0
	for i in range(0 ,1<<v):
		sel=[0]*(v+1)
		vc = 0
		for j in range(1 ,v+1):
			if ((1<<(j-1)) & i) != 0:
				vc = vc+1
				sel[j] = 1
		is_vc = 1
		for j in range(1 ,e+1):
			v1 = g[j][0]
			v2 = g[j][1]
			if sel[v1]==0 and sel[v2] == 0:
				is_vc = 0
				break
		if is_vc == 1 and vc < mvc:
			res = sel
			mvc = vc
			vc_num = 1
		if is_vc == 1 and vc == mvc:
			vc_num = vc_num + 1
	res = [mvc ,vc_num]
	return res
# function ends

#sort vertex by degree 
#delete all vertices without neighbour
#return vertices list sorted by degree
def sort_vertex(v ,vertices ,adj_matrix):
	deg = [0]*(v+1)
	for i in range(0 ,len(vertices)):
		for j in range(i+1 ,len(vertices)):
			if adj_matrix[vertices[i]][vertices[j]] == 1:
				deg[vertices[i]] = deg[vertices[i]]+1
				deg[vertices[j]] = deg[vertices[j]]+1
#	print "deg: " ,deg	
	table=[]
	for i in range(0 ,v+1):
		table.append([])
	sg = []
#	print "vertices :" ,vertices
	for i in range(0 ,len(vertices)):
		table[deg[vertices[i]]].append(vertices[i])
#print table
	t=range(1,len(vertices))
	t.reverse()
	for i in t:
		for j in range(0 ,len(table[i])):
			sg.append(table[i][j])
#	print "sg:" ,sg	
	return sg
#function ends

#check if vc is a vertex cover in graph g
def check_vertex_cover(g,vc):
	e = g[0][1]
	v = g[0][0]
#print g[1:]
#print vc
	covered=[0]*(v+1)
	for i in vc:
		covered[i] = 1
	for edge in g[1:]:
		if covered[edge[0]] == 0 and covered[edge[1]] == 0:
			return 0
	return 1

#find the vertex with the max degree in graph (edges)
#return the vertex selected
def select_vertex(v ,edges):
	deg = [0]*(v+1)
	for i in range(0 ,len(edges)):
		deg[edges[i][0]] = deg[edges[i][0]] + 1
		deg[edges[i][1]] = deg[edges[i][1]] + 1
	sv = 0
	mmd = 0
	for i in range(1 ,v+1):
		if (deg[i] > mmd):
			mmd = deg[i]
			sv = i
	return sv

#search for mvc using greedy algorithm by degree
#return the number of backtrack
def min_vertex_cover(g,mvc):
	v = g[0][0]
	e = g[0][1]
	adj_matrix = []
	for i in range(0 ,v+1):
		adj_matrix.append([0]*(v+1))
	for i in range(1,e+1):
		v1 = g[i][0]
		v2 = g[i][1]
		adj_matrix[v1][v2] = adj_matrix[v2][v1] = 1
#print "adj_matrix :" ,adj_matrix	
	vertices=[]
	for i in range(1,v+1):
		vertices.append(i)
#print "vertices:" ,vertices
	edges=[]
	for i in range(1,v+1):
		for j in range(i+1,v+1):
			if adj_matrix[i][j] == 1:
				edges.append((i,j))
	sv = select_vertex(v,edges)
	vc = []
	stack=[]
	state=[0,[],sv,edges]
	stack.append(state)
	backtrack_times = 0
	while len(stack) != 0:
		state = stack[-1]
	#	print state
		if len(state[1]) >= mvc:
			backtrack_times = backtrack_times + 1
			stack.pop()
		else:
			if state[0] == 0:
				state[0] = 1
				clq = state[1][:]
				clq.append(sv)
				edges=[]
				for edge in state[3]:
					if edge[0] != sv and edge[1] != sv:
						edges.append(edge)
				if len(edges) == 0:
#print "clq:" ,clq
					if len(clq) == mvc:
						if check_vertex_cover(g,clq) == 0:
							print "Error MaxClique!!!"	
						return backtrack_times
				else:
					sv = select_vertex(v,edges)
					stack.append([0,clq,sv,edges])
			elif state[0] == 1:
				state[0] = 2
				sv = state[2]
				clq = state[1][:]
				for ve in range(1,v+1):
					if adj_matrix[sv][ve] == 1 and ve not in state[1]:
						clq.append(ve)
				edges = []
				for edge in state[3]:
					if adj_matrix[sv][edge[0]] == 0 and adj_matrix[sv][edge[1]] == 0:
						edges.append(edge)
				if len(edges) == 0:
					if len(clq) == mvc:
#print "clq:" ,clq
						if check_vertex_cover(g,clq) == 0:
							print clq
							print "Error MaxClique!!!!"	
						return backtrack_times
				else:
				 	sv = select_vertex(v ,edges)
				 	stack.append([0,clq,sv,edges])
			else:
				backtrack_times = backtrack_times + 1
				stack.pop()
	return backtrack_times	  
#function ends

if __name__ == "__main__":
	oplist ,argv = getopt.getopt(sys.argv[1:] ,'gf')
	if len(oplist) == 0:
		print "Error options"
		exit(-1)
	clq = 0
	counter = 1
	random.seed()
	if oplist[0][0] == '-g':
		if len(argv) < 2:
			print "No enough arguments"
			exit(-1)
		n = int (argv[0])
		m = int (argv[1])
		if (len(argv) > 2):
			counter = int(argv[2])
	elif oplist[0][0] == '-f':
		g = readGraph(argv[0])
		if g == [] :
			print "InputFile formate error\n"
			exit (-1)
		clq = g[0][2]
		bts = min_vertex_cover(g ,clq)
#	print "clq:" ,clq ,"bts:" ,bts
		exit (-1)
	else:
		print "Error options"
		exit(-1)
	mmap = set()
#	print n , m ,counter	
	for i in range(0 ,counter):
		g = generate_random_graph(n ,m)
		g_hash = graph_hash(g)
		while g_hash in mmap:
			g = generate_random_graph(n ,m)
			g_hash = graph_hash(g)
			print "generate the same hash value"
		mmap.add(g_hash)
		vc_ct = count_mvc(g)
		clq = vc_ct[1]
		bts = min_vertex_cover(g, clq)
		print "clq:" ,clq ,"bts:" ,bts
		filename = "gnm_" + str(g[0][0]) + "_" + str(g[0][1]) + "_" + str(i) + ".clq"
		try:
			fin = open(filename ,"w")
			fin.write("c " + filename + "\n")
			fin.write("c mvc %d\n"%(clq));
			fin.write("c vertex cover size %d , number %d\n"%(vc_ct[0],vc_ct[1]))
			fin.write("c steps %d\n"%(bts))
			edge = g[1:]
			fin.write("p edge %d %d\n"%(n ,len(edge)))
			for i in range(0 ,len(edge)):
				fin.write ("e %d %d\n"%(edge[i][0] ,edge[i][1]))
			fin.close()
		except IOError:
			print "Open file error " ,filename

            
