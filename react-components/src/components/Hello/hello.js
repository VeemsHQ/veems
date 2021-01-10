import React from 'react';
import ReactDOM from 'react-dom'

export const Hello = () => {
    return (
        <div>
            Hello world, I'm a React Component2
        </div>
    );
};

Hello.propTypes = {};

Hello.defaultProps = {};

// No idea what this does
// const mapDispatchToProps = (dispatch) => {
//     return {
//       dispatch,
//       ...bindActionCreators({}, dispatch),
//     };
//   };
// export default connect(null, mapDispatchToProps)(Hello);

export const createHello = ({ element, ...params }) => {
    ReactDOM.render(<Hello {...params} />, element)
}
