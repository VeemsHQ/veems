import React, { useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import 'regenerator-runtime/runtime.js';

const valueOrEmpty = (value) => ((value !== undefined && value !== null) ? value : '');

const randomItem = (choices) => {
  const index = Math.floor(Math.random() * choices.length);
  return choices[index];
};

export const EditVideoButton = ({
  isSaving,
  isModalOpen,
  onModalClose,
  onModalOpen,
  isLoading,
  videoData,
  handleChange,
}) => {
  console.log('btn render');
  const [title2, setTitle] = useState('');
  const [description2, setDescription] = useState('');
  const [tags2, setTags] = useState('');
  const [visibility2, setVisibility] = useState('public');

  const videoId = valueOrEmpty(videoData.id);
  const title = valueOrEmpty(videoData.title);
  const description = valueOrEmpty(videoData.description);
  const tags = valueOrEmpty(videoData.tags);
  const visibility = valueOrEmpty(videoData.visibility);
  const primaryThumbnailUrl = videoData.thumbnail_image_medium_url;

  // Find ideal thumbnails to display given available at that time.
  let renditionThumbnails = [];
  if (videoData.video_renditions && videoData.video_renditions.length > 0) {
    renditionThumbnails = videoData.video_renditions.map(
      (r) => r.rendition_thumbnails.map((t) => t.file)[0],
    );
  }
  const onVisibilityChange = async (e) => {
    handleChange({ visibility: e.target.name });
  };

  const renderModal = () => (
    <>
      {isLoading && (
        <Modal show={isModalOpen} onHide={onModalClose()}>
          <Form>

            <Modal.Header closeButton>
              <Modal.Title className="w-100"><div className="shine d-block w-75" style={{ height: '30px' }} /></Modal.Title>
            </Modal.Header>

            <Modal.Body>
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
            </Modal.Body>

            <Modal.Footer className="bg-secondary text-muted">
              <div className="shine d-block w-10 mr-auto" style={{ height: '30px' }} />
            </Modal.Footer>

          </Form>
        </Modal>
      )}
      {!isLoading && (
      <Modal show={isModalOpen} onHide={onModalClose()}>
        <Form>

          <Modal.Header closeButton>
            <Modal.Title>Video Details {isSaving && 'Saving...'}</Modal.Title>
          </Modal.Header>

          <Modal.Body>
            <div className="row">
              <div className="col-12 col-lg-8">

                <Form.Group>
                  <Form.Label>Title</Form.Label>
                  <Form.Control onChange={(e) => setTitle(e.target.value)} type="text" value={title} placeholder="Add a title that describes your video." required />
                  <Form.Control.Feedback type="invalid">
                    Please provide a title.
                  </Form.Control.Feedback>
                </Form.Group>

                <Form.Group controlId="exampleForm.ControlTextarea1">
                  <Form.Label>Description</Form.Label>
                  <Form.Control as="textarea" rows={3} onChange={(e) => setDescription(e.target.value)} value={description} placeholder="Tell viewers about your video." />
                </Form.Group>

                <Form.Group>
                  <Form.Label>Thumbnail</Form.Label>
                  <div className="mb-1 text-muted" style={{ fontSize: '0.9em' }}>Select or upload a thumbnail that best shows what's in your video.</div>
                  <div className="thumbnail-grid h-100">
                    <button
                      type="button"
                      className="remove-default-style thumbnail border rounded thumbnail-small d-inline-flex align-items-center justify-content-center mr-2"
                    >
                      <span className="d-flex flex-column text-muted">
                        <i
                          className="material-icons tidy align-middle text-secondary"
                        >add_photo_alternate
                        </i>Upload thumbnail
                      </span>
                    </button>
                    {renditionThumbnails.length > 0 && (
                      <>
                        <div className="thumbnail thumbnail-small mr-2 rounded">
                          <img
                            src={randomItem(renditionThumbnails)}
                            alt=""
                            className="img-fluid h-100"
                          />
                        </div>
                        <div className="thumbnail thumbnail-small thumbnail-unselected mr-2 rounded">
                          <img
                            src={randomItem(renditionThumbnails)}
                            alt=""
                            className="img-fluid h-100"
                          />
                        </div>
                        <div className="thumbnail thumbnail-small thumbnail-unselected mr-2 rounded">
                          <img
                            src={randomItem(renditionThumbnails)}
                            alt=""
                            className="img-fluid h-100"
                          />
                        </div>
                        <div className="thumbnail thumbnail-small thumbnail-unselected rounded">
                          <img
                            src={randomItem(renditionThumbnails)}
                            alt=""
                            className="img-fluid h-100"
                          />
                        </div>
                      </>
                    )}
                    {renditionThumbnails.length === 0
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
                      onChange={onVisibilityChange}
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
                      onChange={onVisibilityChange}
                      style={{ paddingLeft: 0 }}
                    />
                  </div>
                </Form.Group>

                <Form.Group>
                  <Form.Label>Tags</Form.Label>
                  <Form.Control onChange={(e) => setTags(e.target.value)} type="text" value={tags} placeholder="Up to 3 tags to describe your video." />
                  <div className="mt-1 mx-2 text-muted" style={{ fontSize: '0.9em' }}>Enter a comma after each tag.</div>
                  <Form.Control.Feedback type="invalid">
                    Please provide some tags.
                  </Form.Control.Feedback>
                </Form.Group>

              </div>
              <div className="col-12 col-lg-4">

                <div className="card" style={{ width: '18rem' }}>
                  {!primaryThumbnailUrl && (
                    <div
                      className="card-img-top shine d-flex align-items-center justify-content-center"
                    >
                      Uploading video…
                    </div>
                  )}
                  {primaryThumbnailUrl && (
                    <div
                      className="card-img-top d-flex align-items-center justify-content-center"
                      style={{ width: 'auto', height: '171px' }}
                    >
                      <img src={primaryThumbnailUrl} alt="" className="img-fluid w-100 h-100" />
                    </div>
                  )}
                  <div className="card-body text-secondary bg-light">
                    <p className="card-text">Video link<br />
                      <a
                        href={`https://veems.com/v/${videoId}`}
                      >{`https://veems.com/v/${videoId}`}
                      </a>
                    </p>
                    <p className="card-text text-truncate">Filename<br />
                      <span
                        className="text-dark"
                      >uploadingFileName.mp4
                      </span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </Modal.Body>

          <Modal.Footer className="bg-secondary text-muted">
            <div className="mr-auto">Status: Uploaded &amp; Processing</div>
          </Modal.Footer>

        </Form>
      </Modal>
      )}
    </>
  );

  return (
    <>
      <a href="#" onClick={onModalOpen()} className="btn"><i className="material-icons text-secondary">create</i></a>
      {renderModal()}
    </>
  );
};

export default EditVideoButton;
