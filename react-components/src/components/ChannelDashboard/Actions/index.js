import React from 'react';
import ReactDOM from 'react-dom'

// Redux
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

// Components
import ChannelCreate from './ChannelCreate';

// api
import { createChannel } from '../../../api/api';

// Styling

export const actions = ({
  element,
  ...params
}) => {

  const handleCreateChannel = (name, desc, bSync) => {
    // TODO: Set active channel and store ID. If bSync then enable correct tab
    createChannel(name, desc, bSync);
  };

  const DashContainer = () => {
    return (
      <ChannelCreate onCreateChannel={handleCreateChannel} />
    );
  };

  return (
    ReactDOM.render(<DashContainer {...params} />, element)
  );
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({}, dispatch),
  };
};

export default connect(null, mapDispatchToProps)(actions);
