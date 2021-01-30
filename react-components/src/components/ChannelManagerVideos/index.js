import React, { useState } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import ChannelManagerVideos from './ChannelManagerVideos';
import {
  getAllVideosForChannelRequest,
} from '../../api/api';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  videos,
  channelId,
}) => {

  /**
  THIS CODE BLOCK WITH REQUEST = BELOW ERROR

  ChannelManagerVideos/index.js: 'await' is only allowed within async
  functions and at the top levels of modules (21:29)
  */
  const { response, data } = await getAllVideosForChannelRequest(channelId);
  if (response?.status === 200) {
    videos = data;
  }
  return (
    <ChannelManagerVideos
      videos={videos}
      channelId={channelId}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({}, dispatch),
});

const mapStateToProps = (state) => ({
  // When the selected channel changes, we want to re-render the videos.
  channelId: state.channels.activeChannelID,
});

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateChannelManagerVideos = ({
  element,
  ...params
}) => (
  ReactDOM.render(
    <PersistGate loading={null} persistor={persistor}>
      <Provider store={store}>
        <ConnectedContainer {...params} />
      </Provider>
    </PersistGate>,
    element,
  )
);
