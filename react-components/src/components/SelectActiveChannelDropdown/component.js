import React from 'react';

import 'regenerator-runtime/runtime.js';

export const SelectActiveChannelDropdown = ({
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

// SelectActiveChannelDropdown.propTypes = {
//   activeID: PropTypes.string,
//   channels: PropTypes.arrayOf(PropTypes.shape()),
//   onSelectChannel: PropTypes.func,
// };

// SelectActiveChannelDropdown.defaultProps = {
//   activeID: '',
//   onSelectChannel: () => { Error('No callback defined for SelectActiveChannelDropdown'); },
//   channels: [],
// };

export default SelectActiveChannelDropdown;
