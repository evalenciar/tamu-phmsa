# -*- coding: utf-8 -*-
"""
Annual Reports Collection and Mapping

The objective of this module is to call the annual reports, map the variables 
to maintain consistency, and curate the data for future analysis.

The Excel files have separate tabs for the sections. Some are in groups, others
are single per tab. The reports are NOT in the same order.

Will need to reorganize by report number.
"""

import pandas as pd
import numpy as np
# =============================================================================
# ANNUAL REPORTS PREPARATION: IMPORT DATA
# =============================================================================

# Path to all data files
file_dir = 'annual_reports'
file_cat = ['annual_gas_transmission_gathering',
              'annual_gas_distribution',
              'annual_hazardous_liquid',
              'annual_underground_natural_gas_storage',
              'annual_liquefied_natural_gas',
              ]
# Focus just on annual_gas_transmission_gathering
file_year = ['1970_2000',
             '2001_2009',
             '2010_present',
             ]
# Final file_folder in the correct folder dir
# For now, use the 'annual_gas_transmission_gathering_2010_present' folder
file_folder = file_dir + '\\' + file_cat[0] + '\\' + file_cat[0] + '_' + file_year[2]

# Variables for 2010 - Present
var_gt_3 = ['incident_gas_transmission_gathering_jan2010_present.xlsx',
            # Part A - Key Report Information
             'OPERATOR_ID',             # 0 - Operator's 5 Digit Identification Number (OPID)
             'PARTA2NAMEOFCOMP',        # 1 - Operator Name
             'REPORT_YEAR',             # 2 - Report Year
             'REPORT_NUMBER',           # 3 - Report Number
             'SUPPLEMENTAL_NUMBER',     # 4 - Supplemental Number
             'PARTA5COMMODITY',         # 5 - Gas released: Natural, Synthetic, Hydrogen, Propane, Landfill Gas
             
             # Part B - Transmission Pipeline HCA Miles
             'PARTBHCAONSHORE',         # 6 - Onshore Miles
             'PARTBHCAOFFSHORE',        # 7 - Offshore Miles
             'PARTBHCATOTAL',           # 8 - Total Miles
             
             # Part C - Volume Transported in Million SCF Per Year
             'PARTCONNG',               # 9 - Onshore: Natural Gas
             'PARTCONPG',               # 10 - Onshore: Propane Gas
             'PARTCONSG',               # 11 - Onshore: Synthetic Gas
             'PARTCONHG',               # 12 - Onshore: Hydrogen Gas
             'PARTCONLFG',              # 13 - Onshore: Landfill Gas
             'PARTCOFFNG',              # 14 - Offshore: Natural Gas
             'PARTCOFFPG',              # 15 - Offshore: Propane Gas
             'PARTCOFFSG',              # 16 - Offshore: Synthetic Gas
             'PARTCOFFHG',              # 17 - Offshore: Hydrogen Gas
             'PARTCOFFLFG',             # 18 - Offshore: Landfill Gas
             
             # Part D - Miles of Pipe by Material and Corrosion Prevention Status
             # Transmission - Onshore
             'PARTDTONCPB',             # 19 - Steel cathodically protected: Bare
             'PARTDTONCPC',             # 20 - Steel cathodically protected: Coated
             'PARTDTONCUB',             # 21 - Steel cathodically unprotected: Bare
             'PARTDTONCUC',             # 22 - Steel cathodically unprotected: Coated
             'PARTDTONCI',              # 23 - Cast Iron
             'PARTDTONWI',              # 24 - Wrought Iron
             'PARTDTONP',               # 25 - Plastic
             'PARTDTON',                # 26 - Composite <------ confirm this with Excel sheet -------------------!!!!!!!!!!!!!!
             'PARTDTONO',               # 27 - Other
             'PARTDTONTOTAL',           # 28 - Total Miles
             # Transmission - Offshore
             'PARTDTOFFCPB',            # 29 - Steel cathodically protected: Bare
             'PARTDTOFFCPC',            # 30 - Steel cathodically protected: Coated
             'PARTDTOFFCUB',            # 31 - Steel cathodically unprotected: Bare
             'PARTDTOFFCUC',            # 32 - Steel cathodically unprotected: Coated
             'PARTDTOFFCI',             # 33 - Cast Iron
             'PARTDTOFFWI',             # 34 - Wrought Iron
             'PARTDTOFFP',              # 35 - Plastic
             'PARTDTOFFC',              # 36 - Composite
             'PARTDTOFFO',              # 37 - Other
             'PARTDTOFFTOTAL',          # 38 - Total Miles
             # Transmission - Subtotal
             'PARTDTCPBTOTAL',          # 39 - Steel cathodically protected: Bare
             'PARTDTCPCTOTAL',          # 40 - Steel cathodically protected: Coated
             'PARTDTCUBTOTAL',          # 41 - Steel cathodically unprotected: Bare
             'PARTDTCUCTOTAL',          # 42 - Steel cathodically unprotected: Coated
             'PARTDTCITOTAL',           # 43 - Cast Iron
             'PARTDTWITOTAL',           # 44 - Wrought Iron
             'PARTDTPTOTAL',            # 45 - Plastic
             'PARTDTCTOTAL',            # 46 - Composite
             'PARTDTOTOTAL',            # 47 - Other
             'PARTDTTOTAL',             # 48 - Total Miles
             
             # Gathering - Onshore Type A
             'PARTDGONTACPB',           # 49 - Steel cathodically protected: Bare
             'PARTDGONTACPC',           # 50 - Steel cathodically protected: Coated
             'PARTDGONTACUB',           # 51 - Steel cathodically unprotected: Bare
             'PARTDGONTACUC',           # 52 - Steel cathodically unprotected: Coated
             'PARTDGONTACI',            # 53 - Cast Iron
             'PARTDGONTAWI',            # 54 - Wrought Iron
             'PARTDGONTAP',             # 55 - Plastic
             'PARTDGONTAC',             # 56 - Composite
             'PARTDGONTAO',             # 57 - Other
             'PARTDGONATOTAL',          # 58 - Total Miles
             # Gathering - Onshore Type B
             'PARTDGONTBCPB',           # 59 - Steel cathodically protected: Bare
             'PARTDGONTBCPC',           # 60 - Steel cathodically protected: Coated
             'PARTDGONTBCUB',           # 61 - Steel cathodically unprotected: Bare
             'PARTDGONTBCUC',           # 62 - Steel cathodically unprotected: Coated
             'PARTDGONTBCI',            # 63 - Cast Iron
             'PARTDGONTBWI',            # 64 - Wrought Iron
             'PARTDGONTBP',             # 65 - Plastic
             'PARTDGONTBC',             # 66 - Composite
             'PARTDGONTBO',             # 67 - Other
             'PARTDGONBTOTAL',          # 68 - Total Miles
             # Gathering - Offshore
             'PARTDGOFFCPB',            # 69 - Steel cathodically protected: Bare
             'PARTDGOFFCPC',            # 70 - Steel cathodically protected: Coated
             'PARTDGOFFCUB',            # 71 - Steel cathodically unprotected: Bare
             'PARTDGOFFCUC',            # 72 - Steel cathodically unprotected: Coated
             'PARTDGOFFCI',             # 73 - Cast Iron
             'PARTDGOFFWI',             # 74 - Wrought Iron
             'PARTDGOFFP',              # 75 - Plastic
             'PARTDGOFFC',              # 76 - Composite
             'PARTDGOFFO',              # 77 - Other
             'PARTDGOFFTOTAL',          # 78 - Total Miles
             # Gathering - Subtotal
             'PARTDGCPBTOTAL',          # 79 - Steel cathodically protected: Bare
             'PARTDGCPCTOTAL',          # 80 - Steel cathodically protected: Coated
             'PARTDGCUBTOTAL',          # 81 - Steel cathodically unprotected: Bare
             'PARTDGCUCTOTAL',          # 82 - Steel cathodically unprotected: Coated
             'PARTDGCITOTAL',           # 83 - Cast Iron
             'PARTDGWITOTAL',           # 84 - Wrought Iron
             'PARTDGPTOTAL',            # 85 - Plastic
             'PARTDGCTOTAL',            # 86 - Composite
             'PARTDGOTOTAL',            # 87 - Other
             'PARTDGTOTAL',             # 88 - Total Miles
             
             # Total Miles
             'PARTDCPBTOTAL',          # 89 - Steel cathodically protected: Bare
             'PARTDCPCTOTAL',          # 90 - Steel cathodically protected: Coated
             'PARTDCUBTOTAL',          # 91 - Steel cathodically unprotected: Bare
             'PARTDCUCTOTAL',          # 92 - Steel cathodically unprotected: Coated
             'PARTDCITOTAL',           # 93 - Cast Iron
             'PARTDWITOTAL',           # 94 - Wrought Iron
             'PARTDPTOTAL',            # 95 - Plastic
             'PARTDCTOTAL',            # 96 - Composite
             'PARTDOTOTAL',            # 97 - Other
             'PARTDTOTAL',             # 98 - Total Miles
             
             # Part H - Miles of Transmission Pipe by Nominal Pipe Size (NPS)
             # Onshore
             'PARTHON4LESS',
             'PARTHON6',
             'PARTHON8',
             'PARTHON10',
             'PARTHON12',
             'PARTHON14',
             'PARTHON16',
             'PARTHON18',
             'PARTHON20',
             'PARTHON22',
             'PARTHON24',
             'PARTHON26',
             'PARTHON28',
             'PARTHON30',
             'PARTHON32',
             'PARTHON34',
             'PARTHON36',
             'PARTHON38',
             'PARTHON42',
             'PARTHON44',
             'PARTHON46',
             'PARTHON48',
             'PARTHON52',
             'PARTHON56',
             'PARTHON58OVER',
             'PARTHON_OTHER_PIPE_DETAIL',
             'PARTHON_OTHER_PIPE_MILE_TOTAL',
             'PARTHONTOTAL',
             # Offshore
             'PARTHOFF4LESS',
             'PARTHOFF6',
             'PARTHOFF8',
             'PARTHOFF10',
             'PARTHOFF12',
             'PARTHOFF14',
             'PARTHOFF16',
             'PARTHOFF18',
             'PARTHOFF20',
             'PARTHOFF22',
             'PARTHOFF24',
             'PARTHOFF26',
             'PARTHOFF28',
             'PARTHOFF30',
             'PARTHOFF32',
             'PARTHOFF34',
             'PARTHOFF36',
             'PARTHOFF38',
             'PARTHOFF42',
             'PARTHOFF44',
             'PARTHOFF46',
             'PARTHOFF48',
             'PARTHOFF52',
             'PARTHOFF56',
             'PARTHOFF58OVER',
             'PARTHOFF_OTHER_PIPE_DETAIL',
             'PARTHOFF_OTHER_PIPE_MILE_TOTAL',
             'PARTHOFFTOTAL',
             
             # Part I - Miles of Gathering Pipe by Nominal Pipe Size (NPS)
             # Onshore Type A
             'PARTIONA4LESS',
             'PARTIONA6',
             'PARTIONA8',
             'PARTIONA10',
             'PARTIONA12',
             'PARTIONA14',
             'PARTIONA16',
             'PARTIONA18',
             'PARTIONA20',
             'PARTIONA22',
             'PARTIONA24',
             'PARTIONA26',
             'PARTIONA28',
             'PARTIONA30',
             'PARTIONA32',
             'PARTIONA34',
             'PARTIONA36',
             'PARTIONA38',
             'PARTIONA42',
             'PARTIONA44',
             'PARTIONA46',
             'PARTIONA48',
             'PARTIONA52',
             'PARTIONA56',
             'PARTIONA58OVER',
             'PARTIONA_OTHER_PIPE_DETAIL',
             'PARTIONA_OTHER_PIPE_MILE_TOTAL',
             'PARTIONATOTAL',
             # Onshore Type B
             'PARTIONB4LESS',
             'PARTIONB6',
             'PARTIONB8',
             'PARTIONB10',
             'PARTIONB12',
             'PARTIONB14',
             'PARTIONB16',
             'PARTIONB18',
             'PARTIONB20',
             'PARTIONB22',
             'PARTIONB24',
             'PARTIONB26',
             'PARTIONB28',
             'PARTIONB30',
             'PARTIONB32',
             'PARTIONB34',
             'PARTIONB36',
             'PARTIONB38',
             'PARTIONB42',
             'PARTIONB44',
             'PARTIONB46',
             'PARTIONB48',
             'PARTIONB52',
             'PARTIONB56',
             'PARTIONB58OVER',
             'PARTIONB_OTHER_PIPE_DETAIL',
             'PARTIONB_OTHER_PIPE_MILE_TOTAL',
             'PARTIONBTOTAL',
             # Offshore
             'PARTIOFF4LESS',
             'PARTIOFF6',
             'PARTIOFF8',
             'PARTIOFF10',
             'PARTIOFF12',
             'PARTIOFF14',
             'PARTIOFF16',
             'PARTIOFF18',
             'PARTIOFF20',
             'PARTIOFF22',
             'PARTIOFF24',
             'PARTIOFF26',
             'PARTIOFF28',
             'PARTIOFF30',
             'PARTIOFF32',
             'PARTIOFF34',
             'PARTIOFF36',
             'PARTIOFF38',
             'PARTIOFF42',
             'PARTIOFF44',
             'PARTIOFF46',
             'PARTIOFF48',
             'PARTIOFF52',
             'PARTIOFF56',
             'PARTIOFF58OVER',
             'PARTIOFF_OTHER_PIPE_DETAIL',
             'PARTIOFF_OTHER_PIPE_MILE_TOTAL',
             'PARTIOFFTOTAL',
             
             # Part J - Miles of Pipe by Decade Installed
             # Transmission - Onshore
             'PARTJTONUNKWN',
             'PARTJTONPRE1940',
             'PARTJTON194049',
             'PARTJTON195059',
             'PARTJTON196069',
             'PARTJTON197079',
             'PARTJTON198089',
             'PARTJTON199099',
             'PARTJTON200009',
             'PARTJTON201019',
             'PARTJTON202029',
             'PARTJTONTOTAL',
             # Transmission - Offshore
             'PARTJTOFFUNKWN',
             'PARTJTOFFPRE1940',
             'PARTJTOFF194049',
             'PARTJTOFF195059',
             'PARTJTOFF196069',
             'PARTJTOFF197079',
             'PARTJTOFF198089',
             'PARTJTOFF199099',
             'PARTJTOFF200009',
             'PARTJTOFF201019',
             'PARTJTOFF202029',
             'PARTJTOFFTOTAL',
             # Transmission - Subtotal
             'PARTJTUNKWNTOT',
             'PARTJTPRE1940TOT',
             'PARTJT194049TOT',
             'PARTJT195059TOT',
             'PARTJT196069TOT',
             'PARTJT197079TOT',
             'PARTJT198089TOT',
             'PARTJT199099TOT',
             'PARTJT200009TOT',
             'PARTJT201019TOT',
             'PARTJT202029TOT',
             'PARTJTTOTAL',
             
             # Gathering - Onshore Type A
             # Gathering - Onshore Type B
             # Gathering - Offshore
             
             # Park K - Miles of Transmission Pipe by Specified Minimum Yield Strength (SMYS)
             
             # Part M - Failures, Leaks, and Repairs
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

def data_report(category = 'gas_transmission', 
                year_bin = 2, 
                operator_id = 4906,
                ):
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
        0 ~ 1970-2000 \n
        1 ~ 2001-2009 \n
        2 ~ 2010-present
    operator_id : int
        Use the operator's 5 digit identification number (OPID).\n
        For example: 4906 for ExxonMobil Pipeline Co

    Returns
    -------
    None.

    """



    # Import the PHMSA report
    # This is only for the GT 2010-present
    file_path = file_folder + '\\' + var_gt_3[0]
    data_xlsx = pd.ExcelFile(file_path)
    data_A_D = pd.read_excel(data_xlsx, 0) # GT AR Part A to D
    data_F_G = pd.read_excel(data_xlsx, 1) # GT AR Part F to G
    # Parts H, I, J, K, L, M, P, Q, and R may have repeated entries
    # data_H   = pd.read_excel(data_xlsx, 0) # GT AR Part H
    # data_I   = pd.read_excel(data_xlsx, 0) # GT AR Part I
    # data_J   = pd.read_excel(data_xlsx, 0) # GT AR Part J
    # When necessary, add the remaining data