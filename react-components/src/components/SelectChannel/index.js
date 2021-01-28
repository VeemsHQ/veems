import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import SelectChannelDropdown from './SelectChannelDropdown';

import {
  setActiveChannelAction,
  setChannelsDbStaleAction,
} from '../../actions/index';

import {
  setChannelRequest,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  isDbStale,
  storeChannels,
  channels,
  activeChannelID,
  setChannelsDbStale,
  setActiveChannel,
}) => {
  const [dropdownChannels, setDropdownChannels] = useState(channels);

  useEffect(() => {
    /* If we have anything in the persisted Redux store
    at this point and db channels are stale we can assume that we should use that
    instead of the data passed from db. If not we will use db. */
    const dbChannels = channels;
    if (storeChannels && isDbStale) {
      setDropdownChannels(storeChannels);
      // Reset stale state now we are using the most up to date.
      setChannelsDbStale(false);
    } else {
      setDropdownChannels(dbChannels);
    }
  }, [storeChannels]);

  const handleSelectChannel = async (e) => {
    if (e.target.value) {
      // update the active channel in the store and on the server
      setActiveChannel(e.target.value);
      await setChannelRequest(e.target.value);
      window.SELECTED_CHANNEL_ID = e.target.value;
    }
  };

  return (
    <SelectChannelDropdown
      channels={dropdownChannels}
      activeID={activeChannelID}
      onSelectChannel={(e) => handleSelectChannel(e)}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setActiveChannel: setActiveChannelAction,
    setChannelsDbStale: setChannelsDbStaleAction,
  }, dispatch),
});

const mapStateToProps = (state) => ({
  storeChannels: state.channels.channels,
  activeChannelID: state.channels.activeChannelID,
  isDbStale: state.channels.isDbStale,
});

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const SelectChannelContainer = ({
  element,
  ...params
}) => (
  ReactDOM.render(
    <PersistGate loading={null} persistor={persistor}>
      <Provider store={store}>
        <ConnectedContainer {...params} />
      </Provider>
    </PersistGate>,
    element || document.createElement('div'), // for testing purposes
  )
);
