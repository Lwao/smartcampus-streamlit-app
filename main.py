from data_analysis import *
from text_description import *
from imports import *
from plot_suite import *

from pages import data_init, graphs

def main():
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

    state = _get_state()

    pages = {
        'Inicializar o dataset': data_init.app,
        'Plot de tensão/corrente': graphs.app,
        'Plot de frequência': graphs.app,
        'Plot de fator de potência': graphs.app,
        'Plot de potências (P/S/Q)': graphs.app
        }

    st.sidebar.title("Funcionalidades")
    choice = st.sidebar.radio("Selecione a página", tuple(pages.keys()))

    # Display the selected page with the session state
    if(choice=='Inicializar o dataset'): state = pages[choice](state)
    elif(choice=='Plot de tensão/corrente'): pages[choice](state, plot_voltage_n_current)
    elif(choice=='Plot de frequência'): pages[choice](state, plot_frequency)
    elif(choice=='Plot de fator de potência'): pages[choice](state, plot_power_factor)
    elif(choice=='Plot de potências (P/S/Q)'): pages[choice](state, plot_power)

    # Mandatory to avoid rollbacks with widgets, must be called at the end of your app
    state.sync()

class _SessionState:

    def __init__(self, session, hash_funcs):
        """Initialize SessionState instance."""
        self.__dict__["_state"] = {
            "data": {},
            "hash": None,
            "hasher": _CodeHasher(hash_funcs),
            "is_rerun": False,
            "session": session,
        }

    def __call__(self, **kwargs):
        """Initialize state data once."""
        for item, value in kwargs.items():
            if item not in self._state["data"]:
                self._state["data"][item] = value

    def __getitem__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)
        
    def __getattr__(self, item):
        """Return a saved state value, None if item is undefined."""
        return self._state["data"].get(item, None)

    def __setitem__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value

    def __setattr__(self, item, value):
        """Set state value."""
        self._state["data"][item] = value
    
    def clear(self):
        """Clear session state and request a rerun."""
        self._state["data"].clear()
        self._state["session"].request_rerun()
    
    def sync(self):
        """Rerun the app with all state values up to date from the beginning to fix rollbacks."""

        # Ensure to rerun only once to avoid infinite loops
        # caused by a constantly changing state value at each run.
        #
        # Example: state.value += 1
        if self._state["is_rerun"]:
            self._state["is_rerun"] = False
        
        elif self._state["hash"] is not None:
            if self._state["hash"] != self._state["hasher"].to_bytes(self._state["data"], None):
                self._state["is_rerun"] = True
                self._state["session"].request_rerun()

        self._state["hash"] = self._state["hasher"].to_bytes(self._state["data"], None)


def _get_session():
    session_id = get_report_ctx().session_id
    session_info = Server.get_current()._get_session_info(session_id)

    if session_info is None:
        raise RuntimeError("Couldn't get your Streamlit Session object.")
    
    return session_info.session


def _get_state(hash_funcs=None):
    session = _get_session()

    if not hasattr(session, "_custom_session_state"):
        session._custom_session_state = _SessionState(session, hash_funcs)

    return session._custom_session_state


if __name__ == "__main__":
    main()