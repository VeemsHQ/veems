import React, { useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Toast from 'react-bootstrap/Toast';

import "regenerator-runtime/runtime.js";

// Styling
/* Todo: Move all embedded css into here so we can properly pass and use props
  and remove all ugly className syntax.
*/

export const CreateChannelButton = ({
  onCreateChannel,
}) => {
  const [showChannelModal, setShowChannelModal] = useState(false);

  const [channelName, setChannelName] = useState('');
  const [channelDescription, setChannelDescription] = useState('');
  const [channelWarning, setChannelWarning] = useState('');
  const [channelSync, setChannelSync] = useState(false);
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
    const isChannelCreated = await onCreateChannel(channelName, channelDescription, channelSync);
    if (isChannelCreated) {
      setShowChannelModal(false);
      // Show toast success.
      setShowToast(true);
    } else {
      setChannelWarning('Sorry, it looks like something has gone wrong.');
    }
  };

  const renderModal = () => {
    return (
      <>
        <Modal show={showChannelModal} onHide={() => setShowChannelModal(false)}>
        <Form onSubmit={(e) => createChannelHandler(e)} noValidate validated={validated}>

          <Modal.Header closeButton>
            <Modal.Title>Create a channel</Modal.Title>
          </Modal.Header>
                
           <Modal.Body>

              <Form.Group>
                <Form.Label>Channel Name</Form.Label>
                <Form.Control onChange={e => setChannelName(e.target.value)} type="text" placeholder={'My Awesome Channel'} required />
                <Form.Control.Feedback type="invalid">
                  Please provide a channel name.
                </Form.Control.Feedback>
              </Form.Group>

              <Form.Group controlId="exampleForm.ControlTextarea1">
                <Form.Label>Channel Description</Form.Label>
                <Form.Control required onChange={e => setChannelDescription(e.target.value)} as="textarea" rows={4} placeholder={'Tell viewers about your channel. Your description will appear in the About section of your channel and search results, among other places.'} />
                <Form.Control.Feedback type="invalid">
                  Please provide a channel description.
                </Form.Control.Feedback>
              </Form.Group>

              <Form.Group controlId="formBasicCheckbox">
                <Form.Check onChange={e => {setChannelSync(e.target.value === 'on' ? true : false)}} type="checkbox" label={<><label>I'd like to sync videos from my YouTube Channel. </label> <a href='#'> Learn more about channel syncing</a></>} />
              </Form.Group>
              <p className="text-muted">
                By clicking "Create channel", you agree to our <a href="#">Terms of Service</a>.
              </p>
            </Modal.Body>
            
            <Modal.Footer>
              <p className="text-danger">
                {channelWarning}
              </p>
              <button onClick={() => setShowChannelModal(false)} type="button" className="btn btn-light">Cancel</button>
              <button type="submit" className="btn btn-primary">Create Channel</button>
            </Modal.Footer>

          </Form>
        </Modal>
      </>
    )
  };

  const renderToast = () => {
    return (
      <div
        aria-live="polite"
        aria-atomic="true"
        style={{
          position: 'fixed',
          bottom: '0',
          right: '0',
          padding: '20px',
          margin: '20px',
          width: '100%',
          zIndex: '9999',
        }}
      >
        <Toast
          style={{
            position: 'absolute',
            padding: '20px',
            bottom: 0,
            right: 0,
          }}
          show={showToast}
          autohide={true}
          onClose={() => setShowToast(!showToast)}
        >
          <Toast.Header>
            Success
          </Toast.Header>
          <Toast.Body>Created Channel: {channelName}</Toast.Body>
        </Toast>
      </div>
    )
  }

  return (
    <>
      <div><a onClick={() => setShowChannelModal(true)} className="mt-2 btn btn-outline-secondary"><i className="material-icons align-middle">add_circle_outline</i> Create Channel</a></div>
      {renderModal()}
      {renderToast()}
    </>
  );

};

export default CreateChannelButton;


