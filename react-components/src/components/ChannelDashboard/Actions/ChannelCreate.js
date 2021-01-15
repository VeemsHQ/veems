import React, { useState } from 'react';
import Modal from 'react-bootstrap/Modal';
import "regenerator-runtime/runtime.js";

// Styling
/* Todo: Move all embedded css into here so we can properly pass and use props
  and remove all ugly className syntax.
*/

export const ChannelCreate = ({
  onChannelCreate,
}) => {
  const [showChannelModal, setShowChannelModal] = useState(false);

  const [channelName, setChannelName] = useState('My Awesome Channel');
  const [channelDescription, setChannelDescription] = useState('Tell viewers about your channel. Your description will appear in the About section of your channel and search results, among other places.');
  const [channelSync, setChannelSync] = useState(false);

  const createChannelHandler = () => {
    setShowChannelModal(false);
    // Todo: Add some warnings to form validation for failed create.
    onChannelCreate(channelName, channelDescription, channelSync);
  };

  const renderModal = () => {
    return (
      <>
        <Modal show={showChannelModal} onHide={() => setShowChannelModal(false)}>
          <Modal.Header closeButton>
            <Modal.Title>Create a channel</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div className="form-group">
                <label>Channel Name</label>
                <input placeholder={channelName} onInput={e => setChannelName(e.target.value)} type="text" className="form-control" id="customInput2"
                    placeholder="My Awesome Channel" />
            </div>
            <div className="form-group">
                <label>Channel Description</label>
                <textarea placeholder={channelDescription} onInput={e => setChannelDescription(e.target.value)} className="form-control" rows="3" id="customTextArea2"></textarea>
            </div>
            <div className="form-group">
                <div className="custom-control custom-checkboxWW">
                    <input onChange={e => {setChannelSync(e.target.value)}} type="checkbox" className="custom-control-input" id="customCheck2" />
                    <label className="custom-control-label d-flex">I'd like to sync videos
                        from my YouTube Channel.</label><a href="#">Learn more about channel syncing</a>.
                </div>
            </div>
            <p className="text-muted">
                By clicking "Create channel", you agree to our <a href="#">Terms of Service</a>.
            </p>
          </Modal.Body>
          <Modal.Footer>
                <button onClick={() => setShowChannleModal(false)} type="button" className="btn btn-light">Cancel</button>
                <a href="#" onClick={() => createChannelHandler()} className="btn btn-primary">Create Channel</a>
          </Modal.Footer>
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

export default ChannelCreate;