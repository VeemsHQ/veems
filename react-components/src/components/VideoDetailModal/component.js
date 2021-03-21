import React, { useState, useCallback } from 'react';

import debounce from 'lodash.debounce';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import 'regenerator-runtime/runtime.js';

import { valueOrEmpty } from '../../utils';

export const VideoDetailModal = ({
  inputThumbnailFile,
  isModalOpen,
  onModalClose,
  onModalOpen,
  videoDetail,
  videoDetailForm,
  uploadStatus,
  onFormFieldChange,
  onInputThumbnailChange,
  onSetExistingThumbnailAsPrimary,
}) => {
  const saveButtonText = videoDetailForm.isSaving ? 'Saving...' : 'Save Changes';
  let statusText = '';
  const isUploading = uploadStatus && uploadStatus.percentageUploaded < 100;
  if (uploadStatus) {
    if (isUploading) {
      statusText = 'Uploading...'
    } else if (uploadStatus.isProcessing && !uploadStatus.isViewable) {
      statusText = 'Uploaded & processing'
    } else if (uploadStatus.isProcessing && uploadStatus.isViewable) {
      statusText = 'Viewable & processing'
    } else if (!uploadStatus.isProcessing && uploadStatus.isViewable) {
      statusText = 'Viewable & finished processing'
    }
  }
  const uploadThumbnailButtonText = videoDetailForm.isThumbnailUploading ? 'Uploading...' : 'Upload thumbnail';
  const video = videoDetail.video;
  const videoId = valueOrEmpty(video.id);
  const initialTitle = valueOrEmpty(video.title);
  const initialDescription = valueOrEmpty(video.description);
  const initialTags = valueOrEmpty(video.tags);
  const initialVisibility = valueOrEmpty(video.visibility);
  const filename = valueOrEmpty(video.filename);
  const initialPrimaryThumbnailUrl = (
    (uploadStatus && uploadStatus.thumbnailImageSmallUrl) ? uploadStatus.thumbnailImageSmallUrl :
      video.thumbnail_image_small_url
  );
  const [primaryThumbnailUrl, setPrimaryThumbnailUrl] = useState(initialPrimaryThumbnailUrl);
  const [title, setTitle] = useState(initialTitle);
  const [description, setDescription] = useState(initialDescription);
  const [tags, setTags] = useState(initialTags);
  const [visibility, setVisibility] = useState(initialVisibility);
  const autogenThumbnailChoices = (
    (uploadStatus && uploadStatus.autogenThumbnailChoices) ? uploadStatus.autogenThumbnailChoices :
      videoDetail.autogenThumbnailChoices
  );

  React.useEffect(() => {
    if (uploadStatus && uploadStatus.isProcessing) {
      console.debug('Set video thumb from Upload Status');
      setPrimaryThumbnailUrl(uploadStatus.thumbnailImageSmallUrl)
    }
  }, [uploadStatus]);

  React.useEffect(() => {
    console.debug('Set video data from Video Data');
    setPrimaryThumbnailUrl(videoDetail.video.thumbnail_image_small_url);
    setTitle(valueOrEmpty(videoDetail.video.title));
    setDescription(valueOrEmpty(videoDetail.video.description));
    setTags(valueOrEmpty(videoDetail.video.tags));
    setVisibility(valueOrEmpty(videoDetail.video.visibility));
  }, [videoDetail]);

  const debouncedOnFormFieldChange = useCallback(
    debounce((video, data) => onFormFieldChange(video, data), 2000),
    [],
  );

  const handleVisibilityChange = async (e) => {
    onFormFieldChange(videoDetail, { visibility: e.target.name });
  };

  const handleTagsChange = async (e) => {
    const tags = e.target.value;
    const tagsArray = tags.split(',').map((e) => e.trim());
    debouncedOnFormFieldChange(videoDetail, { tags: tagsArray });
    setTags(tags);
  };

  const handleFieldChange = (e, setterFunc) => {
    debouncedOnFormFieldChange(videoDetail, { [e.target.name]: e.target.value });
    setterFunc(e.target.value);
  };

  const handleSaveChangesClicked = async (e) => {
    e.preventDefault();
    onFormFieldChange(videoDetail);
  };

  const handleUploadThumbButtonClick = (e) => {
    e.preventDefault();
    inputThumbnailFile.current.click();
  };

  const handleExistingThumbnailClick = async (e) => {
    const videoRenditionThumbnailId = e.target.dataset.id;
    onSetExistingThumbnailAsPrimary(videoRenditionThumbnailId);
  };

  const renderModal = () => (
    <Modal show={isModalOpen} onShow={() => onModalOpen(videoId)} onHide={onModalClose()}>
      <Form>
        <Modal.Header closeButton>
          {videoDetailForm.isLoading && (<Modal.Title className="w-100"><div className="shine d-block w-75" style={{ height: '30px' }} /></Modal.Title>)}
          {!videoDetailForm.isLoading && (<Modal.Title>Video Details</Modal.Title>)}
        </Modal.Header>
        <Modal.Body>
          {videoDetailForm.isLoading && (
            <div className="row">
              <div className="col-12 col-lg-8">

                <div className="shine d-block w-75 mb-4" style={{ height: '30px' }} />
                <div className="shine d-block w-75 mb-4" style={{ height: '30px' }} />
                <div className="shine thumbnail mb-4" style={{ width: '200px', height: '100px' }} />
                <div className="shine d-block w-75 mb-4" style={{ height: '30px' }} />
                <div className="shine d-block w-75 mb-4" style={{ height: '30px' }} />

              </div>
              <div className="col-12 col-lg-4">
                <div className="card" style={{ width: '18rem' }}>
                  <div
                    className="card-img-top shine d-flex align-items-center justify-content-center"
                    style={{ width: 'auto', height: '171px' }}
                  />
                  <div className="card-body text-secondary bg-light">
                    <p className="card-text">
                      <span className="shine d-block w-100" style={{ height: '20px' }} />
                    </p>
                    <p className="card-text text-truncate">
                      <span className="shine d-block w-100" style={{ height: '20px' }} />
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
          {!videoDetailForm.isLoading && (
            <div className="row">
              <div className="col-12 col-lg-8">

                <Form.Group>
                  <Form.Label>Title</Form.Label>
                  <Form.Control isInvalid={Boolean(videoDetailForm.apiErrors ? videoDetailForm.apiErrors.title : false)} onChange={(e) => handleFieldChange(e, setTitle)} type="text" name="title" value={title} placeholder="Add a title that describes your video." required />
                  <Form.Control.Feedback type="invalid">
                    Please provide a title, up to 500 characters in length.
                  </Form.Control.Feedback>
                </Form.Group>

                <Form.Group>
                  <Form.Label>Description</Form.Label>
                  <Form.Control as="textarea" isInvalid={Boolean(videoDetailForm.apiErrors ? videoDetailForm.apiErrors.description : false)} rows={3} onChange={(e) => handleFieldChange(e, setDescription)} name="description" value={description} placeholder="Tell viewers about your video." />
                </Form.Group>

                <Form.Group>
                  <Form.Label>Thumbnail</Form.Label>
                  <div className="mb-1 text-muted" style={{ fontSize: '0.9em' }}>
                    Select or upload a thumbnail that best shows what's in your video.
                  </div>
                  <div className="thumbnail-grid h-100">
                    <button
                      type="button"
                      onClick={handleUploadThumbButtonClick}
                      className="remove-default-style thumbnail border rounded thumbnail-small d-inline-flex align-items-center justify-content-center mr-2"
                    >
                      <span className="d-flex flex-column text-muted">
                        <i
                          className="material-icons tidy align-middle text-secondary"
                        >add_photo_alternate
                        </i>{uploadThumbnailButtonText}
                      </span>
                    </button>
                    <input type="file" onChange={onInputThumbnailChange} id="custom_thumbnail_image" ref={inputThumbnailFile} className="d-none" />
                    {autogenThumbnailChoices.length > 0 && (
                      <>
                        {!videoDetailForm.isThumbnailUploading && (
                          <button type="button" className="thumbnail thumbnail-small thumbnail-selected mr-2 rounded d-flex align-items-center">
                            <img
                              src={primaryThumbnailUrl}
                              alt="Primary Thumbnail"
                              className="img-fluid h-100"
                            />
                          </button>
                        )}
                        {videoDetailForm.isThumbnailUploading && (
                          <div
                            className="text-muted thumbnail thumbnail-small rounded shine d-inline-flex align-items-center justify-content-center mr-2"
                          />
                        )}
                        <button data-id={autogenThumbnailChoices[0][0]} onClick={(e) => handleExistingThumbnailClick(e)} type="button" className="thumbnail thumbnail-small thumbnail-unselected mr-2 rounded">
                          <img
                            src={autogenThumbnailChoices[0][1]}
                            data-id={autogenThumbnailChoices[0][0]}
                            alt="Thumbnail"
                            className="img-fluid h-100"
                          />
                        </button>
                        <button data-id={autogenThumbnailChoices[1][0]} onClick={(e) => handleExistingThumbnailClick(e)} type="button" className="thumbnail thumbnail-small thumbnail-unselected mr-2 rounded">
                          <img
                            src={autogenThumbnailChoices[1][1]}
                            data-id={autogenThumbnailChoices[1][0]}
                            alt="Thumbnail"
                            className="img-fluid h-100"
                          />
                        </button>
                        <button data-id={autogenThumbnailChoices[2][0]} onClick={(e) => handleExistingThumbnailClick(e)} type="button" className="thumbnail thumbnail-small thumbnail-unselected rounded">
                          <img
                            src={autogenThumbnailChoices[2][1]}
                            data-id={autogenThumbnailChoices[2][0]}
                            alt="Thumbnail"
                            className="img-fluid h-100"
                          />
                        </button>
                      </>
                    )}
                    {autogenThumbnailChoices.length === 0
                      && (
                        <>
                          <div
                            className="text-muted thumbnail thumbnail-small rounded shine d-inline-flex align-items-center justify-content-center mr-2"
                          />
                          <div
                            className="text-muted thumbnail thumbnail-small rounded shine d-inline-flex align-items-center justify-content-center mr-2"
                          />
                          <div
                            className="text-muted thumbnail thumbnail-small rounded shine d-inline-flex align-items-center justify-content-center mr-2"
                          />
                          <div
                            className="text-muted thumbnail thumbnail-small rounded shine d-inline-flex align-items-center justify-content-center"
                          />
                        </>
                      )}
                  </div>

                </Form.Group>

                <Form.Group>
                  <Form.Label>Visibility</Form.Label>
                  <div className="custom-control custom-radio">
                    <Form.Check
                      type="radio"
                      id="public"
                      name="public"
                      label="Public"
                      checked={visibility === 'public'}
                      onChange={handleVisibilityChange}
                      style={{ paddingLeft: 0 }}
                    />
                  </div>

                  <div className="custom-control custom-radio">
                    <Form.Check
                      type="radio"
                      id="private"
                      name="private"
                      label="Private"
                      checked={visibility === 'private'}
                      onChange={handleVisibilityChange}
                      style={{ paddingLeft: 0 }}
                    />
                  </div>
                </Form.Group>

                <Form.Group>
                  <Form.Label>Tags</Form.Label>
                  <Form.Control isInvalid={Boolean(videoDetailForm.apiErrors ? videoDetailForm.apiErrors.tags : false)} onChange={(e) => handleTagsChange(e)} type="text" name="tags" value={tags} placeholder="Up to 3 tags to describe your video." />
                  <div className="mt-1 mx-2 text-muted" style={{ fontSize: '0.9em' }}>Enter a comma after each tag.</div>
                  <Form.Control.Feedback type="invalid">
                    Please provide some tags.
                  </Form.Control.Feedback>
                </Form.Group>

              </div>
              <div className="col-12 col-lg-4">

                <div className="card ml-0 ml-lg-auto" style={{ width: '18rem' }}>
                  {isUploading && (
                    <div
                      className="thumbnail thumbnail-medium w-100 shine d-flex align-items-center justify-content-center"
                    >
                      Uploading video…
                    </div>
                  )}
                  {!isUploading && videoDetailForm.isThumbnailUploading && (
                    <div
                      className="thumbnail thumbnail-medium w-100 shine d-flex align-items-center justify-content-center"
                    >
                      Uploading thumbnail...
                    </div>
                  )}
                  {!isUploading && primaryThumbnailUrl && !videoDetailForm.isThumbnailUploading && (
                    <div
                      className="thumbnail thumbnail-medium w-100 d-flex align-items-center justify-content-center"
                      style={{ width: 'auto', height: '171px' }}
                    >
                      <img src={primaryThumbnailUrl} alt="" className="img-fluid h-100" />
                    </div>
                  )}
                  <div className="card-body text-secondary bg-light">
                    <p className="card-text">Video link<br />
                      <a
                        href={`${window.SITE_BASE_URL}/v/${videoId}`}
                      >{`${window.SITE_BASE_URL}/v/${videoId}`}
                      </a>
                    </p>
                    <p className="card-text text-truncate">Filename<br />
                      <span
                        className="text-dark"
                      >{filename}
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          )}
        </Modal.Body>
        <Modal.Footer className="bg-secondary text-muted">
          {videoDetailForm.isLoading && (
            <div className="shine d-block w-10 mr-auto" style={{ height: '30px' }} />
          )}
          {!videoDetailForm.isLoading && (
            <>
              {!isUploading && (<div className="mr-auto">{statusText}</div>)}
              {isUploading && (
                <div className="mr-auto d-flex align-items-center w-75">
                  <div className="mr-2">{statusText}</div>
                  <div className="progress w-25">
                    <div className="progress-bar progress-bar-striped progress-bar-animated"
                      role="progressbar" style={{ width: `${uploadStatus.percentageUploaded}%` }} aria-valuenow={uploadStatus.percentageUploaded} aria-valuemin="0"
                      aria-valuemax="100">{uploadStatus.percentageUploaded}%</div>
                  </div></div>)}
              <button onClick={handleSaveChangesClicked} type="submit" className="btn btn-primary">{saveButtonText}</button>
            </>
          )}
        </Modal.Footer>
      </Form>
    </Modal>
  );

  return (
    <>
      {renderModal()}
    </>
  );
};

export default VideoDetailModal;
