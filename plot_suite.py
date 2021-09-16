from imports import *

marker_yoko = dict(color='#636EFA',size=1)
marker_sade = dict(color='#B6E880',size=1)
marker_cade = dict(color='#EF553B',size=1)

#@st.cache(suppress_st_warning=True)
def plot_voltage_n_current(df, flags):
    graph1 = st.container()
    graph2 = st.container()
    graph1.subheader('Séries temporais das tensões/correntes medidas')

    title = 'Análise da série temporal'
    
    label_yoko = ['AVG_V1[V][V]','AVG_V2[V][V]','AVG_V3[V][V]','AVG_A1[A][A]','AVG_A2[A][A]','AVG_A3[A][A]']
    label_sade = ['voltA', 'voltB', 'voltC','correnteA', 'correnteB', 'correnteC']
    label_cade = ['voltA', 'voltB', 'voltC','correnteA', 'correnteB', 'correnteC']
    labels = ['VA-', 'VB-', 'VC-', 'IA-', 'IB-', 'IC-']

    for i in range(6):
        label_sade[i]+='_semade'
        label_cade[i]+='_comade'

    fig = make_subplots(rows=2, cols=3, shared_xaxes=False, subplot_titles=('Tensão A','Tensão B', 'Tensão C', 'Corrente A', 'Corrente B', 'Corrente C'))

    for i in range(6):
        x = int(np.floor(i/3))+1
        y = int(i - 3*np.floor(i/3))+1

        if(flags['df_yoko']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'], y=df[label_yoko[i]], name=labels[i]+'cw500', marker=marker_yoko),
                row=x, col=y
            )
        if(flags['df_semade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'], y=df[label_sade[i]], name=labels[i]+'semade', marker=marker_sade),
                row=x, col=y
            )
        if(flags['df_comade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'], y=df[label_cade[i]], name=labels[i]+'comade', marker=marker_cade),
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

        if(flags['df_yoko']):
            error_sade = 100*np.abs((df[label_sade[i]]-df[label_yoko[i]])/df[label_yoko[i]])
            error_cade = 100*np.abs((df[label_cade[i]]-df[label_yoko[i]])/df[label_yoko[i]])
        else:
            error_scade = 100*np.abs((df[label_cade[i]]-df[label_sade[i]])/df[label_sade[i]])


        
        if(flags['df_yoko'] and flags['df_semade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'], y=error_sade, name=labels[i]+'semadeVS.cw500', marker=marker_yoko),
                row=x, col=y
            )
        if(flags['df_yoko'] and flags['df_comade']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'], y=error_cade, name=labels[i]+'comadeVS.cw500', marker=marker_sade),
                row=x, col=y
            )
        if(not flags['df_yoko']):
            fig.add_trace(
                go.Scatter(x=df['Timestamp'], y=error_scade, name=labels[i]+'comadeVS.semade', marker=marker_cade),
                row=x, col=y
            )


    fig.update_layout(height=700, width=1100)#, title_text=title)
    fig.update_yaxes(title_text="", showgrid=True)
    fig.update_xaxes(title_text="", showgrid=True)

    fig['layout']['yaxis']['title']='Erro relativo (%)'
    fig['layout']['yaxis4']['title']='Erro relativo (%)'

    #fig.show()
    graph2.write(fig)

#@st.cache(suppress_st_warning=True)
def plot_frequency(df, flags):
    graph = st.container()
    graph.subheader('Séries temporais das frequências medidas')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=False)


    if(flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['AVG_f[Hz][Hz]'], name='cw500', marker=marker_yoko),
            row=1, col=1
        )
    if(flags['df_semade']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['frequencia_semade'], name='semade', marker=marker_sade),
            row=1, col=1
        )
    if(flags['df_comade']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['frequencia_comade'], name='comade', marker=marker_cade),
            row=1, col=1
        )


    if(flags['df_semade'] and flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.abs(100*(df['frequencia_semade']-df['AVG_f[Hz][Hz]'])/df['AVG_f[Hz][Hz]']), name='erro_semadeVS.CW500', marker=marker_yoko),
            row=2, col=1
        )
    if(flags['df_comade'] and flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.abs(100*(df['frequencia_comade']-df['AVG_f[Hz][Hz]'])/df['AVG_f[Hz][Hz]']), name='erro_comadeVS.CW500', marker=marker_sade),
            row=2, col=1
        )
    if(flags['df_comade'] and flags['df_semade'] and not flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.abs(100*(df['frequencia_comade']-df['frequencia_semade'])/df['frequencia_semade']), name='erro_comadeVS.semade', marker=marker_cade),
            row=2, col=1
        )
    


    fig.update_layout(height=600, width=800)

    fig['layout']['yaxis1']['title']= 'Frequência (Hz)'
    fig['layout']['yaxis2']['title']='Erro relativo (%)'

    graph.write(fig)

