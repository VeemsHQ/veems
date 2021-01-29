import React, { useState } from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import ChannelManagerVideos from './ChannelManagerVideos';

const { store, persistor } = configureStore.getInstance();

const Container = ({
  videos,
  channelId,
}) => {
  const [videos_, setVideos] = useState(videos);

  return (
    <ChannelManagerVideos
      videos={videos_}
      channelId={channelId}
    />
  );
};

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({}, dispatch),
});

const mapStateToProps = (state) => ({
  activeChannelID: state.channels.activeChannelID,
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
