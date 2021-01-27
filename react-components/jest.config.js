  
module.exports = {
  moduleFileExtensions: ['js', 'jsx'],
  moduleNameMapper: {
    '\\.(jpg|jpeg|png|gif|eot|otf|webp|svg|ttf|woff|woff2|mp4|webm|wav|mp3|m4a|aac|oga)$':
      '<rootDir>/react-components/tests/imageMock.js',
    '^.+\\.(css|scss)$': '<rootDir>/react-components/tests/css-stub.js',
    '^@src(.*)$': '<rootDir>/react-components/src/$1',
    '^@assets(.*)$': '<rootDir>/react-components/assets/$1',
    '^@components(.*)$':
      '<rootDir>/node_modules/great-styles/dist/components/$1',
  },
  moduleDirectories: ['node_modules', 'src'],
  transform: {
    '^.+\\.jsx?$': 'babel-jest',
  },
  setupFilesAfterEnv: [
    '<rootDir>/react-components/setupEnzyme.js',
    '<rootDir>/react-components/setupJest.js',
  ],
  testEnvironment: 'jest-environment-jsdom-fifteen',
}