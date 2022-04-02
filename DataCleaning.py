# Data cleaning Essentia
# Author: Destiny Ziebol
# Project: Analysis of Hospital Pricing Data
# Group # 11
# CSCI 5707

import pandas as pd

# Change print setting:
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# List of Providers:
providers = ['Humana', 'South Country Health Alliance', 'Ucare', 'Medica', 'Security Health Plan', 'Blue Cross',
             'Veterans Administration', 'Americas PPO', 'DakotaCare', 'HealthPartners', 'Hennepin Health',
             'Preferred One', 'United Health Care', 'United Behavioral Health', 'URN Oncology', 'First Health',
             'HealthEOS/WPPN', 'Health Tradition', 'Med Cost Solutions'
    , 'Sanford', 'WEA', 'Security Health', 'Group Health', 'WPS', 'South Country Health', 'Bind', 'AETNA', 'Optum',
             'Primewest', 'Imcare']

# providers = [x.lower() for x in providers]

def ProviderSplit(dfcol, providers):
    "Takes in a pandas df of two columns, the second of which is populated, then splits that column to fill both columns based on the items in the list"
    s = dfcol.shape
    # print("Start Provider SPlit")
    # print("shape: ", s)
    if s[1] != 2:
        return print("Incorrect column size!")
    for i in range(s[0]):  # rows
        # print("Product: ", dfcol.iloc[i,1])
        for j in range(len(providers)):
            # apparently we need to do this bs
            if providers[j].lower() in dfcol.iloc[i, 1].lower():
                # print("Match Found: ", providers[j], dfcol.iloc[i,1])
                end = dfcol.iloc[i, 1].lower().index(providers[j].lower()) + len(providers[j])
                dfcol.iloc[i, 0] = providers[j]
                dfcol.iloc[i, 1] = dfcol.iloc[i, 1][end:].lstrip('- ')
    return (dfcol)

# First table, Ada:
# Selecting header also excludes lines above selection
ada = pd.read_csv('ada-hospital-service-charges.csv', header=2054)
print(ada.columns)
print(ada.iloc[:, 0:3].head())

# Remove blank columns from end
ada1 = ada.drop(ada.columns[-8:], axis=1)
ada1 = ada1.drop(ada1.columns[3], axis=1)
print("delete columns")
print(ada1.columns)
print(ada1.head())
print(ada1.shape)

