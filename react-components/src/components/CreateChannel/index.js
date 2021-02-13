import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import CreateChannelButton from './CreateChannelButton';
import {
  setChannelSyncModalOpenAction,
  setActiveChannelAction,
  setChannelsAction,
  createToastAction,
} from '../../actions/index';
import {
  createChannelRequest,
  getChannelsRequest,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  setChannelSyncModalOpen,
  setActiveChannel,
  setChannels,
  createToast,
}) => {
  const handleCreateSuccessToast = async () => {
    createToast({
      header: 'Success',
      body: 'New Channel was created!',
    });
  };

  const handleCreateChannel = async (name, desc, isSynced) => {
    const { response, data } = await createChannelRequest(name, desc, isSynced);

    if (response?.status === 400) {
      return [false, response?.data];
    }

    /* Update active channel redux list from server. Alternativly we could merge
    the returned active channel below to  into an already populated list reduce API calls, but
    leaving this up to the server to manage is safer */
    const allChannels = await getChannelsRequest();
    if (allChannels?.data && Array.isArray(allChannels.data)) await setChannels(allChannels.data);

    // Set active channel and store ID.
    if (data?.id) {
      window.SELECTED_CHANNEL_ID = data.id;
      await setActiveChannel(data.id);
    }

    /* If isSynced then enable correct tab and dispatch Redux action to
    open modal dialog on page */
    if (isSynced) {
      await setChannelSyncModalOpen(true);
      window.location.pathname = '/channel/sync/';
    } else {
      await setChannelSyncModalOpen(false);
    }

    return [true, null];
  };

  return (
    <CreateChannelButton
      onCreateChannel={handleCreateChannel}
      onSuccess={handleCreateSuccessToast}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    setChannelSyncModalOpen: setChannelSyncModalOpenAction,
    setActiveChannel: setActiveChannelAction,
    setChannels: setChannelsAction,
    createToast: createToastAction,
  }, dispatch),
});

const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

export const CreateChannelContainer = ({
  element,
  ...params
}) => (
  ReactDOM.render(
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <ConnectedContainer {...params} />
      </PersistGate>
    </Provider>,
    element || document.createElement('div'), // for testing purposes
  )
);
