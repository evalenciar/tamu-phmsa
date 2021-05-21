# -*- coding: utf-8 -*-
"""
Data Collection and Mapping

The objective of this module is to call the datasets, map the variables to
maintain consistency, and curate the data for future analysis.
"""

import pandas as pd
import numpy as np
# =============================================================================
# DATA PREPARATION: IMPORT DATA
# =============================================================================

# Path to all data files
path = 'data'
# File names for each category
# files_gas_distribution = []

# files_gas_transmission = ['incident_gas_transmission_gathering_1970_mid1984.xlsx',
#                           'incident_gas_transmission_gathering_mid1984_2001.xlsx',
#                           'incident_gas_transmission_gathering_2002_dec2009.xlsx',
#                           'incident_gas_transmission_gathering_jan2010_present.xlsx',
#                           ]

# files_hazardous_liquid = []

# files_liquefied_natural = []

# files_mechanical_fit = []

# Variables for 2010 - Present
var_gt_3 = ['incident_gas_transmission_gathering_jan2010_present.xlsx',
            # Part A - Key Report Information
             'OPERATOR_ID',             # 0 - Operator ID
             'NAME',                    # 1 - Operator Name
             'LOCAL_DATETIME',          # 2 - Incident Date
             'COMMODITY_RELEASED_TYPE', # 3 - Gas released: Natural, Propane, Synthetic, Hydrogen, Landfill Gas
             'SYSTEM_PART_INVOLVED',    # 4 - Part of system involved in Incident (focus on 'Onshore Pipeline')
             'ONSHORE_POSTAL_CODE',     # 5 - If Onshore Only
             
             # Part C - Additional Facility Information
             'MATERIAL_INVOLVED',       # 6 - Material involved in Incident
             'ITEM_INVOLVED',           # 7 - Item involved in Incident: Pipe Body, Pipe Seam
             'PIPE_DIAMETER',           # 8 - Pipe Diameter (in)
             
             # If MATERIAL_INVOLVED is Carbon Steel
             'PIPE_WALL_THICKNESS',     # 9 - Wall thickness (in)
             'PIPE_SMYS',               # 10 - SMYS (Specified Minimum Yield Strength) of pipe (psi)
             'PIPE_SPECIFICATION',      # 11 - Pipe specification
             'PIPE_SEAM_TYPE',          # 12 - Long. ERW - HF, Long. ERW - LF, Long. ERW - Unknown F, etc.
             'PIPE_MANUFACTURER',       # 13 - Pipe manufacturer, OR Unknown
             'PIPE_COATING_TYPE',       # 14 - Pipeline coating type at point of Incident: Epoxy, Coal Tar, Asphalt, etc.
             
             # If MATERIAL_INVOLVED is Plastic
             'PLASTIC_TYPE',            # 15 - Plastic type: PVC, PE, PEX, PB, PP, ABS, PA, CAB, Unknown
             'PLASTIC_SDR',             # 16 - Standard Dimension Ratio (SDR)
             'WT_PLASTIC',              # 17 - Wall thickness (in)
             
             'INSTALLATION_YEAR',       # 18 - Installation Year
             'MANUFACTURED_YEAR',       # 19 - Manufactured Year
             
             # Part G -  Apparent Cause
             'CAUSE',                   # 20 - Apparent Cause
             'CAUSE_DETAILS',           # 21 - Apparent Cause with details
             ]

# Dataframe with variable mapping
df_index = ['File Name',
            # Operator Information
            'Operator ID',
            'Operator Name',
            'Incident Date',
            'Gas Released',
            'System Part',
            'Postal Code',
            # Pipe Information
            'Material',
            'Pipe Failure',
            'Pipe Diameter',
            # If Material is Carbon Steel
            'Pipe Wall Thickness',
            'Pipe SMYS',
            'Pipe Specification',
            'Pipe Seam Type',
            'Pipe Manufacturer',
            'Pipe Coating Type',
            # If Material is Plastic
            'Plastic Type',
            'Plastic SDR',
            'Plastic Wall Thickness',
            # General Information
            'Installation Year',
            'Manufactured Year',
            # Failure Case Information
            'Failure Cause',
            'Failure Cause Details',
            ]

