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

const { store, persistor } = configureStore();

// Component connected to Redux store
function Container(props) {
  const { activeChannelID } = props

  const [channels, setChannels] = useState(props.channels);
  //const [activeChannelID, setActiveChannelID] = useState(0);

  useEffect(() => { 
    /* If we have anything in the persisted Redux store
    at this point we can assume that we should use that instead of the
    data passed from Django. If not we will use Django. */
    if (props && props.storeChannels && props.storeChannels.length > 0)
      setChannels(storeChannels);
  }, [props.storeChannels])

  useEffect(() => {
    // Here we should hit a rerender on change of activeChannelID from CreateChannel. 
    // Currently not hit.
    console.log("rerender")
  }, [activeChannelID])

  const handleSelectChannel = async () => { 
    // select api call
  };
  
  return (
    <SelectChannelDropdown channels={channels} activeID={activeChannelID} onSelectChannel={() => handleSelectChannel()} />
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
  storeChannels: state.channels.currentChannels,
  activeChannelID: state.channels.activeChannelID,
});

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

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
        <PersistGate loading={null} persistor={persistor}>
          <Provider store={store}>
            <ConnectedContainer {...params} />
          </Provider>
        </PersistGate>
      ,
      element
    )
  );
};

