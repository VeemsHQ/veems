import React from 'react';
import { shallow } from 'enzyme';


// Component to be tested
import { Upload } from '.';

const setUp = (props = {}) => {
  const component = shallow(<Upload {...props} />);
  return component;
};

describe('Upload-Component', () => {
  let component;
  beforeEach(() => {
    const props = {
    };
    component = setUp(props);
  });

  it('Should render without errors', () => {
    expect(component.exists()).toBe(true);
  });
});
