import React, { useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { valueOrEmpty } from '../../utils';

import 'regenerator-runtime/runtime.js';

export const DeleteVideoButton = ({
  isSaving,
  isModalOpen,
  onModalClose,
  onModalOpen,
  onDelete,
  isLoading,
  videoData,
}) => {
  const deleteButtonText = isSaving ? 'Deleting...' : 'Delete forever';
  const videoId = valueOrEmpty(videoData.id);
  const initialTitle = valueOrEmpty(videoData.title);
  const initialCreatedDate = valueOrEmpty(videoData.created_date_human);
  const primaryThumbnailUrl = videoData.thumbnail_image_medium_url;
  const [videoCreatedDate, setVideoCreatedDate] = useState(initialCreatedDate);
  const [videoTitle, setTitle] = useState(initialTitle);
  const [isCheckboxUnderstoodChecked, setIsCheckboxUnderstoodChecked] = useState(false);

  React.useEffect(() => {
    setTitle(initialTitle);
    setVideoCreatedDate(initialCreatedDate);
  }, [initialTitle, initialCreatedDate]);

  const renderModal = () => (
    <>
      {isLoading && (
        <Modal size="lg" show={isModalOpen} onHide={onModalClose()}>
          <Form>

            <Modal.Header closeButton>
              <Modal.Title className="w-100"><div className="shine d-block w-75" style={{ height: '30px' }} /></Modal.Title>
            </Modal.Header>

            <Modal.Body>
              <div className="shine thumbnail mb-4" style={{ width: '300px', height: '100px' }} />
              <div className="shine d-block w-50 mb-4" style={{ height: '30px' }} />

            </Modal.Body>

            <Modal.Footer>
              <div className="shine d-block w-10 mr-auto" style={{ height: '30px' }} />
            </Modal.Footer>

          </Form>
        </Modal>
      )}
      {!isLoading && (
      <Modal size="lg" show={isModalOpen} onHide={onModalClose()}>
        <Form>

          <Modal.Header closeButton>
            <Modal.Title>Permanently delete this video?</Modal.Title>
          </Modal.Header>

          <Modal.Body>
            <div className="d-inline-flex mb-3 bg-secondary text-muted p-4">
              <a href={`/v/${videoId}`} className="thumbnail thumbnail-small d-inline-block mr-2">
                <img className="card-img-top w-100" src={primaryThumbnailUrl} alt={videoTitle} />
              </a>
              <div className="metadata-container d-flex">
                <div className="content p-2">
                  <h5 className="m-0 mb-1">{videoTitle}</h5>
                  <div className="metadata">
                    <div className="card-text text-muted text-wrap text-truncate">
                      Uploaded on {videoCreatedDate}
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <Form.Group controlId="double_check">
              <Form.Check type="checkbox" label="I understand that deleting is permanent, and can't be undone" checked={isCheckboxUnderstoodChecked} onChange={() => setIsCheckboxUnderstoodChecked(!isCheckboxUnderstoodChecked)} />
            </Form.Group>
          </Modal.Body>

          <Modal.Footer>
            <button type="button" className="btn btn-primary" onClick={onModalClose()}>Cancel</button>
            <button type="submit" className="btn btn-light" onClick={onDelete()} disabled={!isCheckboxUnderstoodChecked}>{deleteButtonText}</button>
          </Modal.Footer>

        </Form>
      </Modal>
      )}
    </>
  );

  return (
    <>
      <button type="button" onClick={onModalOpen()} className="btn"><i className="material-icons text-secondary">delete</i></button>
      {renderModal()}
    </>
  );
};

export default DeleteVideoButton;
