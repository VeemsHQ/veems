const path = require('path');

module.exports = {
  devtool: 'source-map',
  entry: {
    app: './react-components/src/bundle.js',
  },
  output: {
    path: path.resolve(__dirname, 'dist'),
    filename: '[name].js',
    publicPath: '',
    library: '[name]',
    libraryExport: 'default',
    libraryTarget: 'var',
  },
  resolve: {
    extensions: ['.js', '.jsx'],
    alias: {
      '@src': path.resolve(__dirname, 'src'),
    },
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        loader: 'babel-loader',
        options: {
          presets: [
            '@babel/preset-env',
            '@babel/react',
            {
              plugins: ['@babel/plugin-proposal-class-properties'],
            },
          ],
        },
        exclude: /node_modules/,
      }
    ],
  },
  plugins: [],
}
