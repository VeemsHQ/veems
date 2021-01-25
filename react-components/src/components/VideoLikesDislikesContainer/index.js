import React from 'react';
import ReactDOM from 'react-dom'

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { configureStore } from '../../store';
import { PersistGate } from 'redux-persist/integration/react'

import VideoLikesDislikesContainer from './VideoLikesDislikesContainer';

import {
  setSyncModalOpenAction,
  setActiveChannelAction,
  setChannelsAction,
} from '../../actions/index';

import {
  createChannelRequest,
  getChannelsRequest,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

// Component connected to Redux store
function Container(props) {

  const handleCreateChannel = async (name, desc, isSynced) => {

    const {response, data } = await createChannelRequest(name, desc, isSynced);

    if (response?.status === 400)
      return false;

    /* Update active channel redux list from server. Alternativly we could merge
    the returned active channel below to  into an already populated list reduce API calls, but
    leaving this up to the server to manage is safer */
    const allChannels =  await getChannelsRequest();
    if (allChannels?.data && Array.isArray(allChannels.data))
      await props.setChannels(allChannels.data);

    // Set active channel and store ID.
    if (data?.id) {
      window.SELECTED_CHANNEL_ID = data.id;
      await props.setActiveChannel(data.id);
    }

    /* If isSynced then enable correct tab and dispatch Redux action to
    open modal dialog on page */
    if (isSynced) {
      await props.setSyncModalOpen(true);
      window.location.pathname = '/channel/sync/';
    } else {
      await props.setSyncModalOpen(false);
    }

    return true;
  };

  return (
    <VideoLikesDislikesContainer onCreateChannel={handleCreateChannel} />
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({
      setSyncModalOpen: setSyncModalOpenAction,
      setActiveChannel: setActiveChannelAction,
      setChannels: setChannelsAction,
    }, dispatch),
  };
};

const ConnectedContainer = connect(null, mapDispatchToProps)(Container);

export const CreateVideoLikesDislikesContainer = ({
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

