import React from 'react';
import PropTypes from 'prop-types';

import 'regenerator-runtime/runtime.js';

export const SelectChannelDropdown = ({
  onSelectChannel,
  activeID,
  channels,
}) => {
  const renderDropdown = () => (
    <>
      <select
        value={activeID}
        onChange={onSelectChannel}
        className="custom-select custom-select-sm d-inline-block w-auto ml-3"
      >
        {channels.map((channel) => (
          <option key={channel.id} value={channel.id}>{channel.name}</option>
        ))};
      </select>
    </>
  );

  return (
    <>
      {renderDropdown()}
    </>
  );
};

SelectChannelDropdown.propTypes = {
  activeID: PropTypes.string,
  channels: PropTypes.arrayOf(PropTypes.shape()),
  onSelectChannel: PropTypes.func,
};

SelectChannelDropdown.defaultProps = {
  activeID: '',
  onSelectChannel: () => { Error('No callback defined for SelectChannelDropdown'); },
  channels: [],
};

export default SelectChannelDropdown;
