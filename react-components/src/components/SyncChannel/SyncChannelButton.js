import React, { useState } from 'react';
import styled from 'styled-components';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import "regenerator-runtime/runtime.js";

// Styling
export const StyledLink = styled.a`
    color: #fff !important;
`; // Bootstrap is overriding color here so having to use !important. Needs investigation.

export const SyncChannelButton = ({
  isModalOpen,
  onModalClose,
  onModalOpen,
  onSyncChannel,
}) => {
  const [channelName, setChannelName] = useState('');

  const syncHandler = (e) => {
    // e.preventDefault();
    // Todo: Add some warnings to form validation
    onSyncChannel();
    onModalClose()
  };

  const renderModal = () => {
    return (
      <>
        <Modal show={isModalOpen} onHide={onModalClose()}>
        <Form>

          <Modal.Header closeButton>
            <Modal.Title>Sync a channel</Modal.Title>
          </Modal.Header>
                
           <Modal.Body>

              <Form.Group>
                <Form.Label>Your Veems Channel Name</Form.Label>
                <Form.Control onChange={e => setChannelName(e.target.value)} type="text" placeholder={'Veems Channel Name'} required />
                <div className="mt-1 mx-2 text-muted" style={{fontSize: "0.9em"}}>This will be the public display
                                name for your channel.</div>
                <div className="mt-1 mx-2 text-muted" style={{fontSize: "0.9em"}}>Channel names cannot be changed
                    once chosen, please be extra careful.</div>
                <Form.Control.Feedback type="invalid">
                  Please provide a channel name.
                </Form.Control.Feedback>
              </Form.Group>

              <Form.Group>
                <Form.Label>Your YouTube Channel Link</Form.Label>
                <Form.Control onChange={e => setChannelName(e.target.value)} type="text" placeholder={'https://www.youtube.com/channel/...'} required />
                <Form.Control.Feedback type="invalid">
                  Please provide YouTube channel link.
                </Form.Control.Feedback>
              </Form.Group>

              <Form.Group controlId="formBasicCheckbox">
                <Form.Check type="checkbox" label={'I have permission to re-distribute content from this YouTube Channel.'} />
              </Form.Group>

              <Form.Group controlId="formBasicCheckbox1">
                <Form.Check type="checkbox" label={<><label>I want to sync my YouTube
                                    content to Veems and agree to </label> <a href='#'> these terms</a><label>. I have also read and understand <a href='#'> how the program works</a>.</label></>} />
              </Form.Group>

            </Modal.Body>

            <Modal.Footer>
              <button onClick={onModalClose()} type="button" className="btn btn-light">Cancel</button>
              <a href="#" className="btn btn-primary">Sync Channel</a>
            </Modal.Footer>

          </Form>
        </Modal>
      </>
    )
  };

  return (
    <>
      <h2 className="h5 ">Sync Status</h2>
      <StyledLink onClick={onModalOpen(true)} className="btn btn-primary ml-auto">Add YouTube Channel</StyledLink>
      {renderModal()}
    </>
  );

};

export default SyncChannelButton;


