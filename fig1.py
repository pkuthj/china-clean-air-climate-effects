import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import pandas as pd
import os



plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 12


## fig1a

df = pd.read_excel(r'.\SO2_3.xlsx')

fig, ax = plt.subplots(figsize=(13, 7))
min_year = df['year'].min()
max_year = df['year'].max()
xticks_positions = np.arange(min_year, max_year + 1, 5)
ax.set_xticks(xticks_positions)
ax.set_xticklabels([str(int(x)) for x in xticks_positions],fontsize = 18)
ax.tick_params(axis='y', labelsize=18)

ax.plot(df['year'], df['CEDS'], marker='o', markersize=5.3, linewidth=2, 
        label='CEDS', color="#FBB41C")  # 蓝色
ax.plot(df['year'], df['EDGAR'], marker='o', markersize=5.3, linewidth=2, 
        label='EDGAR', color='#BD3752')  # 红色
ax.plot(df['year'], df['GEMS'], marker='o', markersize=5.3, linewidth=2, 
        label='GEMS', color='#7A1B6D')   # 黑色-

ax.set_xlabel('Year', fontsize=14, fontweight='bold')
ax.set_ylabel('SO$_2$ emission (Gg)', fontsize=20, fontweight='bold')

start_shadow_year = 2010
end_shadow_year = df['year'].max()

ax.axvspan(start_shadow_year, end_shadow_year, alpha=0.2, color="#2926C5", label='Post-2013 Period')
plt.tight_layout()
plt.savefig('BC_trend_comparison.png', dpi=300, bbox_inches='tight')
plt.savefig('BC_trend_comparison.pdf', bbox_inches='tight')  # 矢量图
plt.xlim(1980,2022)

save_path = r'D:\MODEL\OSCAR-master-cn2025\fig\fig1a.pdf'
plt.savefig(
    save_path,
    format='pdf',
    bbox_inches='tight',        
    dpi=300,                    
    transparent=False,          
    facecolor='white'           
)

## fig1b

data = {
    "Year": [2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
    "EDGAR": [0.000, 4.472, 6.049, 5.575, 2.914, 0.805, -4.846, -9.030, -14.522, -16.539, -18.995, -15.337, -15.452],
    "GEMS": [0.000, -7.643, -15.720, -23.521, -29.651, -42.044, -45.968, -50.075, -53.731, -57.377, -60.050, np.NaN,np.NaN],
    "CEDS": [0.000, 3.866, 1.537, -7.914, -24.142, -36.142, -47.732, -57.322, -60.824, -63.782, -66.205, -66.632, -66.542]
}

fig, ax = plt.subplots(figsize=(3.4, 2.8))
colors = {'CEDS': '#FBB41C', 'EDGAR': '#BD3752', 'GEMS': '#7A1B6D'}
labels = {'CEDS': 'CEDS', 'EDGAR': 'EDGAR', 'GEMS': 'GEMS'}

for var in ['CEDS', 'EDGAR', 'GEMS']:
    df_sub = df[(df['Year'] >= 2010) & (df['Year'] <= 2020)].copy()  
    x = df_sub['Year'].values
    y = df_sub[var].values
    
    mask = ~np.isnan(y)
    x_fit = x[mask]
    y_fit = y[mask]
    
    a, b = np.polyfit(x_fit, y_fit, 1)  # y = a*x + b
    fit_y = np.polyval([a, b], x)  
    
    ax.plot(x, y, '-o', color=colors[var], linewidth=1.5, markersize=3.5, label=labels[var])
    ax.plot(x, fit_y, '--', color=colors[var], linewidth=1.0, alpha=0.8)
    
    ypos_dict = {'GEMS': -43, 'CEDS': -39, 'EDGAR': -35}  
    ax.text(2010.2, ypos_dict[var], f"{labels[var]} slope = {a:.3f} %/yr",
            color=colors[var], fontsize=7, ha='left', va='bottom')

ax.axhline(0, color='black', linewidth=0.6, linestyle='--')
ax.set_xlabel("Year", fontsize=8)
ax.set_ylabel("Relative change since 2010 (%)", fontsize=8)
ax.set_xlim(2010, 2020)
ax.set_ylim(-70, 10)
ax.set_xticks(range(2010, 2021, 2))
ax.set_yticks([-45, -35, -25, -15, 0, 10])
ax.tick_params(axis='both', which='major', labelsize=7.5, direction='in', length=3, width=0.8)
ax.tick_params(axis='both', which='minor', direction='in', length=1.8, width=0.6)
ax.tick_params(axis='x',labelsize = 6)

ax.tick_params(axis='y', labelsize= 6)
ax.minorticks_on()
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(0.8)
    spine.set_color('black')
ax.legend(frameon=False, fontsize=7.5, loc='upper right', handlelength=2.2, handletextpad=0.5)
plt.grid(False)
plt.tight_layout(pad=0.2)
save_path = r'D:\MODEL\OSCAR-master-cn2025\fig\fig1b.pdf'
fig.savefig(
    save_path,
    format='pdf',
    bbox_inches='tight',
    dpi=300,
    transparent=False,
    facecolor='white'
)