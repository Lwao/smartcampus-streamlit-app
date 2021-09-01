from imports import *
from data_analysis import *
from text_description import *



@st.cache
def get_data_yoko(fname):
    df = load_yokogawa_dataset(fname)
    return df

@st.cache
def get_data_smartmetropolis(fname, id):
    df = load_smartmetropolis_dataset(fname, label=id)
    return df

def app(state):

    header = st.beta_container()
    dataset = st.beta_container()
    load = st.beta_container()

    


    with header:
        st.image('logo.png')
        st.title(header_title())
        st.markdown(header_markdown())

    with dataset:
        st.header(dataset_title())
        st.markdown(dataset_markdown())

    dataset_options = ['CW500', 'Smartcampus 1.0', 'Smartcampus 2.0']

    with load:
        st.header(load_title())
        st.markdown(load_markdown())

        
        #default_yoko = 'https://drive.google.com/file/d/1EFRE6md8BYFfOYOcueZbKc_k47eK7R93/view?usp=sharing' # dataset completo
        #default_yoko = 'https://drive.google.com/file/d/1eBi9kUSRWjGubCzI77TfSEHOi4rxOmCf/view?usp=sharing' # dataset cortado
        #default_comade = 'https://drive.google.com/file/d/1xHjrBebEb02rGRkXOfGc64wJicHpNQcr/view?usp=sharing'
        #default_semade = 'https://drive.google.com/file/d/1tLZBHQqe5rbCW4ijbX_ghi74k-_7Ds-X/view?usp=sharing'     
        default_yoko = '' # dataset cortado
        default_comade = ''
        default_semade = ''

        st.markdown('Insira os links públicos para os datasets de interesse.')

        default_yoko = st.text_input('Link para o dataset do CW500:', value=default_yoko)
        default_comade = st.text_input('Link para o dataset do Smartcampus 1.0:', value=default_comade)
        default_semade = st.text_input('Link para o dataset do Smartcampus 2.0:', value=default_semade)
    
        fname_yoko = 'https://drive.google.com/uc?export=download&id='+default_yoko.split('/')[-2]
        fname_comade = 'https://drive.google.com/uc?export=download&id='+default_comade.split('/')[-2]
        fname_semade = 'https://drive.google.com/uc?export=download&id='+default_semade.split('/')[-2]

        which_datasets = st.multiselect('Escolha os datasets a serem analisados:', dataset_options, dataset_options)


        df_lengths = dict()
        df = pd.DataFrame()
        flags = dict({'df_yoko':False, 'df_comade':False, 'df_semade':False})

        calendar1, calendar2, calendar3 = st.beta_columns(3)

        # load chosen dataframes
        for itr in which_datasets:
            if(itr=='CW500'): 
                df_yoko = get_data_yoko(fname_yoko)
                df_lengths['df_yoko'] = len(df_yoko)
                flags['df_yoko'] = True
                start_date = df_yoko['Timestamp'].iloc[0]  
                end_date = df_yoko['Timestamp'].iloc[-1] 
                calendar1.date_input("Duração dos dados: CW500", [start_date, end_date],
                min_value=start_date, max_value=end_date)
            if(itr=='Smartcampus 1.0'): 
                df_comade = get_data_smartmetropolis(fname_comade, '_comade')
                df_lengths['df_comade'] = len(df_comade)
                flags['df_comade'] = True
                start_date = df_comade['Timestamp'].iloc[0]  
                end_date = df_comade['Timestamp'].iloc[-1] 
                calendar2.date_input("Duração dos dados: Smartcampus 1.0", [start_date, end_date],
                min_value=start_date, max_value=end_date)
            if(itr=='Smartcampus 2.0'): 
                df_semade = get_data_smartmetropolis(fname_semade, '_semade')
                df_lengths['df_semade'] = len(df_semade)
                flags['df_semade'] = True
                start_date = df_semade['Timestamp'].iloc[0]  
                end_date = df_semade['Timestamp'].iloc[-1] 
                calendar3.date_input("Duração dos dados: Smartcampus 2.0", [start_date, end_date],
                min_value=start_date, max_value=end_date)

        # sort dataframes by size
        df_sorted = sorted(df_lengths, key=df_lengths.get)

        # inner merge based in Timestamp where left=smaller and right=higher
        for itr in range(len(df_sorted)):
            if(itr==0): df = eval(df_sorted[itr])
            else: df = merge_dataframes(df, eval(df_sorted[itr]))

        st.markdown(load_markdown1())

        calendar_col1, calendar_col2, result_calendar = st.beta_columns(3)

        start_date = calendar_col1.date_input('Data inicial:', value=df['Timestamp'].iloc[0], min_value=df['Timestamp'].iloc[0], max_value=df['Timestamp'].iloc[-1])
        end_date = calendar_col2.date_input('Data final:', value=df['Timestamp'].iloc[-1], min_value=df['Timestamp'].iloc[0], max_value=df['Timestamp'].iloc[-1])
        if(start_date<df['Timestamp'].iloc[0]): result_calendar.error('Erro: Data inicial precisa estar contida no período que há dados disponíveis.')
        elif(end_date>df['Timestamp'].iloc[-1]): result_calendar.error('Erro: Data final precisa estar contida no período que há dados disponíveis.')
        elif(start_date >= end_date): result_calendar.error('Erro: Data final deve estar à frente da data inicial.')
        else: result_calendar.success('Data inicial: `%s`\n\nData final: `%s`' % (start_date, end_date))

        idx_ini = df['Timestamp'][df['Timestamp']>=pd.to_datetime(start_date)].iloc[0:1].index[0]
        idx_end = df['Timestamp'][df['Timestamp']>=pd.to_datetime(end_date)].iloc[0:1].index[0]
        df = df.iloc[idx_ini:idx_end]
    
        state.__setitem__('df',df)
        state.__setitem__('flags',flags)
        

        return state



