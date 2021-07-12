from data_analysis import *
from text_description import *
from imports import *

header = st.beta_container()
dataset = st.beta_container()
load = st.beta_container()
graph = st.beta_container()

@st.cache
def get_data_yoko(fname):
    df = load_yokogawa_dataset(fname)
    return df

@st.cache
def get_data_smartmetropolis(fname, id):
    df = load_smartmetropolis_dataset(fname, label=id)
    return df

st.markdown(
        f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {1100}px;
       
    }}
</style>
""",
        unsafe_allow_html=True,
    )


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

    
    default_yoko = 'https://drive.google.com/file/d/1EFRE6md8BYFfOYOcueZbKc_k47eK7R93/view?usp=sharing' # dataset completo
    default_yoko = 'https://drive.google.com/file/d/1eBi9kUSRWjGubCzI77TfSEHOi4rxOmCf/view?usp=sharing' # dataset cortado
    default_comade = 'https://drive.google.com/file/d/1xHjrBebEb02rGRkXOfGc64wJicHpNQcr/view?usp=sharing'
    default_semade = 'https://drive.google.com/file/d/1tLZBHQqe5rbCW4ijbX_ghi74k-_7Ds-X/view?usp=sharing'     

    st.markdown('Insira os links públicos para os datasets de interesse.')

    default_yoko = st.text_input('Link para o dataset do CW500:', value=default_yoko)
    default_comade = st.text_input('Link para o dataset do Smartcampus 1.0:', value=default_comade)
    default_semade = st.text_input('Link para o dataset do Smartcampus 2.0:', value=default_semade)
   
    fname_yoko = 'https://drive.google.com/uc?export=download&id='+default_yoko.split('/')[-2]
    fname_comade = 'https://drive.google.com/uc?export=download&id='+default_comade.split('/')[-2]
    fname_semade = 'https://drive.google.com/uc?export=download&id='+default_semade.split('/')[-2]

    which_datasets = st.multiselect('Escolha os datasets a serem analisados:', dataset_options, dataset_options)


    df_lengths = dict()
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

label_yoko = ['AVG_V1[V][V]','AVG_V2[V][V]','AVG_V3[V][V]','AVG_A1[A][A]','AVG_A2[A][A]','AVG_A3[A][A]']
label_sade = ['voltA', 'voltB', 'voltC','correnteA', 'correnteB', 'correnteC']
label_cade = ['voltA', 'voltB', 'voltC','correnteA', 'correnteB', 'correnteC']
labels = ['VA-', 'VB-', 'VC-', 'IA-', 'IB-', 'IC-']
for i in range(6):
    label_sade[i]+='_semade'
    label_cade[i]+='_comade'


with graph:
    st.header(graph_title())
    st.markdown(graph_markdown())

    
    graph1 = st.beta_container()
    graph2 = st.beta_container()


    graph1.subheader('Séries temporais das tensões/correntes medidas')

    title = 'Análise da série temporal'
    #idx_ini = 100
    #idx_end = -1

    fig = make_subplots(rows=2, cols=3, shared_xaxes=False, subplot_titles=('Tensão A','Tensão B', 'Tensão C', 'Corrente A', 'Corrente B', 'Corrente C'))

    for i in range(6):
        x = int(np.floor(i/3))+1
        y = int(i - 3*np.floor(i/3))+1

        if(flags['df_yoko']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'].iloc[idx_ini:idx_end], y=df[label_yoko[i]].iloc[idx_ini:idx_end], name=labels[i]+'cw500'),
                row=x, col=y
            )
        if(flags['df_semade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'].iloc[idx_ini:idx_end], y=df[label_sade[i]].iloc[idx_ini:idx_end], name=labels[i]+'semade'),
                row=x, col=y
            )
        if(flags['df_comade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'].iloc[idx_ini:idx_end], y=df[label_cade[i]].iloc[idx_ini:idx_end], name=labels[i]+'comade'),
                row=x, col=y
            )


    fig.update_layout(height=700, width=1100)#, title_text=title)
    fig.update_yaxes(title_text="", showgrid=True)
    fig.update_xaxes(title_text="", showgrid=True)

    fig['layout']['yaxis']['title']='Tensão (V)'
    fig['layout']['yaxis4']['title']='Corrente (A)'

    #fig.show()
    graph1.write(fig)

    graph2.subheader('Séries temporais dos erros')

    fig = make_subplots(rows=2, cols=3, shared_xaxes=False, 
                      subplot_titles=('Tensão A','Tensão B', 'Tensão C', 
                                      'Corrente A', 'Corrente B', 'Corrente C'))

    for i in range(6):
        x = int(np.floor(i/3))+1
        y = int(i - 3*np.floor(i/3))+1

        error_sade = 100*np.abs((df[label_sade[i]].iloc[idx_ini:idx_end]-df[label_yoko[i]].iloc[idx_ini:idx_end])/df[label_yoko[i]].iloc[idx_ini:idx_end])
        error_cade = 100*np.abs((df[label_cade[i]].iloc[idx_ini:idx_end]-df[label_yoko[i]].iloc[idx_ini:idx_end])/df[label_yoko[i]].iloc[idx_ini:idx_end])

        if(flags['df_yoko'] and flags['df_semade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'].iloc[idx_ini:idx_end], y=error_sade, name=labels[i]+'semadeVS.cw500'),
                row=x, col=y
            )
        if(flags['df_yoko'] and flags['df_comade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'].iloc[idx_ini:idx_end], y=error_cade, name=labels[i]+'comadeVS.cw500'),
                row=x, col=y
            )


    fig.update_layout(height=700, width=1100)#, title_text=title)
    fig.update_yaxes(title_text="", showgrid=True)
    fig.update_xaxes(title_text="", showgrid=True)

    fig['layout']['yaxis']['title']='Erro relativo (%)'
    fig['layout']['yaxis4']['title']='Erro relativo (%)'

    #fig.show()
    graph2.write(fig)
