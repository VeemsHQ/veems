import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom'

// Redux
import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import configureStore from '../../store';
import { PersistGate } from 'redux-persist/integration/react'

// Components
import SelectChannelDropdown from './SelectChannelDropdown';

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
  const [channels, setChannels] = useState(props.channels);

  useEffect(() => { }
    /* If we have anything in the persisted Redux store
    at this point we can assume that we should use that instead of the
    data passed from Django. If not we will use Django. */
  , [])

  const handleSelectChannel = async () => { 
    // select api call
  };
  
  return (
    <SelectChannelDropdown channels={channels} onSelectChannel={handleSelectChannel} />
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
export const SelectChannel = ({
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