#@st.cache(suppress_st_warning=True)
def plot_power_factor(df, flags):
    graph = st.container()
    graph.subheader('Séries temporais dos fatores de potência')

    fig = make_subplots(rows=2, cols=1, shared_xaxes=False)


    if(flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['AVG_PF[]'], name='cw500', marker=marker_yoko),
            row=1, col=1
        )
    if(flags['df_semade']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['fatorDePotencia_semade'], name='semade', marker=marker_sade),
            row=1, col=1
        )
    if(flags['df_comade']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['fatorDePotencia_comade'], name='comade', marker=marker_cade),
            row=1, col=1
        )

    if(flags['df_comade'] and flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.abs(100*(df['fatorDePotencia_comade']-df['AVG_PF[]'])/df['AVG_PF[]']), name='erro_comadeVS.CW500', marker=marker_cade),
            row=1, col=1
        )
    if(flags['df_semade'] and flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.abs(100*(df['fatorDePotencia_semade']-df['AVG_PF[]'])/df['AVG_PF[]']), name='erro_semadeVS.CW500', marker=marker_sade),
            row=2, col=1
        )
    if(flags['df_comade'] and flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.abs(100*(df['fatorDePotencia_comade']-df['AVG_PF[]'])/df['AVG_PF[]']), name='erro_comadeVS.CW500'),
            row=2, col=1
        )
    if(flags['df_comade'] and flags['df_semade'] and not flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.abs(100*(df['fatorDePotencia_comade']-df['fatorDePotencia_semade'])/df['fatorDePotencia_semade']), name='erro_comadeVS.semade'),
            row=2, col=1
        )
    


    fig.update_layout(height=600, width=800)

    fig['layout']['yaxis1']['title']= 'Fator de potência (Hz)'
    fig['layout']['yaxis2']['title']='Erro relativo (%)'

    graph.write(fig)

#@st.cache(suppress_st_warning=True)
def plot_power(df, flags):
    graph = st.container()
    graph.subheader('Séries temporais das potências')

    fig = make_subplots(rows=3, cols=1, shared_xaxes=False)


    if(flags['df_yoko']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=np.sqrt(df['AVG_S[VA][VA]']**2-df['AVG_Q[var][var]']**2)/1000, name='kW-cw500', marker=marker_yoko),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['AVG_S[VA][VA]']/1000, name='kVA-cw500', marker=marker_yoko),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['AVG_Q[var][var]']/1000, name='kvar-cw500', marker=marker_yoko),
            row=3, col=1
        )
    if(flags['df_semade']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['potenciaAtiva_semade'], name='kW-semade', marker=marker_sade),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['potenciaAparente_semade'], name='kVA-semade', marker=marker_sade),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['potenciaReativa_semade'], name='kvar-semade', marker=marker_sade),
            row=3, col=1
        )
    if(flags['df_comade']):
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['potenciaAtiva_comade'], name='kW-comade', marker=marker_cade),
            row=1, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['potenciaAparente_comade'], name='kVA-comade', marker=marker_cade),
            row=2, col=1
        )
        fig.add_trace(
            go.Scatter(x=df['Timestamp'], y=df['potenciaReativa_comade'], name='kvar-comade', marker=marker_cade),
            row=3, col=1
        )



    fig['layout']['yaxis1']['title']= 'Potência ativa (kW)'
    fig['layout']['yaxis2']['title']= 'Potência aparente (kVA)'
    fig['layout']['yaxis3']['title']= 'Potência reativa (kvar)'

    fig.update_layout(height=700, width=700)

    graph.write(fig)






