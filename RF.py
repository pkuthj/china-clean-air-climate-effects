import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import os
from core_fct.mod_process import OSCAR
from core_fct.fct_loadP import load_all_param
from core_fct.fct_genMC import generate_config
from run_scripts.get_SSP_drivers import For_hist
from run_scripts.get_SSP_drivers import For_scen


##PART 1

var_keep = [var for var in list(OSCAR._processes.keys()) if 'RF' in var]

Par0 = load_all_param(mod_region='Houghton_2017')
Par = generate_config(Par0, nMC=3000)
Par = xr.merge([Par, For_hist.drop([VAR for VAR in For_hist if 'year' in For_hist[VAR].dims])])
Par.to_netcdf('./results/Par_OSCAR.nc')  
Par = xr.open_dataset('./results/Par_OSCAR.nc')

For_hist = For_hist.drop([VAR for VAR in For_hist if 'year' not in For_hist[VAR].dims])
For_scen = For_scen.sel(year=slice(2015, 2030))
For_scen = For_scen.sel(scen='SSP2-4.5').drop('scen')
For_base = xr.concat([For_hist, For_scen], dim='year')  
For_base = For_base.fillna(0)

Out_base = OSCAR(Ini=None, Par=Par, For=For_base, var_keep=var_keep)
Out_base.to_netcdf('./results/Out_base.nc')
Ini = Out_base.sel(year=1950)
Ini.to_netcdf('./results/Ini.nc')


For_update = For_base.copy(deep=True)


## SO2
unit_change = 1e-3*0.5
emission_dataset = pd.read_excel('./emi_datasets/CEDS_SO2.xlsx')

for _, row in emission_dataset.iterrows():
    year = row['year']
    rog_val = row['ROG'] * unit_change
    china_val = row['China+'] * unit_change

    For_update['E_SO2'].loc[dict(year=year)] = 0.0

    if 0 in For_update['reg_land']:
        For_update['E_SO2'].loc[dict(year=year, reg_land=0)] += rog_val
    if 7 in For_update['reg_land']:
        For_update['E_SO2'].loc[dict(year=year, reg_land=7)] += china_val

## BC
unit_change = 1e-3
emission_dataset = pd.read_excel('./emi_datasets/CEDS_BC.xlsx')
for _, row in emission_dataset.iterrows():
    year = row['year']
    rog_val = row['ROG'] * unit_change
    china_val = row['China+'] * unit_change

    For_update['E_BC'].loc[dict(year=year)] = 0.0

    if 0 in For_update['reg_land']:
        For_update['E_BC'].loc[dict(year=year, reg_land=0)] += rog_val
    if 7 in For_update['reg_land']:
        For_update['E_BC'].loc[dict(year=year, reg_land=7)] += china_val

## OC
unit_change = 1e-3
emission_dataset = pd.read_excel('./emi_datasets/CEDS_OC.xlsx')

for _, row in emission_dataset.iterrows():
    year = row['year']
    rog_val = row['ROG'] * unit_change
    china_val = row['China+'] * unit_change

    For_update['E_OC'].loc[dict(year=year)] = 0.0

    if 0 in For_update['reg_land']:
        For_update['E_OC'].loc[dict(year=year, reg_land=0)] += rog_val
    if 7 in For_update['reg_land']:
        For_update['E_OC'].loc[dict(year=year, reg_land=7)] += china_val


## NOx

unit_change = 1e-3*0.304
emission_dataset = pd.read_excel('./emi_datasets/CEDS_NOX.xlsx')

for _, row in emission_dataset.iterrows():
    year = row['year']
    rog_val = row['ROG'] * unit_change
    china_val = row['China+'] * unit_change

    For_update['E_NOX'].loc[dict(year=year)] = 0.0

    if 0 in For_update['reg_land']:
        For_update['E_NOX'].loc[dict(year=year, reg_land=0)] += rog_val
    if 7 in For_update['reg_land']:
        For_update['E_NOX'].loc[dict(year=year, reg_land=7)] += china_val

## VOC

unit_change = 1e-3
emission_dataset = pd.read_excel('./emi_datasets/CEDS_VOC.xlsx')

for _, row in emission_dataset.iterrows():
    year = row['year']
    rog_val = row['ROG'] * unit_change
    china_val = row['China+'] * unit_change

    For_update['E_VOC'].loc[dict(year=year)] = 0.0

    if 0 in For_update['reg_land']:
        For_update['E_VOC'].loc[dict(year=year, reg_land=0)] += rog_val
    if 7 in For_update['reg_land']:
        For_update['E_VOC'].loc[dict(year=year, reg_land=7)] += china_val

## NH3

unit_change = 1e-3*0.824
emission_dataset = pd.read_excel('./emi_datasets/CEDS_NH3.xlsx')

for _, row in emission_dataset.iterrows():
    year = row['year']
    rog_val = row['ROG'] * unit_change
    china_val = row['China+'] * unit_change

    For_update['E_NH3'].loc[dict(year=year)] = 0.0

    if 0 in For_update['reg_land']:
        For_update['E_NH3'].loc[dict(year=year, reg_land=0)] += rog_val
    if 7 in For_update['reg_land']:
        For_update['E_NH3'].loc[dict(year=year, reg_land=7)] += china_val

## CO

unit_change = 1e-3*0.429
emission_dataset = pd.read_excel('./emi_datasets/CEDS_CO.xlsx')

for _, row in emission_dataset.iterrows():
    year = row['year']
    rog_val = row['ROG'] * unit_change
    china_val = row['China+'] * unit_change

    For_update['E_CO'].loc[dict(year=year)] = 0.0

    if 0 in For_update['reg_land']:
        For_update['E_CO'].loc[dict(year=year, reg_land=0)] += rog_val
    if 7 in For_update['reg_land']:
        For_update['E_CO'].loc[dict(year=year, reg_land=7)] += china_val

For_update.to_netcdf('./results/For_update.nc')  ## 保存OSCAR自带的驱动数据（2014年以前是清单，2014-2030是SSP245）
Out_update = OSCAR(Ini=Ini, Par=Par, For=For_update.sel(year=slice(1950,2030)), var_keep=var_keep)
Out_update.to_netcdf('./results/CEDS_Out_update.nc')

## PART 2

Par = xr.open_dataset('./results/Par_OSCAR.nc')
For_hist = xr.open_dataset('./results/For_update.nc')
Ini = xr.open_dataset('./results/Ini.nc')

species_list = ['SO2', 'VOC', 'BC', 'OC', 'CO', 'NOX', 'NH3']

for species in species_list:
    var_name = f'E_{species}'
    For_hist_mch = For_hist.copy(deep=True)
    For_hist_mrog = For_hist.copy(deep=True)
    For_hist_mch[var_name][:,7] *= 0.99
    for i in [0,1,2,3,4,5,6]+[8,9,10]:
     For_hist_mrog[var_name][:,i] *= 0.99
   
    Out_mch = OSCAR(Ini=Ini, Par=Par, For=For_hist_mch.sel(year=slice(1950,2022)), var_keep=var_keep)
    Out_mrog = OSCAR(Ini=Ini, Par=Par, For=For_hist_mrog.sel(year=slice(1950,2022)), var_keep=var_keep)
    Out_mch.to_netcdf(f'./results/CEDS_e0_Out_mch_{species}.nc')
    Out_mrog.to_netcdf(f'./results/CEDS_e0_Out_mrog_{species}.nc')