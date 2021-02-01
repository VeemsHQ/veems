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
  isLoading,
}) => (
  <ChannelManagerVideos
    videos={videos}
    isLoading={isLoading}
  />
);

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({}, dispatch),
});

const mapStateToProps = (state, ownProps) => {
  let videos;
  if (state.channels.activeChannelVideos === undefined) {
    videos = ownProps.videos;
  } else {
    videos = state.channels.activeChannelVideos;
  }
  return {
    videos: videos,
    isLoading: state.channels.activeChannelVideosLoading,
  };
};

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
