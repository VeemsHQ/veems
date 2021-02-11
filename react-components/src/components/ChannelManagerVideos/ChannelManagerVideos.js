import React from 'react';

import { EditVideoButtonContainer } from '../EditVideoButton';

import 'regenerator-runtime/runtime.js';

const descMaxLen = 150;
const truncate = (input, max) => (input.length > max ? `${input.substring(0, max + 1)}...` : input);

export const ChannelManagerVideos = ({
  videos,
  isLoading,
  isModalOpen,
  onModalClose,
  onModalOpen,
}) => (
  <>
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
                  <a href="#" className="thumbnail d-inline-block mr-2 bg-secondary" />
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
                  <a href="#" className="thumbnail  d-inline-block mr-2 bg-secondary" />
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
                  <a href="#" className="thumbnail  d-inline-block mr-2 bg-secondary" />
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
                <a href="#" className="thumbnail d-inline-block mr-2">
                  <img className="card-img-top w-100" src={video.thumbnail_image_medium_url} alt={video.title} />
                  <div className="overlays">{video.video_duration}</div>
                </a>
                <div className="metadata-container d-flex">
                  <div className="content p-2">
                    <h5 className="m-0 mb-1"><a href="#">{video.title}</a></h5>
                    <div className="metadata">
                      <div className="card-text text-muted text-wrap text-truncate">
                        <a href="#">{truncate(video.description, descMaxLen)}</a>
                      </div>
                    </div>
                  </div>
                  <div className="overlay align-items-center">
                    <EditVideoButtonContainer
                      videoId={video.id}
                      isModalOpen={isModalOpen}
                      onModalOpen={() => onModalOpen}
                      onModalClose={() => onModalClose}
                    />
                    <a href={`/v/${video.id}/`} className="btn" target="_blank"><i className="material-icons text-secondary">play_circle_outline</i></a>
                    <a href="#" className="btn"><i className="material-icons text-secondary">delete</i></a>
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
  </>
);

export default ChannelManagerVideos;
