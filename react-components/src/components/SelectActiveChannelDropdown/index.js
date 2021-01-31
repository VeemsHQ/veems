import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import SelectActiveChannelDropdown from './SelectActiveChannelDropdown';

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
  activeChannelId,
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
    const channelId = e.target.value;
    if (channelId) {
      // update the active channel in the store and on the server
      setActiveChannel(channelId);
      await setChannelRequest(channelId);
      window.SELECTED_CHANNEL_ID = channelId;
    }
  };

  return (
    <SelectActiveChannelDropdown
      channels={dropdownChannels}
      activeID={activeChannelId}
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
  activeChannelId: state.channels.activeChannelId,
  isDbStale: state.channels.isDbStale,
});

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateSelectActiveChannelDropdown = ({
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
