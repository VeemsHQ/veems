import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import VideoLikeDislikeWidget from './component';

import {
  createToastAction,
  toggleVideoLike,
  toggleVideoDislike,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

function Container(props) {
  const { video } = props;

  return (
    <VideoLikeDislikeWidget
      onToggleVideoLikeClicked={() => props.toggleVideoLike(props.videoId)}
      onToggleVideoDislikeClicked={() => props.toggleVideoDislike(props.videoId)}
      video={video}
    />
  );
}

const mapDispatchToProps = (dispatch) => ({
  dispatch,
  ...bindActionCreators({
    createToast: createToastAction,
    toggleVideoLike: toggleVideoLike,
    toggleVideoDislike: toggleVideoDislike,
  }, dispatch),
});

const mapStateToProps = (state, ownProps) => {
  if (!state.video.viewing.videoId) {
    return {
      video: {
        videoId: ownProps.videoId,
        likesCount: ownProps.likesCount,
        dislikesCount: ownProps.dislikesCount,
        likesDislikesPercentage: ownProps.likesDislikesPercentage,
        isLiked: ownProps.isLiked,
      }
    };
  } else {
    return {
      video: state.video.viewing,
    };
  }
};

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateVideoLikeDislikeWidget = ({
  element,
  ...params
}) => (
  ReactDOM.render(
    <Provider store={store}>
      <PersistGate loading={null} persistor={persistor}>
        <ConnectedContainer {...params} />
      </PersistGate>
    </Provider>,
    element,
  )
);
