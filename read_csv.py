import pandas as pd

laed_filepath ='/Users/micah/build/firstlove/data/Lead.csv'
lead_data = pd.read_csv(laed_filepath, index_col='Id')