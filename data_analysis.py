import pandas as pd

def load_yokogawa_dataset(filename_yokogawa):
  df = pd.read_csv(filename_yokogawa,      # filename read in previous cell
                  delimiter=';',           # semicolon(;)/coma(,) separated values
                  decimal=",",             # set decimal point to '.' instead of ','
                  encoding='utf-8',        # encoding in utf-8
                  skiprows=37,              # skip default rows with Yokogawa configuration header
                  na_values=['----', '-----:--:--'],      # assign NaN to mixed types values
                  dayfirst=True,           # standardize  date format
                  parse_dates=['DateTime'] # parse DateTime column as Timestamp object
                  )

  # Filtering necessary variables
  df = df.filter(['DateTime', 'AVG_V1[V][V]', 'AVG_V2[V][V]', 'AVG_V3[V][V]', 
                  'AVG_A1[A][A]', 'AVG_A2[A][A]', 'AVG_A3[A][A]', 
                  'AVG_P[W][W]', 'AVG_S[VA][VA]', 'AVG_Q[var][var]',
                  'AVG_Vthd1[%][%]', 'AVG_Vthd2[%][%]', 'AVG_Vthd3[%][%]', 
                  'AVG_Athd1[%][%]', 'AVG_Athd2[%][%]', 'AVG_Athd3[%][%]', 
                  'AVG_PF[]', 'AVG_f[Hz][Hz]',
                  'AVG_V1[deg][deg]', 'AVG_V2[deg][deg]', 'AVG_V3[deg][deg]', 
                  'WP+[Wh][Wh]', 'WQi+[varh][varh]', 'WS+[VAh][VAh]'])

  df['AVG_V1[V][V]'] = df['AVG_V1[V][V]']#*np.sqrt(3) # adjust line voltage
  df['AVG_V2[V][V]'] = df['AVG_V2[V][V]']#*np.sqrt(3) # adjust line voltage
  df['AVG_V3[V][V]'] = df['AVG_V3[V][V]']#*np.sqrt(3) # adjust line voltage
  df = df.rename(columns={'DateTime': 'Timestamp'})   # rename column 'TimeInstant' to 'Timestamp' allowing to merge
  df = df.reset_index(drop=True)                      # reset indexes after cleaning

  return df

def load_smartmetropolis_dataset(filename_smartmetropolis, label):
  df = pd.read_csv(filename_smartmetropolis,           # filename read in previous cell
                  delimiter=',',              # semicolon(;)/coma(,) separated values
                  encoding='utf-8',           # encoding in utf-8
                  na_values=['inf'],          # assign NaN to inf values
                  parse_dates=['TimeInstant'] # parse TimeInstant column as Timestamp object
                  )

  # Filtering necessary variables
  old_columns = ['TimeInstant', 'voltA', 'voltB', 'voltC',
                    'correnteA', 'correnteB', 'correnteC', 
                    'potenciaAtiva', 'potenciaAparente', 'potenciaReativa',
                    'voltTHDA', 'voltTHDB', 'voltTHDC', 
                    'correnteTHDA', 'correnteTHDB', 'correnteTHDC', 
                    'fatorDePotencia', 'frequencia', 
                    'anguloVoltAB', 'anguloVoltAC', 'anguloVoltBC', 
                    'energiaAtiva', 'energiaReativa', 'energiaAparente']
  df = df.filter(old_columns)
  

  df.dropna(subset = ['frequencia'], inplace=True)        # drop rows with NaN values
  df = df[df['voltA'] != float(0.0)]                    # remove rows with 0's only
  df = df.rename(columns={'TimeInstant': 'Timestamp'})   # rename column 'TimeInstant' to 'Timestamp' allowing to merge
  df['Timestamp'] = df['Timestamp'].dt.tz_localize(None) # remove time zone from SmartMetropolis timestamps
  df['Timestamp'] -= pd.to_timedelta(3, unit='h')         # delay timestamps for 3h to correct dashboard desynchronization
  df['Timestamp'] += pd.to_timedelta(1, unit='min') 
  df['Timestamp'] += pd.to_timedelta(20, unit='sec') 
  df['Timestamp'] += pd.to_timedelta(6, unit='min') 
  df['Timestamp'] += pd.to_timedelta(20, unit='sec') 
  df = df.reset_index(drop=True)                         # reset indexes after cleaning

  new_columns = ['Timestamp']
  for i in range(len(old_columns)-1): new_columns.append(old_columns[i+1]+label)
  df.columns = new_columns

  return df

def merge_dataframes(df1, df2):

  # Merging dataframes based on similar timestamps with 10s tolerance
  df = pd.merge_asof(df1.sort_values('Timestamp'), 
                    df2.sort_values('Timestamp'), 
                    on='Timestamp', 
                    tolerance=pd.Timedelta("20s"), 
                    allow_exact_matches=False, direction='nearest')
  df.dropna(subset = [list(df1)[1], list(df2)[2]], inplace=True, how='any') # drop rows with NaN values

  return df