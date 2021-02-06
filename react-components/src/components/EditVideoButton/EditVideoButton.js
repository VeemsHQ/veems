import React, { useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import 'regenerator-runtime/runtime.js';

export const EditVideoButton = ({
  isModalOpen,
  onModalClose,
  onModalOpen,
  isLoading,
}) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [tags, setTags] = useState('');
  const [visibility, setVisibility] = useState('public');

  const onVisibilityChange = (e) => {
    setVisibility(e.target.id);
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
                        <div className="shine d-block w-100" style={{ height: '20px' }} />
                      </p>
                      <p className="card-text text-truncate">
                        <div className="shine d-block w-100" style={{ height: '20px' }} />
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
            <Modal.Title>Video Details</Modal.Title>
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

                  <div className="thumbnail-grid d-flex align-items-around h-100 border rounded">
                    <button
                      type="button"
                      className="remove-default-style thumbnail d-inline-flex w-100 align-items-center justify-content-center"
                    >
                      <span>
                        <i
                          className="material-icons tidy align-middle text-secondary"
                        >add_photo_alternate
                        </i>Upload thumbnail
                      </span>
                    </button>
                    <div className="bg-secondary thumbnail">
                      <img
                        src="https://i.ytimg.com/vi/pJkgymyv0_s/hq720.jpg?sqp=-oaymwEZCNAFEJQDSFXyq4qpAwsIARUAAIhCGAFwAQ==&rs=AOn4CLCfMf5cCfG3GSPEB1LkYOuXFvgkOw"
                        className="img-fluid h-100"
                      />
                    </div>
                    <div
                      className="thumbnail thumbnail-generating w-100 shine d-inline-flex align-items-center justify-content-center"
                    >
                      Auto-generating...
                    </div>
                  </div>

                </Form.Group>

                <Form.Group>
                  <Form.Label>Visibility</Form.Label>
                  <div className="custom-control custom-radio">
                    <Form.Check
                      type="radio"
                      id="public"
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
                  <div
                    className="card-img-top shine d-flex align-items-center justify-content-center"
                    style={{ width: 'auto', height: '171px' }}
                  >
                    Uploading video…
                  </div>
                  <div className="card-body text-secondary bg-light">
                    <p className="card-text">Video link<br />
                      <a
                        href="https://veems.com/v/UCASvHD"
                      >https://veems.com/v/UCASvHD
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
