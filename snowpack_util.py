#%%

# [[ snowpack_util.py ]]
# read and visualize SNOWPACK's output.

# >>>>>>>>>> IMPORT >>>>>>>>>>
import datetime as dt
import matplotlib
import matplotlib.pyplot as plt
# <<<<<<<<<< IMPORT <<<<<<<<<<

# <<<<<<<<<< CREATE OBJECTS <<<<<<<<<<
class profile:
    def __init__(self, ipt):
        with open(ipt) as f:
            l = f.read().splitlines()
        self.params = [[t.strip() for t in s.split('=')] for s in 
            l[l.index('[STATION_PARAMETERS]')+1:l.index('[HEADER]')-1]
        ]
        self.header = [[t.strip() for t in s.split(',')] for s in
            l[l.index('[HEADER]')+1:l.index('[DATA]')-1]
        ]
        self.data = [[t.strip() for t in s.split(',')] for s in l[l.index('[DATA]')+1:]]
        # https://models.slf.ch/docserver/snowpack/html/snowpackio.html
        self.grain_table = {
            '1': 'PP',
            '2': 'DF',
            '3': 'RG',
            '4': 'FC',
            '5': 'DH',
            '6': 'SH',
            '7': 'MF',
            '772': 'MFcr',
            '8': 'IF',
            '9': 'FCxr',
        }
        self.color_table = {
            'PP': '#00FF00',
            'DF': '#228B22',
            'RG': '#FFB6C1',
            'FC': '#ADD8E6',
            'FCxr': '#ADD8E6',
            'DH': '#0000FF',
            'SH': '#ea33f7',
            'MF': '#FF0000',
            'MFcr': '#FF0000',
            'IF': '#00FFFF',
        }
        # run interpretion
        self.interpret()
    
    def interpret(self):
        flag_first = True
        self.formatted_data = []
        the_dt = the_surface_grain_type = the_surface_grain_size = the_surface_density = 0
        the_height = the_density = the_temperature = the_water = the_dendricity = the_sphericity = the_bond_size = the_grain_size = the_grain_type = the_ice = the_air = the_viscosity = the_soil = the_temperature_gradient = the_thermal_conductivity = the_absorbed_shortwave_radiation = the_viscous_deformation = the_ssi = []
        for row in self.data:
            if row[0] == '0500':  #! datetime
                if flag_first:
                    flag_first = False
                else:
                    #save
                    self.formatted_data.append({
                        'datetime': the_dt,
                        'height': the_height,
                        'density': the_density,
                        'temperature': the_temperature,
                        'water': the_water,
                        'dendricity': the_dendricity,
                        'sphericity': the_sphericity,
                        'bond_size': the_bond_size,
                        'grain_size': the_grain_size,
                        'grain_type': the_grain_type,
                        'surface_grain_type': the_surface_grain_type,
                        'surface_grain_size': the_surface_grain_size,
                        'surface_density': the_surface_density,
                        'ice': the_ice,
                        'air': the_air,
                        'viscosity': the_viscosity,
                        'soil': the_soil,
                        'temperature_gradient': the_temperature_gradient,
                        'thermal_conductivity': the_thermal_conductivity,
                        'absorbed_shortwave_radiation': the_absorbed_shortwave_radiation,
                        'viscous_deformation_rate': the_viscous_deformation,
                        'ssi': the_ssi
                    })
                    the_dt = the_surface_grain_type = the_surface_grain_size = the_surface_density = -9999
                    the_height = the_density = the_temperature = the_water = the_dendricity = the_sphericity = the_bond_size = the_grain_size = the_grain_type = the_ice = the_air = the_viscosity = the_soil = the_temperature_gradient = the_thermal_conductivity = the_absorbed_shortwave_radiation = the_viscous_deformation = the_ssi = []
                the_dt = dt.datetime.strptime(row[1], '%d.%m.%Y %H:%M:%S')
            elif row[0] == '0501':  # ! height (cm)
                the_height = [float(s) for s in row[2:]]
            elif row[0] == '0502':  # ! density (kg m-3)
                the_density = [float(s) for s in row[2:]]
            elif row[0] == '0503':  # ! temperature (degC)
                the_temperature = [float(s) for s in row[2:]]
            elif row[0] == '0506':  # ! liquid water content by volume (%)
                the_water = [float(s) for s in row[2:]]
            elif row[0] == '0508':  # ! dendricity
                the_dendricity = [float(s) for s in row[2:]]
            elif row[0] == '0509':  # ! sphericity
                the_sphericity = [float(s) for s in row[2:]]
            elif row[0] == '0511':  # ! bond size (mm)
                the_bond_size = [float(s) for s in row[2:]]
            elif row[0] == '0512':  # ! grain size (mm)
                the_grain_size = [float(s) for s in row[2:]]
            elif row[0] == '0513':  # ! grain type (Swiss Code F1F2F3)
                the_grain_type = [float(s) for s in row[2:-1]]
            elif row[0] == '0514':  # ! at surface
                the_surface_grain_type = float(row[2])
                the_surface_grain_size = float(row[3])
                the_surface_density = float(row[4])
            elif row[0] == '0515':  # ! ice volume fraction (%)
                the_ice = [float(s) for s in row[2:]]
            elif row[0] == '0516':  # ! air volume fraction (%)
                the_air = [float(s) for s in row[2:]]
            elif row[0] == '0518':  # ! viscosity (GPa s)
                the_viscosity = [float(s) for s in row[2:]]
            elif row[0] == '0519':  # ! soil volume fraction (%)
                the_soil = [float(s) for s in row[2:]]
            elif row[0] == '0520':  # ! temperature gradient (K m-1)
                the_temperature_gradient = [float(s) for s in row[2:]]
            elif row[0] == '0521':  # ! thermal conductivity (W K-1 m-1)
                the_thermal_conductivity = [float(s) for s in row[2:]]
            elif row[0] == '0522':  # ! absorbed shortwave radiation (W m-2)
                the_absorbed_shortwave_radiation = [float(s) for s in row[2:]]
            elif row[0] == '0523':  # ! viscous deformation rate (1.e-6 s-1)
                the_viscous_deformation = [float(s) for s in row[2:]]
            elif row[0] == '0604':  # ! ssi
                the_ssi = [float(s) for s in row[2:]]
        #save the last data
        self.formatted_data.append({
            'datetime': the_dt,
            'height': the_height,
            'density': the_density,
            'temperature': the_temperature,
            'water': the_water,
            'dendricity': the_dendricity,
            'sphericity': the_sphericity,
            'bond_size': the_bond_size,
            'grain_size': the_grain_size,
            'grain_type': the_grain_type,
            'surface_grain_type': the_surface_grain_type,
            'surface_grain_size': the_surface_grain_size,
            'surface_density': the_surface_density,
            'ice': the_ice,
            'air': the_air,
            'viscosity': the_viscosity,
            'soil': the_soil,
            'temperature_gradient': the_temperature_gradient,
            'thermal_conductivity': the_thermal_conductivity,
            'absorbed_shortwave_radiation': the_absorbed_shortwave_radiation,
            'viscous_deformation_rate': the_viscous_deformation,
            'ssi': the_ssi
        })

    def figure(self, savefile=False, mode='grain_type', xlim=False, ylim=False):
        matplotlib.rc('font', family='Noto Sans CJK JP')
        fig = plt.figure(dpi=200, figsize=(10, 7.5), facecolor='w', edgecolor='k')
        ax = fig.add_subplot(111)

        plt.xticks(fontsize=16)
        fig.autofmt_xdate(rotation=45)
        plt.yticks(fontsize=16)
        ax.set_ylabel('snow depth [cm]', size=16)
        if not xlim == False:
            ax.set_xlim(*xlim)
        if not ylim == False:
            ax.set_ylim(*ylim)
        
        for row in self.formatted_data:
            the_dt = row['datetime']
            bef_h = 0
            for h, g in zip(row['height'], row['grain_type']):
                bars = ax.bar(the_dt, h-bef_h, bottom=bef_h, width=0.04,
                    align="center")
                color = 'lightgray'
                grain_type = self.grain_table[str(g)[:1]]
                color = self.color_table[grain_type]
                for bar_item in bars:
                    bar_item.set_color(color)
                    # bar_item.set_edgecolor('black')
                bef_h = h
        g1 = plt.bar([0], [0], width=0, align='center', label='PP', color=self.color_table['PP'])
        g2 = plt.bar([0], [0], width=0, align='center', label='DF', color=self.color_table['DF'])
        g3 = plt.bar([0], [0], width=0, align='center', label='RG', color=self.color_table['RG'])
        g4 = plt.bar([0], [0], width=0, align='center', label='FC', color=self.color_table['FC'])
        g5 = plt.bar([0], [0], width=0, align='center', label='DH', color=self.color_table['DH'])
        g6 = plt.bar([0], [0], width=0, align='center', label='SH', color=self.color_table['SH'])
        g7 = plt.bar([0], [0], width=0, align='center', label='MF', color=self.color_table['MF'])
        g8 = plt.bar([0], [0], width=0, align='center', label='IF', color=self.color_table['IF'])
        ax.legend(handles=[g1, g2, g3, g4, g5, g6, g7, g8],
                loc='upper left', bbox_to_anchor=(1.02, 1), 
                borderaxespad=0, frameon=False, fontsize=18)
        
        if not savefile == False:
            plt.savefig(savefile, bbox_inches='tight', pad_inches=0.05)
            print(f'the figure was saved as {savefile}.')
        plt.show()
# <<<<<<<<<< CREATE OBJECTS <<<<<<<<<<

# >>>>>>>>>> RUN >>>>>>>>>>
if __name__ == '__main__':
    inst = profile('data.pro')
    inst.figure('sample.png')
# <<<<<<<<<< RUN <<<<<<<<<<
# %%
