import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

// Redux
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

// Components

// Styling
export const Container = styled.div`
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 120px 70% 180px;
    height: 100vh;
    width: 100vw;
    box-sizing: border-box;
    padding: 100px 10% 100px 10%;
`;

export const Customisation = ({
  children,
  ...props
}) => {
  return (
    <Container {...props}>
      {children}
      <Play />
    </Container>
  );
};

/** Props Types */
Customisation.propTypes = {
};

/** Default Props. */
Customisation.defaultProps = {
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({}, dispatch),
  };
};

export default connect(null, mapDispatchToProps)(Customisation);
