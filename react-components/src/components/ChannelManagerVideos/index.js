import React from 'react';
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
}) => (
  <ChannelManagerVideos
    videos={videos}
    channelId={channelId}
  />
);

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({}, dispatch),
});

const mapStateToProps = (state) => ({
  // When the selected channel changes, we want to re-render the videos.
  channelId: state.channels.activeChannelId,
  videos: state.channels.activeChannelVideos,
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
