import {
    START_VIDEO_UPLOADING,
    SET_VIDEO_UPLOADING_FEEDBACK,
    SET_VIDEO_DETAIL,
    SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTOR_VISIBLE,
    SET_VIDEO_DETAIL_MODAL_OPEN,
    SET_VIDEO_THUMBNAIL_UPLOADING,
} from '../actions/ActionTypes';
import { randomItem } from '../utils';

const urlParams = new URLSearchParams(window.location.search);
const queryParamUploadModalOpen = urlParams.get('display') == 'upload-modal';
export const initialState = {
    uploadingVideos: {
        // null: {
        //     autogenThumbnailChoices: [],
        //     isProcessing: false,
        //     isUploading: false,
        //     isViewable: false,
        // }
    },
    videoDetail: {
        video: {},
        id: null,
        autogenThumbnailChoices: [],
    },
    // TODO: replace container state with this.
    videoDetailForm: {
        apiErrors: {},
        isFileSelectorVisible: true,
        isFileSelected: false,
        isLoading: false,
        isThumbnailUploading: false,
        thumbsUpdatedFromUploadFeedback: false,
        isProcessing: false,
        isUploading: false,
        isViewable: false,
    },
    isVideoThumbnailUploading: false,
    isVideoFileSelectorVisible: true,
    isVideoDetailModalOpen: queryParamUploadModalOpen,
    displayUploadModal: queryParamUploadModalOpen,
};

export default (state = initialState, action) => {
    const { payload, type } = action;
    let newState = null;
    let videoId = null;

    switch (type) {
        case SET_VIDEO_DETAIL_MODAL_OPEN:
            if (payload === false) {
                // On modal close, clear all related state.
                return {
                    ...state,
                    ...{
                        isVideoDetailModalOpen: false,
                        displayUploadModal: false,
                        videoDetail: initialState.videoDetail,
                    }
                };
            } else {
                return { ...state, isVideoDetailModalOpen: payload };
            }
        case SET_VIDEO_DETAIL:
            const videoDetail = {
                video: payload,
                id: payload.id,
                autogenThumbnailChoices: getAutogenThumbnailChoices(payload),
            }
            return { ...state, videoDetail: videoDetail };
        case START_VIDEO_UPLOADING:
            videoId = payload;
            newState = { ...state.uploadingVideos, [videoId]: {} };
            return { ...state, uploadingVideos: newState };
        case SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTOR_VISIBLE:
            return { ...state, isVideoFileSelectorVisible: payload };
        case SET_VIDEO_THUMBNAIL_UPLOADING:
            return { ...state, isVideoThumbnailUploading: payload };
        case SET_VIDEO_UPLOADING_FEEDBACK:
            videoId = state.videoDetail.id;
            let newFeedback;
            if (state.uploadingVideos) {
                const feedback = state.uploadingVideos[videoId];
                newFeedback = { ...feedback, ...payload };
            } else {
                newFeedback = payload
            }
            newState = { ...state.uploadingVideos, [videoId]: newFeedback };
            return { ...state, uploadingVideos: newState };
        default:
            return state;
    }
};

const getAutogenThumbnailChoices = (videoData) => {
    let renditionThumbnails = [];
    if (videoData.video_renditions && videoData.video_renditions.length > 0) {
        // Find highest resolution rendition.
        const bestRendition = videoData.video_renditions.sort((a, b) => b.height - a.height)[0];
        renditionThumbnails = bestRendition.rendition_thumbnails;
    }
    if (renditionThumbnails.length > 0) {
        const thumb0 = randomItem(renditionThumbnails);
        const thumb1 = randomItem(renditionThumbnails);
        const thumb2 = randomItem(renditionThumbnails);
        return [
            [thumb0.id, thumb0.file],
            [thumb1.id, thumb1.file],
            [thumb2.id, thumb2.file],
        ];
    } else {
        return [];
    }
}
