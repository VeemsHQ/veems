import React from 'react';
import ReactDOM from 'react-dom'

// Redux
import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import configureStore from '../../store';
import { PersistGate } from 'redux-persist/integration/react'

// Components
import CreateChannelButton from './CreateChannelButton';

// Actions
import {
  setSyncModalOpenAction,
  setActiveChannelAction,
} from '../../actions/index';

// api
import { createChannelRequest } from '../../api/api';

const { store, persistor } = configureStore();

// Component connected to Redux store
export function Container(props) {

  const handleCreateChannel = async (name, desc, bSync) => {
     
    const response = await createChannelRequest(name, desc, bSync);
    // Set active channel and store ID.
    if (response && response.data && response.data.id)
      await props.setActiveChannel(response.data.id);

    /* If bSync then enable correct tab and dispatch Redux action to
    open modal dialog on page */ 
    if (bSync) {
      await props.setSyncModalOpen(true);
      window.location.pathname = '/channel/sync/';
    } else {
      await props.setSyncModalOpen(false);
    }
  };
  
  return (
    <CreateChannelButton onCreateChannel={handleCreateChannel} />
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({
      setSyncModalOpen: setSyncModalOpenAction,
      setActiveChannel: setActiveChannelAction,
    }, dispatch),
  };
};

export const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

/* Entry point for DOM element render and subsequent button render.
This only deal with the above and handling API requests. The SyncChannel
component will manage logic.
*/
export const CreateChannel = ({
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

