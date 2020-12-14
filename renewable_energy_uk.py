#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""    _ 
      /  |     | __  _ __  _
     /   |    /  |_||_|| ||
    /    |   /   |  |\ | ||_
   /____ |__/\ . |  | \|_|\_|
   __________________________ .
   
Created on Mon Dec 14 17:13:08 2020

@author: chrisunderwood
"""
import numpy as np
import matplotlib as mpl
np.set_printoptions(precision=3)
import matplotlib.pyplot as plt

# Load my module of functions
import sys
sys.path.insert(0, '/Users/chrisunderwood/Documents/Python/')
import CUnderwood_Functions3 as func
import pandas as pd

from mpl_toolkits.basemap import Basemap
sys.path.insert(0, '/Users/chrisunderwood/Documents/Location/')
from Locations_Plot import returnMap, draw_map

mpl.rcParams['figure.figsize'] = [15.0, 12.0]
labelSize = 15
mpl.rcParams['ytick.labelsize'] =  labelSize
mpl.rcParams['xtick.labelsize'] =  labelSize
mpl.rcParams['axes.labelsize'] =  labelSize
mpl.rcParams['legend.fontsize' ] =  labelSize
mpl.rcParams['axes.titlesize'] =  labelSize + 2
mpl.rcParams['legend.title_fontsize' ] =  labelSize
mpl.rcParams['figure.titlesize'] = labelSize + 3

       


def get_windfarms(df):
    cropArray = np.zeros_like(  df["Technology Type"], dtype=bool)
    cropArray += df["Technology Type"] == "Wind Onshore"
    cropArray += df["Technology Type"] == "Wind Offshore" 
    cropArray
    dfWind = df[cropArray]
    dfWind  = dfWind.reset_index()

    return dfWind, cropArray


def get_solar(df):
    dfSolar = df[df["Technology Type"] == "Solar Photovoltaics"]
    dfSolar  = dfSolar.reset_index()
    return dfSolar
    

def coors_cap_df(df):
    dfCoors = df[['X-coordinate', 'Y-coordinate', 'Installed Capacity (MWelec)']]    
    dfCoors = dfCoors.rename(columns={'X-coordinate':"x", 'Y-coordinate':"y", 'Installed Capacity (MWelec)':"cap"})
    return dfCoors

def aspectShow():
    plt.gca().set_aspect('equal')
    plt.show()    
    
def capacity_map(dfCoors):

    im = plt.scatter(dfCoors['x'], dfCoors['y'], 
                      s = dfCoors['cap'],
                     c = dfCoors['cap'] )
    plt.colorbar(im)
    aspectShow()    

if __name__ == '__main__':
    
    root = "/Volumes/CIDU_passport/Renewable_Energy_Map_Project/"
    fp = root + "renewable_energy_planning_db_2020_09.xlsx"
    
    try:
        df
        print ("df already loaded")
    except NameError:
        df = pd.read_excel(fp)     
        dfCoors = coors_cap_df(df)

        print ("df loaded")    
        
        dfWind, cropArray = get_windfarms(df)
        dfWindCoors = coors_cap_df(dfWind)

        dfSolar = get_solar(df)
        dfSolarCoors = coors_cap_df(dfSolar)
        
        
# =============================================================================
#     
#     Technology Types
#     np.array(['Advanced Conversion Technologies', 'Anaerobic Digestion',
#            'Battery', 'Biomass (co-firing)', 'Biomass (dedicated)',
#            'EfW Incineration', 'Flywheels', 'Fuel Cell (Hydrogen)',
#            'Hot Dry Rocks (HDR)', 'Landfill Gas', 'Large Hydro',
#            'Liquid Air Energy Storage', 'Pumped Storage Hydroelectricity',
#            'Sewage Sludge Digestion', 'Shoreline Wave', 'Small Hydro',
#            'Solar Photovoltaics', 'Tidal Barrage and Tidal Stream',
#            'Wind Offshore', 'Wind Onshore'], dtype=object)
# =============================================================================
    
    # techTypes = np.unique(df['Technology Type'])
    # n, c = np.unique(df['Technology Type'], return_counts=True)
    # for ni, ci in zip(n, c):
    #     print(ni, '\t\t', ci)


    # plt.plot(dfCoors['x'], dfCoors['y'] , '.')
    # aspectShow()
    
    if False:
        capacity_map(dfCoors)
        capacity_map(dfWindCoors)
        capacity_map(dfSolarCoors)
        
    
    
    
    im = plt.scatter(dfSolarCoors['x'], dfSolarCoors['y'], 
                      # s = dfWind['No. of Turbines']*4,
                     c = dfSolarCoors['cap'],
                     ec= 'k',
                     vmax = np.unique(dfSolarCoors['cap'])[-3],
                    cmap = 'spring',
                     )
    cb = plt.colorbar(im)
    cb.set_label("Solar Capacity (MW)")

                     
    im = plt.scatter(dfWindCoors['x'], dfWindCoors['y'], 
                      s = dfWind['No. of Turbines']*4,
                     c = dfWindCoors['cap'],
                     ec= 'k',
                    cmap = 'winter'                     
                     )
    cb = plt.colorbar(im)
    cb.set_label("Wind Capacity (MW)")
    
    # lArr = len(np.unique(dfWind['No. of Turbines'][cropArray]))
    # msizes = np.unique(dfWind['No. of Turbines'][cropArray])[np.arange(10, lArr, 10)]
    msizes = [1, 5, 10, 50, 100, 200, 400]
    msizes = msizes[::-1]
    markers = []
    for size in msizes:
       markers.append(plt.scatter([],[], s=size*4, label=size, c='w', ec='k'))
    
    plt.legend(handles=markers, title = "Number of Wind\nTurbines")
    aspectShow()        


                     
    
                         
    
    
    