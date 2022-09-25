#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 20:16
# @Author  : wuhao
# @Email   : guess?????
# @File    : test_rpy2.py
import rpy2.robjects as robjects
from rpy2.robjects.packages import importr
import csv
import networkx as nx
import pandas as pd
import collections
#‘pi’为R的内置变量
# 第一种
# t0 = robjects.r['pi']
# print(t0[0])

# creat an R function，自定义R函数
#python 调用RRRR
robjects.r('''
library(igraph)
library('Matrix')
library(purrr)
library(tidyverse)
''')
robjects.r('''
    nodedist<-function(g){
    N<-length(V(g))
    r<-c()
    dg=shortest.paths(g,mode=c("all"),algorithm=c("unweighted"))#geodesic distance
    dg[which(dg==Inf)]=N
    q=setdiff(intersect(dg,dg),0)
    a=Matrix(0,ncol=N,nrow=N)
    for(i in (1:length(q))){
    b=dg
    b[which(b!=q[i])]=0
    a[1:N,q[i]]=colSums(b)/q[i]
}
return(a/(N-1))
}
           ''')
robjects.r('''
            diversity<-function(a){
            div=0
            while(length(a)>1){
            n=sqrt(length(a))
            a[matrix(c(1:n,1:n),ncol=2)]=1
            div=div+min(a)
            escolhas=ceiling(which(a==min(a))/n)
            b=a[escolhas,]
            r<-c()
            for(j in (1:length(escolhas))){
            r<-c(r,sort(b[j,])[2])
            }
            quem=order(r)[1]
            quem=escolhas[quem]
            a=a[setdiff(1:n,quem),setdiff(1:n,quem)]
            n=sqrt(length(a))
            }
            return(div)
            }
           ''')
robjects.r('''
get_diversity_value_list<-function(file_name_path){
        data <-read.csv(file_name_path,fileEncoding = "UTF-8-BOM",skip=1,header = T)
        edges <- data[,1:2]
        graph_test <- graph_from_data_frame(edges, directed = FALSE, vertices=NULL)
        adjacent_distance <- dist(nodedist(graph_test),method="euclidean")
        diversity_value <- diversity(as.matrix(adjacent_distance))
        return(diversity_value)
}
           ''')