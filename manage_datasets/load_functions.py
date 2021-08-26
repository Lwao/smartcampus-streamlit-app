import numpy as np
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
  # Filter necessary columns
  df = df.filter(['DateTime', 'AVG_V1[V][V]', 'AVG_V2[V][V]', 'AVG_V3[V][V]', 
                'AVG_A1[A][A]', 'AVG_A2[A][A]', 'AVG_A3[A][A]', 
                'AVG_P[W][W]', 
                'AVG_Q[var][var]','AVG_Q1[var][var]','AVG_Q2[var][var]','AVG_Q3[var][var]',
                'AVG_S[VA][VA]','AVG_S1[VA][VA]','AVG_S2[VA][VA]','AVG_S3[VA][VA]',
                'AVG_PF[]','AVG_PF1[]','AVG_PF2[]','AVG_PF3[]',
                'AVG_f[Hz][Hz]','MAX_f[Hz][Hz]','MIN_f[Hz][Hz]',
                'WP+[Wh][Wh]','WP+1[Wh][Wh]','WP+2[Wh][Wh]','WP+3[Wh][Wh]',
                'WP-[Wh][Wh]','WP-1[Wh][Wh]','WP-2[Wh][Wh]','WP-3[Wh][Wh]',
                'WQi+[varh][varh]','WQi+1[varh][varh]','WQi+2[varh][varh]','WQi+3[varh][varh]',
                'WQc+[varh][varh]','WQc+1[varh][varh]','WQc+2[varh][varh]','WQc+3[varh][varh]',
                'WQi-[varh][varh]','WQi-1[varh][varh]','WQi-2[varh][varh]','WQi-3[varh][varh]',
                'WQc-[varh][varh]','WQc-1[varh][varh]','WQc-2[varh][varh]','WQc-3[varh][varh]',
                'WS+[VAh][VAh]','WS+1[VAh][VAh]','WS+2[VAh][VAh]','WS+3[VAh][VAh]',
                'WS-[VAh][VAh]','WS-1[VAh][VAh]','WS-2[VAh][VAh]','WS-3[VAh][VAh]',
                'AVG_Vthd1[%][%]', 'AVG_Vthd2[%][%]', 'AVG_Vthd3[%][%]', 
                'AVG_Athd1[%][%]', 'AVG_Athd2[%][%]', 'AVG_Athd3[%][%]', 
                'AVG_V1[deg][deg]', 'AVG_V2[deg][deg]', 'AVG_V3[deg][deg]'])
  
  #df = df.dropna(axis=1, how='all') # drop columns with all NaN
  #df = df.loc[:, (df != 0).any(axis=0)] # drop columns with all 0's
  df = df.rename(columns={'DateTime': 'Timestamp'})   # rename column 'TimeInstant' to 'Timestamp' allowing to merge
  df = df.reset_index(drop=True)                      # reset indexes after cleaning
  
  return df

def load_smartmetropolis_dataset(filename_smartmetropolis):
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
  df = df.reset_index(drop=True)                         # reset indexes after cleaning
  return df