import React, { useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

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
  const [channelSync, setChannelSync] = useState(false);

  const createChannelHandler = () => {
    setShowChannelModal(false);
    // Todo: Add some warnings to form validation for failed create.
    onCreateChannel(channelName, channelDescription, channelSync);
  };

  const renderModal = () => {
    return (
      <>
        <Modal show={showChannelModal} onHide={() => setShowChannelModal(false)}>
        <Form>

          <Modal.Header closeButton>
            <Modal.Title>Create a channel</Modal.Title>
          </Modal.Header>
                
           <Modal.Body>

              <Form.Group>
                <Form.Label>Channel Name</Form.Label>
                <Form.Control onChange={e => setChannelName(e.target.value)} type="text" placeholder={channelName} />
              </Form.Group>

              <Form.Group controlId="exampleForm.ControlTextarea1">
                <Form.Label>Channel Description</Form.Label>
                <Form.Control onChange={e => setChannelDescription(e.target.value)} as="textarea" rows={3} placeholder={'Tell viewers about your channel. Your description will appear in the About section of your channel and search results, among other places.'} />
              </Form.Group>

              <Form.Group controlId="formBasicCheckbox">
                <Form.Check onChange={e => {setChannelSync(e.target.value === 'on' ? true : false)}} type="checkbox" label="I'd like to sync videos from my YouTube Channel." />
                <a href="#">Learn more about channel syncing</a>
              </Form.Group>

            </Modal.Body>

            <Modal.Footer>
              <button onClick={() => setShowChannleModal(false)} type="button" className="btn btn-light">Cancel</button>
              <a href="#" onClick={() => createChannelHandler()} className="btn btn-primary">Create Channel</a>
            </Modal.Footer>

          </Form>
        </Modal>
      </>
    )
  };

  return (
    <>
      <div><a onClick={() => setShowChannelModal(true)} className="mt-2 btn btn-outline-secondary"><i className="material-icons align-middle">add_circle_outline</i> Create Channel</a></div>
      {renderModal()}
    </>
  );

};

export default CreateChannelButton;


