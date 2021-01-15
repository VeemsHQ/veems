import React from 'react';
import ReactDOM from 'react-dom'

// Redux
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

// Components
import CreateChannelButton from './CreateChannelButton';

// api
import { createChannelRequest } from '../../api/api';

// Styling


/* Entry point for DOM element render and subsequent button render.
This only deal with the above and handling API requests. The CreateChannel
component will manage logic.
*/
export const CreateChannel = ({
  element,
  ...params
}) => {

  const handleCreateChannel = (name, desc, bSync) => {
    // TODO: Set active channel and store ID. 
    createChannelRequest(name, desc, bSync);
    // If bSync then enable correct tab
    if (bSync)
      window.location.pathname = '/channel/sync/';
  };

  const ButtonContainer = () => {
    return (
      <CreateChannelButton onCreateChannel={handleCreateChannel} />
    );
  };

  return (
    ReactDOM.render(<ButtonContainer {...params} />, element)
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({}, dispatch),
  };
};

export default connect(null, mapDispatchToProps)(CreateChannel);