from imports import *
from data_analysis import *
from text_description import *
from plot_suite import *

def app(state, usage_function): 
    df = state.__getitem__('df')
    flags = state.__getitem__('flags')

    graph = st.beta_container()

    with graph:
        st.header(graph_title())
        st.markdown(graph_markdown())

        usage_function(df, flags)
