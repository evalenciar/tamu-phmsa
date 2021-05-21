# -*- coding: utf-8 -*-
"""
# =============================================================================
# PHMSA Database
# =============================================================================

Created by Emmanuel Valencia
04/26/2021
"""
import pandas as pd
import numpy as np
import data_map
import data_plot

# Import ALL the data from the PHMSA dataset
df, data, data_IC, data_EC = data_map.data_incident(category='gas_transmission', 
                                          year_bin=3,
                                          failure_cause='corrosion',
                                          material='carbon_steel')
# Import ALL the data from the PHMSA annual reports



# =============================================================================
# Perform the ML / statistical prediction
# =============================================================================


# =============================================================================
# Plot the results
# =============================================================================

# Histogram
data_plot.hist(data, df)
# Scatter Matrix
data_plot.scatter_matrix(data, df)
# Overlayed Scatter

# t-SNE

# What other methods exist for multi-dimensional plotting?