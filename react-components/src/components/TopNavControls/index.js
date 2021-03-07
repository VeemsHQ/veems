import React from 'react';
import ReactDOM from 'react-dom';

import { connect, Provider } from 'react-redux';
import { bindActionCreators } from 'redux';
import { PersistGate } from 'redux-persist/integration/react';
import { configureStore } from '../../store';

import TopNavControls from './component';

import {
    createToast,
    toggleVideoLike,
    toggleVideoDislike,
} from '../../actions/index';

const { store, persistor } = configureStore.getInstance();

function Container({
    toggleVideoLike,
    toggleVideoDislike,
    video,
}) {
    const onToggleVideoLikeClicked = async (e) => {
        e.preventDefault();
        toggleVideoLike(video.videoId, video.isLiked)
    }

    const onToggleVideoDislikeClicked = async (e) => {
        e.preventDefault();
        toggleVideoDislike(video.videoId, video.isLiked)
    }

    return (
        <TopNavControls
            onToggleVideoLikeClicked={onToggleVideoLikeClicked}
            onToggleVideoDislikeClicked={onToggleVideoDislikeClicked}
            video={video}
        />
    );
}

const mapDispatchToProps = (dispatch) => ({
    dispatch,
    ...bindActionCreators({
        createToast: createToast,
        toggleVideoLike: toggleVideoLike,
        toggleVideoDislike: toggleVideoDislike,
    }, dispatch),
});

const mapStateToProps = (state, ownProps) => {
    if (!state.video.viewing.videoId) {
        const video = {
            videoId: ownProps.videoId,
            likesCount: ownProps.likesCount,
            dislikesCount: ownProps.dislikesCount,
            likesDislikesPercentage: ownProps.likesDislikesPercentage,
            isLiked: ownProps.isLiked,
        };
        return { video: video };
    } else {
        return {
            video: state.video.viewing,
        };
    }
};

const ConnectedContainer = connect(mapStateToProps, mapDispatchToProps)(Container);

export const CreateTopNavControls = ({
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
