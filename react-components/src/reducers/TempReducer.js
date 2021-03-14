import {
    START_VIDEO_UPLOADING,
    SET_VIDEO_UPLOADING_FEEDBACK,
    SET_VIDEO_DETAIL,
    SET_VIDEO_DETAIL_FILE_SELECTOR_IS_VISIBLE,
    SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTED,
    SET_VIDEO_DETAIL_MODAL_OPEN,
    SET_VIDEO_THUMBNAIL_UPLOADING,
    SET_VIDEO_DETAIL_IS_LOADING,
    SET_VIDEO_DETAIL_IS_SAVING,
} from '../actions/ActionTypes';
import { randomItem } from '../utils';

const urlParams = new URLSearchParams(window.location.search);
const queryParamUploadModalOpen = urlParams.get('display') == 'upload-modal';
const initialStateUploadingVideo = {
    autogenThumbnailChoices: [],
    thumbnailImageSmallUrl: null,
    isProcessing: false,
    isUploading: true,
    isViewable: false,
    percentageUploaded: 0,
}
export const initialState = {
    uploadingVideos: {
    },
    videoDetail: {
        video: {},
        id: null,
        autogenThumbnailChoices: [],
    },
    videoDetailForm: {
        apiErrors: {},
        isFileSelectorVisible: queryParamUploadModalOpen,
        isFileSelected: false,
        isLoading: false,
        isThumbnailUploading: false,
        // thumbsUpdatedFromUploadFeedback: false,
        // isProcessing: false,
        // isViewable: false,
        isSaving: false,
    },
    isVideoDetailModalOpen: queryParamUploadModalOpen,
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
                        videoDetailForm: initialState.videoDetailForm,
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
            newState = { ...state.uploadingVideos, [videoId]: initialStateUploadingVideo };
            return {
                ...state, uploadingVideos: newState
            }
        case SET_VIDEO_DETAIL_FILE_SELECTOR_IS_VISIBLE:
            return {
                ...state, ...{ videoDetailForm: { ...state.videoDetailForm, isFileSelectorVisible: payload } }
            };
        case SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTED:
            return {
                ...state, ...{ videoDetailForm: { ...state.videoDetailForm, isFileSelected: payload } }
            };
        case SET_VIDEO_DETAIL_IS_LOADING:
            return {
                ...state, ...{ videoDetailForm: { ...state.videoDetailForm, isLoading: payload } }
            };
        case SET_VIDEO_DETAIL_IS_SAVING:
            return {
                ...state, ...{ videoDetailForm: { ...state.videoDetailForm, isSaving: payload } }
            };
        case SET_VIDEO_THUMBNAIL_UPLOADING:
            return {
                ...state, ...{ videoDetailForm: { ...state.videoDetailForm, isThumbnailUploading: payload } }
            };
        case SET_VIDEO_UPLOADING_FEEDBACK:
            videoId = payload[0];
            let newFeedbackForVideo = { ...state.uploadingVideos[videoId], ...payload[1] };
            let newVideoDetailVideoItem = {
                ...state.videoDetail.video,
                thumbnail_image_small_url: newFeedbackForVideo.thumbnailImageSmallUrl,
            }
            return {
                ...state,
                uploadingVideos: {
                    ...state.uploadingVideos,
                    [videoId]: newFeedbackForVideo,
                },
                videoDetail: {
                    ...state.videoDetail,
                    video: newVideoDetailVideoItem,
                }
            };
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
