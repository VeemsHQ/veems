import {
    START_VIDEO_UPLOADING,
    SET_VIDEO_UPLOADING_FEEDBACK,
    SET_ACTIVE_VIDEO_DETAIL_DATA,
    SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTOR_VISIBLE,
    SET_VIDEO_DETAIL_MODAL_OPEN,
} from '../actions/ActionTypes';
import { randomItem } from '../utils';

const urlParams = new URLSearchParams(window.location.search);
const queryParamUploadModalOpen = urlParams.get('display') == 'upload-modal';
export const initialState = {
    uploadingVideosFeedback: {},// DEL onreload
    uploadingVideos: null,// DEL onreload
    activeVideoDetailData: {
        video: {},
        id: null,
        autogenThumbnailChoices: [],
    },// DEL onreload
    isDbStale: false,
    isVideoFileSelectorVisible: true, // DEL onreload
    isVideoDetailModalOpen: queryParamUploadModalOpen, // DEL onreload
    displayUploadModal: queryParamUploadModalOpen, // DEL onreload
};

export default (state = initialState, action) => {
    const { payload, type } = action;
    let newState = null;
    let videoId = null;

    switch (type) {
        case SET_VIDEO_DETAIL_MODAL_OPEN:
            console.debug('Reduce SET_VIDEO_DETAIL_MODAL_OPEN');
            console.log(payload);
            return { ...state, isVideoDetailModalOpen: payload };
        case SET_ACTIVE_VIDEO_DETAIL_DATA:
            console.debug('Reduce SET_ACTIVE_VIDEO_DETAIL_DATA');
            const activeVideoDetailData = {
                video: payload,
                id: payload.id,
                autogenThumbnailChoices: getAutogenThumbnailChoices(payload),
            }
            return { ...state, activeVideoDetailData: activeVideoDetailData };
        case START_VIDEO_UPLOADING:
            console.debug('Reduce START_VIDEO_UPLOADING');
            videoId = payload;
            newState = { ...state.uploadingVideos, [videoId]: {} };
            return { ...state, uploadingVideos: newState };
        case SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTOR_VISIBLE:
            console.debug('Reduce SET_ACTIVE_VIDEO_DETAIL_FILE_SELECTOR_VISIBLE');
            return { ...state, isVideoFileSelectorVisible: payload };
        case SET_VIDEO_UPLOADING_FEEDBACK:
            console.debug('Reduce SET_VIDEO_UPLOADING_FEEDBACK');
            videoId = state.activeVideoDetailData.id;
            let newFeedback;
            if (state.uploadingVideos) {
                const feedback = state.uploadingVideos[videoId];
                newFeedback = { ...feedback, payload };
            } else {
                newFeedback = payload
            }
            newState = { ...state.uploadingVideos, [videoId]: newFeedback };
            console.log('<>>>> state');
            console.log(newState);
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
