from load_functions import *

fname_v1 = 'manage_datasets\cmp___smartcampus_ge120_placaEsp.json'
fname_v2 = 'manage_datasets\cmp___smartcampus_ge117_placaEsp.json'
fname_v1_temp = 'tempV1.csv'
fname_v2_temp = 'tempV2.csv'

dfv1 = pd.read_json(fname_v1, lines=True)
dfv1.to_csv(fname_v1_temp)
del dfv1

dfv2 = pd.read_json(fname_v2, lines=True)
dfv2.to_csv(fname_v2_temp)
del dfv2

df1_end = load_smartmetropolis_dataset(fname_v1_temp)
df1_end.to_csv('file1.csv')
del df1_end

df2_end = load_smartmetropolis_dataset(fname_v2_temp)
df2_end.to_csv('file2.csv')
del df2_end