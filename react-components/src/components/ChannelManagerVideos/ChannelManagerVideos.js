import React, {useState} from 'react';

import { VideoDetailModalContainer } from '../VideoDetailModal';
import { DeleteVideoButtonContainer } from '../DeleteVideoButton';

import 'regenerator-runtime/runtime.js';

const descMaxLen = 150;
const truncate = (input, max) => (input.length > max ? `${input.substring(0, max + 1)}...` : input);

export const ChannelManagerVideos = ({
  videos,
  isLoading,
}) => {
  const [isEditModalOpen, setEditModalOpen] = useState(false);
  const handleSetEditModalOpen = () => {
    setEditModalOpen(true);
  }

  const handleSetEditModalClosed = () => {
    setEditModalOpen(false);
  }

  return(<>
    <table className="table mt-4">
      <thead>
        <tr className="text-muted">
          <th scope="col">Video</th>
          <th scope="col">Visibility</th>
          <th scope="col">Date</th>
          <th scope="col">Earnings</th>
          <th scope="col">Views</th>
          <th scope="col">Comments</th>
          <th scope="col">Likes/dislikes</th>
        </tr>
      </thead>
      <tbody className={isLoading === true ? 'channel-videos channel-videos-placeholder' : 'channel-videos '}>
        {isLoading && (
          <>
            <tr>
              <td>
                <div className="d-flex">
                  <a href="#" className="thumbnail thumbnail-small d-inline-block mr-2 bg-secondary" />
                  <div className="metadata-container d-flex">
                    <div className="content p-2">
                      <h5 className="m-0 mb-1 bg-primary" />
                      <div className="metadata">
                        <div className="card-text placeholder-text" />
                      </div>
                    </div>
                  </div>
                </div>
              </td>
              <td>
                <div className="placeholder-text" />
              </td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text bg-success" style={{ minWidth: 30 }} /></td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text" /></td>
            </tr>
            <tr>
              <td>
                <div className="d-flex">
                  <a href="#" className="thumbnail thumbnail-small d-inline-block mr-2 bg-secondary" />
                  <div className="metadata-container d-flex">
                    <div className="content p-2">
                      <h5 className="m-0 mb-1 bg-primary" />
                      <div className="metadata">
                        <div className="card-text placeholder-text" />
                      </div>
                    </div>
                  </div>
                </div>
              </td>
              <td>
                <div className="placeholder-text" />
              </td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text bg-success" style={{ minWidth: 30 }} /></td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text" /></td>
            </tr>
            <tr>
              <td>
                <div className="d-flex">
                  <a href="#" className="thumbnail thumbnail-small d-inline-block mr-2 bg-secondary" />
                  <div className="metadata-container d-flex">
                    <div className="content p-2">
                      <h5 className="m-0 mb-1 bg-primary" />
                      <div className="metadata">
                        <div className="card-text placeholder-text" />
                      </div>
                    </div>
                  </div>
                </div>
              </td>
              <td>
                <div className="placeholder-text" />
              </td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text bg-success" style={{ minWidth: 30 }} /></td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text" /></td>
              <td><div className="placeholder-text" /></td>
            </tr>
          </>
        )}
        {!isLoading && videos.map((video, index) => (
          <tr key={index}>
            <td>
              <div className="d-flex">
                <button type="button" onClick={handleSetEditModalOpen}  className="remove-default-style thumbnail thumbnail-small d-inline-block mr-2">
                  <img className="h-100" src={video.thumbnail_image_small_url} alt={video.title} />
                  <div className="overlays">{video.video_duration}</div>
                </button>
                <div className="metadata-container d-flex">
                  <div className="content p-2">
                    <h5 className="m-0 mb-1"><a href="#">{video.title}</a></h5>
                    <div className="metadata">
                      <div className="card-text text-muted text-wrap text-truncate">
                        <a href="#">{truncate(video.description ? video.description : '', descMaxLen)}</a>
                      </div>
                    </div>
                  </div>
                  <div className="overlay align-items-center">
                    <VideoDetailModalContainer
                      videoId={video.id}
                      isChooseFileUploadModalOpen={true}
                      onSetModalOpen={handleSetEditModalOpen}
                      onSetModalClosed={handleSetEditModalClosed}
                      isModalOpen={isEditModalOpen}
                    />
                    <button type="button" onClick={handleSetEditModalOpen} className="btn"><i className="material-icons text-secondary">create</i></button>
                    <a href={`/v/${video.id}/`} className="btn" target="_blank"><i className="material-icons text-secondary">play_circle_outline</i></a>
                    <DeleteVideoButtonContainer videoId={video.id} />
                    <a href="#" className="btn"><i className="material-icons text-secondary d-none">delete</i></a>
                  </div>
                </div>
              </div>
            </td>
            <td>
              <div className="text-muted">{video.visibility}</div>
              <div className="text-muted">Uploading...</div>
              <div className="progress">
                <div
                  className="progress-bar progress-bar-striped progress-bar-animated"
                  role="progressbar"
                  style={{ width: '55%' }}
                  aria-valuenow="55"
                  aria-valuemin="0"
                  aria-valuemax="100"
                >55%
                </div>
              </div>
            </td>
            <td>{video.created_date_human}<br /><span className="text-muted">Uploaded</span></td>
            <td className="text-success">$0</td>
            <td>{video.view_count}</td>
            <td>{video.comment_count}</td>
            <td>{video.likes_count}/{video.dislikes_count}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </>);
};

export default ChannelManagerVideos;
