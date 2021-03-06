import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import SelectActiveChannelDropdown from './component';

import {
  setActiveChannel,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  channels,
  activeChannelId,
  setActiveChannel,
}) => {

  const handleSelectChannel = async (e) => {
    const channelId = e.target.value;
    if (channelId) {
      setActiveChannel(channelId);
    } else {
      console.error('handleSelectChannel, channelId not set');
    }
  };
  return (
    <SelectActiveChannelDropdown
      channels={channels}
      activeID={activeChannelId}
      onSelectChannel={(e) => handleSelectChannel(e)}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setActiveChannel: setActiveChannel,
  }, dispatch),
});

const mapStateToProps = (state, ownProps) => {
  let activeChannelId;
  let channels = [];
  if (state.channels.activeChannelId === null) {
    activeChannelId = ownProps.activeChannelId;
  } else {
    activeChannelId = state.channels.activeChannelId;
  }
  if (ownProps.channels && !state.channels.channels.length) {
    channels = ownProps.channels;
  } else {
    channels = state.channels.channels;
  }
  return {
    channels: channels,
    activeChannelId: activeChannelId,
  };
};

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