df_cats = ['gas_distribution',
           'gas_transmission',
           'hazardous_liquid',
           'liquefied_natural',
           'mechanical_fit']

df_cols = [# Gas Transmission & Gathering Incident Data
           df_cats[1] + '_0',
           df_cats[1] + '_1',
           df_cats[1] + '_2',
           df_cats[1] + '_3']

df = pd.DataFrame(index=df_index)
df.insert(loc=0, column=df_cols[3], value=var_gt_3)

def data_incident(category = 'gas_transmission', year_bin = 3, failure_cause = 'corrosion', material = 'carbon_steel'):
    """
    Select the PHMSA dataset and year bin. Data curation will be performed
    according to the method selected. \n
    ---------- \n
    category : str \n
        gas_distribution,
        gas_transmission,
        hazardous_liquid,
        liquefied_natural,
        mechanical_fit
    year_bin : int
        0 ~ 1970-1984 \n
        1 ~ 1984-2001 \n
        2 ~ 2002-2009 \n
        3 ~ 2010-present
    failure_cause : str \n
        corrosion
    material : str \n
        carbon_steel \n
        plastic

    Returns
    -------
    None.

    """
    # Import the PHMSA dataset
    category_bin = category + '_' + str(year_bin)
    file_path = path + '\\' + df.loc['File Name', category_bin]
    data = pd.read_excel(file_path)
    
    # Begin curating the data
    if category == 'gas_transmission':
        if (failure_cause == 'corrosion' and material == 'carbon_steel'):
            # This will only focus on the following: 
            #   Apparent Cause      = Corrosion Failure
            #   Material Involved   = Carbon Steel
            
            # Drop all the data that is not MATERIAL_INVOLVED = CARBON STEEL
            flag1 = 'CARBON STEEL'
            flagged_data = data[data[df.loc['Material', category_bin]] != flag1].index
            data.drop(flagged_data, inplace=True)
            
            # Drop all the data that does not have an INSTALLATION_YEAR or MANUFACTURED_YEAR
            flag2 = np.nan
            flagged_data = data[data[df.loc['Installation Year', category_bin]] == flag2].index
            data.drop(flagged_data, inplace=True)
            flagged_data = data[data[df.loc['Manufactured Year', category_bin]] == flag2].index
            data.drop(flagged_data, inplace=True)
            
            # Convert the INSTALLATION_YEAR and MANUFACTURED_YEAR data into datetime64[ns]
            data[df.loc['Installation Year', category_bin]] = \
                pd.to_datetime(data[df.loc['Installation Year', category_bin]], format='%Y', errors='coerce')
            data[df.loc['Manufactured Year', category_bin]] = \
                pd.to_datetime(data[df.loc['Manufactured Year', category_bin]], format='%Y', errors='coerce')
            
            # Insert new column with LIFETIME data
            life_install = data[df.loc['Incident Date', category_bin]] - \
                data[df.loc['Installation Year', category_bin]]
            data.insert(0, 'LIFE_INSTALLED', (life_install.astype('timedelta64[D]')/365.25), allow_duplicates=True)
            life_manufac = data[df.loc['Incident Date', category_bin]] - \
                data[df.loc['Manufactured Year', category_bin]]
            data.insert(0, 'LIFE_MANUFACTURED', (life_manufac.astype('timedelta64[D]')/365.25), allow_duplicates=True)
            
            # Drop all the data that is not CAUSE = CORROSION FAILURE
            flag3 = 'CORROSION FAILURE'
            flagged_data = data[data[df.loc['Failure Cause', category_bin]] != flag3].index
            data.drop(flagged_data, inplace=True)
            
            # Separate the data into External Corrosion and Internal Corrosion
            flag_IC = 'INTERNAL CORROSION'
            flag_EC = 'EXTERNAL CORROSION'
            data_IC = data[data[df.loc['Failure Cause Details', category_bin]] == flag_IC]
            data_EC = data[data[df.loc['Failure Cause Details', category_bin]] == flag_EC]
            
            return df, data, data_IC, data_EC
    else:
        return df, data

# =============================================================================
# DATA PREPARATION: CURATE DATA
# =============================================================================

