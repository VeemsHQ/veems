import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { subscribeToWatcher } from 'redux-action-watcher';
import { configureStore } from '../../store';

import ChannelManagerVideos from './ChannelManagerVideos';
import {
  getAllVideosForChannelRequest,
} from '../../api/api';
import * as aTypes from '../../actions/ActionTypes';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  videos,
  channelId,
}) => {
  console.log(channelId);
  const [data, setData] = useState({
    channelId: channelId,
    videos: videos,
  });

  useEffect(() => {
    // When active Channel Id changes, request Videos for that Channel from the API.
    subscribeToWatcher(store, [
      {
        action: aTypes.SET_ACTIVE_CHANNEL_ID,
        callback: async () => {
          const channelId = store.getState().channels.activeChannelId;
          const { response, data } = await getAllVideosForChannelRequest(channelId);
          console.log(`callback ${channelId}`);
          console.log(response);
          setData({
            channelId: channelId,
            videos: data,
          });
        },
        onStateChange: true,
      },
    ]);
  }, []);

  return (
    <ChannelManagerVideos
      videos={data.videos}
      channelId={data.channelId}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({}, dispatch),
});

const mapStateToProps = (state) => ({
  // When the selected channel changes, we want to re-render the videos.
  channelId: state.channels.activeChannelId,
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
