import React, { useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Toast from 'react-bootstrap/Toast';

import 'regenerator-runtime/runtime.js';

export const CreateChannelButton = ({
  onCreateChannel,
}) => {
  const [showChannelModal, setShowChannelModal] = useState(false);
  const [apiErrors, setApiErrors] = useState({});

  const [channelName, setChannelName] = useState('');
  const [channelDescription, setChannelDescription] = useState('');
  const [primaryFormError, setPrimaryFormError] = useState('');
  const [isChannelSynced, setIsChannelSynced] = useState(false);
  const [validated, setValidated] = useState(false);
  const [showToast, setShowToast] = useState(false);

  const createChannelHandler = async (e) => {
    const form = e.currentTarget;
    e.preventDefault();

    if (form.checkValidity() === false) {
      e.stopPropagation();
      setValidated(true);
      return;
    }
    const [isChannelCreated, apiErrors_] = await onCreateChannel(
      channelName, channelDescription, isChannelSynced,
    );
    if (isChannelCreated) {
      setShowToast(true);
      setShowChannelModal(false);
    } else {
      setApiErrors(apiErrors_);
      setPrimaryFormError('Please correct the form errors shown above and resubmit.');
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

            <Form.Group controlId="exampleForm.ControlTextarea1">
              <Form.Label>Channel Description</Form.Label>
              <Form.Control isInvalid={Boolean(apiErrors ? apiErrors.description : false)} onChange={(e) => setChannelDescription(e.target.value)} name="description" as="textarea" rows={4} placeholder="Tell viewers about your channel. Your description will appear in the About section of your channel and search results, among other places." />
              <Form.Control.Feedback type="invalid">{apiErrors ? apiErrors.description : ''}</Form.Control.Feedback>
            </Form.Group>

            <Form.Group controlId="formBasicCheckbox">
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

  const renderToast = () => (
    <div
      aria-live="polite"
      aria-atomic="true"
      style={{
        position: 'fixed',
        top: '0',
        right: '0',
        height: '2px',
        width: '100%',
        zIndex: '9999',
      }}
    >
      <Toast
        style={{
          position: 'absolute',
          top: 20,
          right: 20,
        }}
        show={showToast}
        autohide
        onClose={() => setShowToast(!showToast)}
      >
        <Toast.Header>
          <strong className="mr-auto">Success</strong>
        </Toast.Header>
        <Toast.Body>Your new channel has been created.</Toast.Body>
      </Toast>
    </div>
  );

  return (
    <>
      <div>
        <a onClick={() => setShowChannelModal(true)} className="mt-2 btn btn-outline-secondary">
          <i className="material-icons align-middle">add_circle_outline</i> Create Channel
        </a>
      </div>
      {renderModal()}
      {renderToast()}
    </>
  );
};

export default CreateChannelButton;
