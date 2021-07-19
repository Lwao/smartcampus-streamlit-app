from imports import *
from data_analysis import *
from text_description import *
from plot_suite import *
from statistics import *

def load_calibration_dataset(fname):
    df= pd.read_csv(fname,           # filename read in previous cell
                    delimiter=',',           # semicolon(;)/coma(,) separated values
                    decimal=",",             # set decimal point to '.' instead of ','
                    encoding='utf-8',        # encoding in utf-8
                    )
    return df

def full_regression(df, degList, condList, labels):
    predLabels = ['VA_PREDITO','VB_PREDITO','VC_PREDITO','IA_PREDITO','IB_PREDITO','IC_PREDITO']
    labelsReduced = ['VA', 'VB', 'VC', 'IA', 'IB', 'IC']
    pinPointsList = []
    # generate pin points list for each variable: VA, VB, VC, IA, IB, IC
    for i in range(len(condList)): pinPointsList.append(generate_pin_points(np.array(df[labels[2*i+1]]), condList[i]))

    coeff_dict = {}
    r_dict = {}
    for i in range(len(labelsReduced)):
        temp = RangedRegression(x = df[labels[2*i]],   # read value
                                y = df[labels[2*i+1]], # real value
                                degree=degList[i], 
                                pin_points=pinPointsList[i])
        y_pred, _ = temp.ranged_prediction()
        df[predLabels[i]] = y_pred.reshape(-1)
        coeff_dict[labelsReduced[i]] = temp.get_coefficients()
        r_dict[labelsReduced[i]] = temp.get_score()

    return df, coeff_dict, r_dict

def app(): 

    initialization = st.beta_container()
    configuration = st.beta_container()
    results = st.beta_container()

    labelsReduced = ['VA', 'VB', 'VC', 'IA', 'IB', 'IC']
    predLabels = ['VA_PREDITO','VB_PREDITO','VC_PREDITO','IA_PREDITO','IB_PREDITO','IC_PREDITO']

    labels = ['VA_LIDO', 'VA_REAL',
              'VB_LIDO', 'VB_REAL',
              'VC_LIDO', 'VC_REAL',
              'IA_LIDO', 'IA_REAL',
              'IB_LIDO', 'IB_REAL',
              'IC_LIDO', 'IC_REAL']

    degList = [ # 1st section = 2nd order poly, 2nd section = 1st order poly,  3rd section = 1st order poly, 
                [1], # 2 sections for VA
                [1], # 2 sections for VB
                [3], # 2 sections for VC
                [1], # 2 sections for IA
                [1], # 2 sections for IB
                [1], # 2 sections for IC
            ] # degree for regression of each variable

    condList = [
                [], # conditions for VA
                [], # conditions for VB
                [], # conditions for VC
                [], # conditions for IA
                [], # conditions for IB
                [], # conditions for IC
            ] # condition list for each variable

    with initialization:
        st.header(calibration_title())
        st.markdown(calibration_markdown())
        
        df_test = pd.DataFrame(columns=labels)

        st.write(df_test)

        uploaded_file = st.file_uploader('Carregue o dataset de calibração:', accept_multiple_files=False)
        if uploaded_file is not None: 
            df = load_calibration_dataset(uploaded_file)
            st.write(df.head())
        else: pass

    with configuration:
        st.header('Configurações da calibração')
        st.markdown('Algumas configurações devem ser realizadas para que a calibração atenda os resultados esperados.')

        degree_columns = st.beta_columns(6)

        list_ = ['VA): ', 'VB): ', 'VC): ', 'IA): ', 'IB): ', 'IC): ']
        for i in range(6): degList[i][0] = degree_columns[i].number_input(label='Grau do polinômio (' + list_[i], min_value=1)

        df, coeff_dict, r_dict = full_regression(df, degList, condList, labels)

    with results:
        st.header('Resultados da calibração')
        st.markdown('Aqui são apresentados os resultados numéricos e gráficos da calibração.')

        st.write('**Coeficientes de correlação**: ')
        for i in range(6): st.write(labelsReduced[i] + ': ' + str(r_dict[list(r_dict.keys())[i]]))
        st.write('**Coeficientes das curvas de calibração**: ')
        for i in range(6): st.write(labelsReduced[i] + ': ' + str(coeff_dict[list(coeff_dict.keys())[i]]))

        st.write('**Resultados gráficos**: ')

        # sorting dataset

        dfPlot = df.copy()
        graph1 = st.beta_container()
        graph2 = st.beta_container()

        for i in range(6):
            dfPlot[labels[2*i]] = dfPlot[labels[2*i]].sort_values(ascending=True)
            dfPlot[predLabels[i]] = dfPlot[predLabels[i]].sort_values(ascending=True)

        fig1 = make_subplots(rows=2, cols=3, shared_xaxes=False, 
                    subplot_titles=('Tensão A (V)','Tensão B (V)', 'Tensão C (V)', 
                                      'Corrente A (A)', 'Corrente B (A)', 'Corrente C (A)'))
        fig2 = make_subplots(rows=2, cols=3, shared_xaxes=False, 
                            subplot_titles=('Tensão A','Tensão B', 'Tensão C', 
                                            'Corrente A', 'Corrente B', 'Corrente C'))

        preNames = ['VA-', 'VB-', 'VC-', 'IA-', 'IB-', 'IC-']   
        label1 = 'predito'
        label2 = 'lido'
        for i in range(6):
            x = int(np.floor(i/3))+1
            y = int(i - 3*np.floor(i/3))+1

            fig1.add_trace(
                go.Scatter(x=dfPlot[labels[2*i+1]], y=dfPlot[predLabels[i]], name=preNames[i]+label1),
                row=x, col=y
            )
            fig1.add_trace(
                go.Scatter(x=dfPlot[labels[2*i+1]], y=dfPlot[labels[2*i]], name=preNames[i]+label2),
                row=x, col=y
            )

            fig2.add_trace(
                go.Scatter(y=100*(dfPlot[predLabels[i]]-dfPlot[labels[2*i+1]])/dfPlot[labels[2*i+1]], name='erro' + preNames[i]+label1),
                row=x, col=y
            )
            fig2.add_trace(
                go.Scatter(y=100*(dfPlot[labels[2*i]]-dfPlot[labels[2*i+1]])/dfPlot[labels[2*i+1]], name='erro' + preNames[i]+label2),
                row=x, col=y
            )
            
        

        fig1.update_layout(height=700, width=1100, title_text='Predição/Lido vs. Real')
        fig1.update_xaxes(title_text='Real lido no multimedidor', showgrid=True)
        fig2.update_layout(height=700, width=1100, title_text='Erro relativo da Predição/Lido vs. Real')

        fig1['layout']['yaxis']['title']='Predição/Lido'
        fig1['layout']['yaxis4']['title']='Predição/Lido'
        fig2['layout']['yaxis']['title']='Erro relativo (%)'
        fig2['layout']['yaxis4']['title']='Erro relativo (%)'

        graph1.write(fig1)
        graph2.write(fig2)