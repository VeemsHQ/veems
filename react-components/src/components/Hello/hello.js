import React from 'react';
import ReactDOM from 'react-dom'
import PropTypes from 'prop-types';
import styled from 'styled-components';

// Redux
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';

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

export const Hello = ({
  children,
  ...props
}) => {
  return (
    <Container {...props}>
      Hello world, I'm a React Component
    </Container>
  );
};

/** Props Types */
Hello.propTypes = {
};

/** Default Props. */
Hello.defaultProps = {
};

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch,
    ...bindActionCreators({}, dispatch),
  };
};

// No idea what this does
// export default connect(null, mapDispatchToProps)(Hello);

export const createHello = ({ element, ...params }) => {
    ReactDOM.render(<Hello {...params} />, element)
  }
