from load_functions import *

fname_bigger = 'manage_datasets\YOKO_NPITI.csv'
fname_minor = 'manage_datasets\YOKO_NPITI_04082021-23082021_TESTE.csv'

df_bigger = pd.read_csv(fname_bigger)
df_minor = load_yokogawa_dataset(fname_minor)

df_list = []
df_list.append(df_bigger)
df_list.append(df_minor)
df_end = pd.concat(df_list, axis=0)
df_end.to_csv('file.csv')