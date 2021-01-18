import React from 'react';
import styled from 'styled-components';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

import "regenerator-runtime/runtime.js";

// Styling
export const StyledLink = styled.a`
    color: #fff !important;
`; // Bootstrap is overriding color here so having to use !important. Needs investigation.

export const SyncChannelButton = ({
  bModalOpen,
  onModalClose,
  onSyncChannel,
}) => {

  const syncHandler = () => {
    // Todo: Add some warnings to form validation
    onSyncChannel();
    onModalClose()
  };

  const renderModal = () => {
    return (
      <>
        <Modal show={bModalOpen} onHide={onModalClose()}>
        <Form>

          <Modal.Header closeButton>
            <Modal.Title>Create a channel</Modal.Title>
          </Modal.Header>
                
           <Modal.Body>

              <Form.Group>
                <Form.Label>Channel Name</Form.Label>
              </Form.Group>

              <Form.Group controlId="exampleForm.ControlTextarea1">
                <Form.Label>Channel Description</Form.Label>
              </Form.Group>

              <Form.Group controlId="formBasicCheckbox">
                <a href="#">Learn more about channel syncing</a>
              </Form.Group>

            </Modal.Body>

            <Modal.Footer>
              <button onClick={onModalClose()} type="button" className="btn btn-light">Cancel</button>
              <a href="#" onClick={() => createChannelHandler()} className="btn btn-primary">Create Channel</a>
            </Modal.Footer>

          </Form>
        </Modal>
      </>
    )
  };

  return (
    <>
      <h2 className="h5 ">Sync Status</h2>
      <StyledLink onClick={() => setShowSyncModal(true)} className="btn btn-primary ml-auto">Add YouTube Channel</StyledLink>
      {renderModal()}
    </>
  );

};

export default SyncChannelButton;


