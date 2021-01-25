import React from 'react';
import ReactDOM from 'react-dom'

// Redux
import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { configureStore } from '../../store';
import { PersistGate } from 'redux-persist/integration/react'

// Components
import SyncChannelButton from './SyncChannelButton';

// Actions
import {
  setSyncModalOpenAction,
} from '../../actions/index';

// api
// import { syncChannelRequest } from '../../api/api';

const { store, persistor } = configureStore.getInstance();

// Component connected to Redux store
export function Container(props) {
  const handleSyncChannel = () => {
    // todo when server calls in place 
    // syncChannelRequest();
  };
  const handleModalClose = () => props.setSyncModalOpen(false);
  const handleModalOpen = () => props.setSyncModalOpen(true);
  return (
    <SyncChannelButton bModalOpen={props.bSyncModalOpen} onSyncChannel={handleSyncChannel} onModalOpen={() => handleModalOpen} onModalClose={() => handleModalClose} />
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({
      setSyncModalOpen: setSyncModalOpenAction,
    }, dispatch),
  };
};

const mapStateToProps = state => ({
  bSyncModalOpen: state.channels.bSyncModalOpen,
});

export const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

/* Entry point for DOM element render and subsequent button render.
This only deal with the above and handling API requests. The SyncChannel
component will manage logic.
*/
export const SyncChannel = ({
  element,
  ...params
}) => {
  return (
    ReactDOM.render(
      <Provider store={store}>
        <PersistGate loading={null} persistor={persistor}>
          <ConnectedContainer {...params} />
        </PersistGate>
      </Provider>,
      element
    )
  );
};

