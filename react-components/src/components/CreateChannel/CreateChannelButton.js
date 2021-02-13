import React, { useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import { MSG_CORRECT_FORM_ERRORS } from '../../constants';
import 'regenerator-runtime/runtime.js';

export const CreateChannelButton = ({
  onCreateChannel,
  onSuccess,
}) => {
  const [showChannelModal, setShowChannelModal] = useState(false);
  const [apiErrors, setApiErrors] = useState({});

  const [channelName, setChannelName] = useState('');
  const [channelDescription, setChannelDescription] = useState('');
  const [primaryFormError, setPrimaryFormError] = useState('');
  const [isChannelSynced, setIsChannelSynced] = useState(false);
  const [validated, setValidated] = useState(false);

  const createChannelHandler = async (e) => {
    const form = e.currentTarget;
    e.preventDefault();

    if (form.checkValidity() === false) {
      e.stopPropagation();
      setValidated(true);
      return;
    }
    onSuccess();
    const [isChannelCreated, apiErrors_] = await onCreateChannel(
      channelName, channelDescription, isChannelSynced,
    );
    if (isChannelCreated) {
      setShowChannelModal(false);
    } else {
      setApiErrors(apiErrors_);
      setPrimaryFormError(MSG_CORRECT_FORM_ERRORS);
    }
  };

  const renderModal = () => (
    <>
      <Modal show={showChannelModal} onHide={() => setShowChannelModal(false)}>
        <Form onSubmit={(e) => createChannelHandler(e)} noValidate validated={validated}>
          <Modal.Header closeButton>
            <Modal.Title>Create a channel</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <Form.Group>
              <Form.Label>Channel Name</Form.Label>
              <Form.Control isInvalid={Boolean(apiErrors ? apiErrors.name : false)} onChange={(e) => setChannelName(e.target.value)} name="name" type="text" placeholder="My Awesome Channel" required />
              <Form.Control.Feedback type="invalid">{apiErrors ? apiErrors.name : ''}</Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="control_description">
              <Form.Label>Channel Description</Form.Label>
              <Form.Control isInvalid={Boolean(apiErrors ? apiErrors.description : false)} onChange={(e) => setChannelDescription(e.target.value)} name="description" as="textarea" rows={4} placeholder="Tell viewers about your channel. Your description will appear in the About section of your channel and search results, among other places." />
              <Form.Control.Feedback type="invalid">{apiErrors ? apiErrors.description : ''}</Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="control_sync_videos_interested">
              <Form.Check checked={isChannelSynced} onChange={() => setIsChannelSynced(!isChannelSynced)} type="checkbox" id="sync_videos_interested" name="sync_videos_interested" label={<><label htmlFor="sync_videos_interested">I'd like to sync videos from my YouTube Channel. </label> <a href="#"> Learn more about channel syncing</a></>} />
            </Form.Group>
            <p className="text-muted">
              By clicking "Create channel", you agree to our <a href="#">Terms of Service</a>.
            </p>
          </Modal.Body>

          <Modal.Footer>
            <p className="text-danger">
              {primaryFormError}
            </p>
            <button onClick={() => setShowChannelModal(false)} type="button" className="btn btn-light">Cancel</button>
            <button type="submit" className="btn btn-primary">Create Channel</button>
          </Modal.Footer>

        </Form>
      </Modal>
    </>
  );

  return (
    <>
      <div>
        <a onClick={() => setShowChannelModal(true)} className="mt-2 btn btn-outline-secondary">
          <i className="material-icons align-middle">add_circle_outline</i> Create Channel
        </a>
      </div>
      {renderModal()}
    </>
  );
};

export default CreateChannelButton;
