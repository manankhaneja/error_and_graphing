#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  24 19:28:30 2018

@author: manan
"""
# Plotting is preliminary and I will improve it in a day or two.
#Try it for any excel data you have and let me know the areas of improvement (except plotting)
#For verification, a simple check can be made. Check if the errors are correctly calculated for any arbitary case.- errors are printed in output before plot.

from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (16, 9)
def dataset():
    address = input("Enter the location of xlsx file: -Full file name with address \n")
    sheet = input("Enter the sheet name: \n")
    data = pd.read_excel(address, sheet)
    print(data)
    return (data)

def dependencies(data,points): #NOTE - All dependencies of the error function in the working formula should be in the dataframe
    dependence = {}
    flag = 1
    while flag:
        column = int(input("Enter the dependence column number (column numbers start from 0) \n"))
        name = (list(data.columns.values))[column]
        colarray = points[:,column]
        print("The least count for ",name, "\n" )
        colerror = float(input("Enter the least count \n" ))
        dependence.update({name:[colarray, colerror]})
        flag=int(input("Is there any other dependence? \n0. NO \n1. YES\n"))
    return(dependence)

def readingerror(dependence):
    variablelist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    vlist = []
    var = {}
    i = 0
    dependency = {}
    for key in dependence.keys():
        vlist.append(variablelist[i])
        print( key," is mapped as ",variablelist[i], " --enter the formula in terms of the mapped variables \n")
        dependency.update({vlist[i]: dependence[key]})
        i = i+1
    formulastring = input("Enter the formula: Dependent variable = \n Note: log is interpreted as natural logarithm \n")

    for l in range(len(vlist)):
        var.update({vlist[l]:symbols(vlist[l], real = True)})

    formula = parse_expr(formulastring ,local_dict=var)
    error = []
    errformulalist = [abs((Derivative(formula,var[vlist[k]]).doit()) * dependency[vlist[k]][1]) for k in range(len(vlist))]
    errformula = sum(errformulalist)

    for i in range(len(dependency['a'][0])):
        err = errformula.evalf(subs= {var[vlist[j]]:(dependency[vlist[j]][0])[i] for j in range(len(vlist))})
        error.append(err)

    return(error)
    
def theoretical(dependence):
    variablelist = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
    vlist = []
    var = {}
    value = []
    i = 0
    dependency = {}
    for key in dependence.keys():
        vlist.append(variablelist[i])
        print( key," is mapped as ",variablelist[i], " --enter the formula in terms of the mapped variables \n")
        dependency.update({vlist[i]: dependence[key]})
        i = i+1
    indepvar = input("Enter the independent variable to plot")
    formulastring = input("Enter the formula: Dependent variable = \n Note: log is interpreted as natural logarithm \n")

    for l in range(len(vlist)):
        var.update({vlist[l]:symbols(vlist[l], real = True)})

    formula = parse_expr(formulastring ,local_dict=var)

    for i in range(len(dependency['a'][0])):
        val = formula.evalf(subs= {var[vlist[j]]:(dependency[vlist[j]][0])[i] for j in range(len(vlist))})
        value.append(val)

def plot(x,y,yerror):
    
    ax = plt.axes()
    ax.xaxis.set_major_locator(plt.MaxNLocator(10))
    ax.xaxis.set_minor_locator(plt.MaxNLocator(100))
    ax.yaxis.set_major_locator(plt.MaxNLocator(10))
    ax.yaxis.set_minor_locator(plt.MaxNLocator(100))
    flag = int(input("Do you want to plot semi log? \n0. NO \n1. YES\n"))
    if flag:
        ax.set_xscale("log")
       
    plt.errorbar(x,y, yerr= yerror,fmt='o', linewidth=1, markersize=4, capsize=2, label = "Experimental")
    ax.grid(which = 'major', linestyle='-', linewidth = 0.9, alpha=1.0)
    ax.grid(which = 'minor', linestyle=':', linewidth = 0.6, alpha=0.8)
    plt.xticks(rotation='vertical')
    xlab = input("Enter the x label \n")
    ylab = input ("Enter the y label \n")
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    p = np.polyfit(x,y,1)
    plt.plot(x, p[1]+p[0]*x)
    x = x.astype(np.float64,copy=False)
    y = y.astype(np.float64,copy=False)
    plt.legend(loc = 'upper left')
    plt.savefig('fig1.png',dpi=400)
    plt.show()
    

def main():
    print("Welcome to Graphing 101: Error analytics in 2D plotting  \n")
    data = dataset()
    points = np.array(data)
    indepvar = int(input("Enter column number for independent variable (Column numbers start from 0) \n"))
    depvar = int(input("Enter column number for dependent variable (Column numbers start from 0) \n"))
    x = points[:,indepvar]
    print(type(x[0]))
    y = points[:,depvar]
    print(y)
    flag = int(input("Want to add reading error? \n0.NO \n1.YES\n"))        #As of now, the program can only include instrumental/reading error. Statistical manipulations will be added soon.
    yerror = 0
    if flag:
        dependence = dependencies(data,points)
        yerror = readingerror(dependence)
    print(yerror)
    plot(x,y,yerror)

if __name__=='__main__':
    main()