# Select only MS-DRG codes
ada2 = ada1[ada1['DRG Type'] == 'MS-DRG']
print(ada2.head())
print(ada2.shape)
# Add location column
ada2.insert(0, 'Location', 'Essentia Ada')
print("Location insert")
print(ada2.head())
# transform table from wide to long using melt:
ada3 = ada2.melt(id_vars=['Location', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product",
                 value_name="Price")

print("melt: ")
print(ada3.head())
print(ada3.shape)
# print(ada3['Product'].unique())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
ada3['DRG Type'] = 'MS'
print(ada3.head())
ada3.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(ada3.head())

# Remove all rows with NaN in Charge:
ada3 = ada3[ada3["Charge"].notna()]
# Remove all rows with Multiplan in Product:
ada3 = ada3[~ada3["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
ada3 = ada3[ada3.Product != 'Median Charge']

# Find and replace non-consistent Products:
ada3['Product'] = ada3['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
ada3['Product'] = ada3['Product'].str.replace('UHC', 'United Health Care')

# Add leading zeros to drg_cd:
ada3[['drg_cd']] = ada3[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
ada3['Provider'] = ada3.insert(4, 'Provider', '')

print(ada3.head())
print(ada3.shape)

# Split providers and services:
ada3[['Provider', 'Product']] = ProviderSplit(ada3[['Provider', 'Product']], providers)

print(ada3.shape)
print(ada3)

# Save
ada3.to_csv('ada_cleaned.csv')

# Next up: Deer river!
df = pd.read_csv('deer-river-hospital-service-charges.csv', header=2155)
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
df = df.drop(df.columns[-4:], axis=1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Dear River')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistent Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('dr_cleaned.csv')

print("First concat: ")
print(ada3.shape)
print(df.shape)
dfc = pd.concat([ada3, df])
print(dfc.shape)

# Third! Detroit Lakes
df = pd.read_csv('detroit-lakes-hospital-service-charges.csv', header=3210)
print("import: ")
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
# df = df.drop(df.columns[-4:], axis = 1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Detroit Lakes')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistant Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('dl_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# Forth, Fosston
df = pd.read_csv('fosston-hospital-service-charges.csv', header=3047)
print("import: ")
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
df = df.drop(df.columns[-10:], axis=1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Fosston')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistent Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('foss_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# Fifth holy-trinity-graceville-hospital-service-charges.csv
df = pd.read_csv('holy-trinity-graceville-hospital-service-charges.csv', header=2393)
print("import: ")
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
# df = df.drop(df.columns[-10:], axis = 1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Fith, Holy-trinity-graceville
# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Graceville')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistent Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('HTGrace_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# 6 Duluth miller-dwan-hospital-service-charges
df = pd.read_csv('miller-dwan-hospital-service-charges.csv', header=5700)
print("import: ")
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
df = df.drop(df.columns[-8:], axis=1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Duluth Miller Dawn')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistent Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('dmd_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# 7 Moose-Lake-Hospital-Service-Charges
df = pd.read_csv('Moose-Lake-Hospital-Service-Charges.csv', header=1937)
print("import: ")
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
# df = df.drop(df.columns[-8:], axis = 1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Moose Lake')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistent Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('ml_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# 8 Northern Pines aurora
df = pd.read_csv('northern-pines-aurora-hospital-service-charges.csv', header=2500)
print("import: ")
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
df = df.drop(df.columns[-8:], axis=1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Northern Pines')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistant Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)
# Save
df.to_csv('np_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# 9 Sandstone
df = pd.read_csv('sandstone-hospital-service-charges.csv', header=2682)
print("import: ")
print(df.head())
# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
# df = df.drop(df.columns[-8:], axis = 1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Sandstone')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistent Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('snd_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# 10 Brainerd
df = pd.read_csv('st-josephs-medical-center-brainerd-hospital-service-charges.csv', header=4904)
print("import: ")
print(df.head())

# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
df = df.drop(df.columns[-1:], axis=1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Brainerd')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistant Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)
# Save
df.to_csv('brnd_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# 11 Duluth St Mary
df = pd.read_csv('st-marys-medical-center-hospital-duluth-service-charges.csv', header=8489)
print("import: ")
print(df.head())

# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
df = df.drop(df.columns[-4:], axis=1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Duluth St. Mary')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistant Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('dul_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

# 12 Virgina
df = pd.read_csv('virginia-hospital-service-charges.csv', header=3563)
print("import: ")
print(df.head())

# Get rid of empty columns:
df = df.drop(df.columns[3], axis=1)
df = df.drop(df.columns[-1:], axis=1)
print('Remove Cols:')
print(df.head())
print(df.shape)

# Select rows:
df = df[df['DRG Type'] == 'MS-DRG']
print("select rows: ")
print(df.shape)

# Add location column
df.insert(0, 'Hospital', 'Essentia Virginia')
print("Location insert")
print(df.head())

# transform table from wide to long using melt:
df = df.melt(id_vars=['Hospital', 'DRG Type', 'DRG Code', 'DRG Description'], var_name="Product", value_name="Charge")
print("melt: ")
print(df.head())

# Make column names standard to rest of group and ER Diagram:
print("Rename:")
df['DRG Type'] = 'MS'
print(df.head())
df.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'Product', 'Charge']
print(df.head())

# Strip
df['Product'] = df['Product'].str.strip()
# Remove all rows with NaN in Charge:
df = df[df["Charge"].notna()]
# Remove all rows with Multiplan in Product:
df = df[~df["Product"].str.contains('MULTIPLAN')]
# Remove all rows with "Median Charge" Product:
df = df[df.Product != 'Median Charge']

print("removal step, new shape: ", df.shape)

# Find and replace non-consistent Products:
df['Product'] = df['Product'].str.replace('AMERICA\'S PPO', 'Americas PPO')
df['Product'] = df['Product'].str.replace('UHC', 'United Health Care')
df['Product'] = df['Product'].str.replace('SOUTH COUNTRY HLTH', 'South Country Health')
df['Product'] = df['Product'].str.replace('UMR', 'United Health Care UMR')
df['Product'] = df['Product'].str.replace('BCBS MN STATE OF MN/', 'Blue Cross ')
df['Product'] = df['Product'].str.replace('BCBS MN', 'Blue Cross')
df['Product'] = df['Product'].str.replace('BCBS', 'Blue Cross')
df['Product'] = df['Product'].str.replace('De', 'Blue Cross')

# Add leading zeros to drg_cd:
df[['drg_cd']] = df[['drg_cd']].apply(lambda x: x.astype(str).str.zfill(3))

# Add a column for Providers:
df['Provider'] = df.insert(4, 'Provider', '')

print("find and replace, leading zeros and added provider: ")
print(df.head())
print(df.shape)

# Split providers and services:
df[['Provider', 'Product']] = ProviderSplit(df[['Provider', 'Product']], providers)
print("split provider and services: ")
print(df.shape)
print(df)

# Save
df.to_csv('vg_cleaned.csv')

print("Concat: ")
print(dfc.shape)
print(df.shape)
dfc = pd.concat([dfc, df])
print(dfc.shape)

dfc.columns = ['Hospital', 'Code_type', 'drg_cd', 'drg_desc', 'MCO', 'Product', 'Charge']

print(dfc[:100])

dfc.to_csv('Cleaned_Essentia.csv')
