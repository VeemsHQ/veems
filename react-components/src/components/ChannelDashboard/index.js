import React from 'react';
import ReactDOM from 'react-dom'
import styled from 'styled-components';
import Chart from 'chart.js';

// Redux
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

// Components
import Overview from './Overview';

// Styling

export const ChannelDashboard = ({
  element,
  ...params
}) => {
  
  const DashContainer = () => {
    return (
      <Overview />
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

export default connect(null, mapDispatchToProps)(ChannelDashboard);