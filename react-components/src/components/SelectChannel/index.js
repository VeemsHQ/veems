import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom'

// Redux
import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { configureStore } from '../../store';
import { PersistGate } from 'redux-persist/integration/react'

// Components
import SelectChannelDropdown from './SelectChannelDropdown';

// Actions
import {
  setSyncModalOpenAction,
  setActiveChannelAction,
} from '../../actions/index';

// api
import { 
  setChannelRequest,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

// Component connected to Redux store
function Container(props) {
  const [channels, setChannels] = useState(props.channels);

  useEffect(() => { 
    /* If we have anything in the persisted Redux store
    at this point we can assume that we should use that instead of the
    data passed from Django. If not we will use Django. */
    if (props?.storeChannels && props.storeChannels.length > 0)
      setChannels(props.storeChannels);
  }, [props.storeChannels])

  const handleSelectChannel = async (e) => { 
    if (e.target.value){
      // update the active channel in the store and on the server
      props.setActiveChannel(e.target.value);
      await setChannelRequest(e.target.value);
      window.SELECTED_CHANNEL_ID = e.target.value;
    }
  };
  
  return (
    <SelectChannelDropdown channels={channels} activeID={props.activeChannelID} onSelectChannel={(e) => handleSelectChannel(e)} />
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

const mapStateToProps = state => ({
  storeChannels: state.channels.channels,
  activeChannelID: state.channels.activeChannelID,
});

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

/* Entry point for DOM element render and subsequent button render.
This only deal with the above and handling API requests. The SyncChannel
component will manage logic.
*/
export const SelectChannelContainer = ({
  element,
  ...params
}) => {
  return (
    ReactDOM.render(
        <PersistGate loading={null} persistor={persistor}>
          <Provider store={store}>
            <ConnectedContainer {...params} />
          </Provider>
        </PersistGate>
      ,
      element || document.createElement('div') // for testing purposes
    )
  );
};

