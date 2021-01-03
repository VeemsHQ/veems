const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const RemovePlugin = require('remove-files-webpack-plugin')
const nodeSass = require('node-sass')

module.exports = {
  devtool: 'source-map',
  entry: {
    app: './react-components/src/bundle.js',
    // styles: './core/sass/main.scss',
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
      '@assets': path.resolve(__dirname, 'assets'),
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
      },
      {
        test: /\.s?css$/i,
        use: [
          // extract to seperate file
          MiniCssExtractPlugin.loader,
          // Translates CSS into CommonJS
          {
            loader: 'css-loader',
            options: {
              sourceMap: true,
            },
          },
          {
            loader: 'resolve-url-loader',
            options: {
              sourceMap: true,
            },
          },
          // Compiles Sass to CSS
          {
            loader: 'sass-loader',
            options: {
              implementation: nodeSass,
              sourceMap: true,
              sassOptions: {
                outputStyle: 'compressed',
                includePaths: ['./node_modules/great-styles/src/scss/'],
              },
            },
          },
        ],
      },
      {
        test: /\.(jpg|png|gif|jpeg|svg)$/,
        loader: 'url-loader?limit=10000&name=img/[name].[ext]',
      },
      {
        test: /\.(woff|woff2|eot|ttf)$/,
        loader: 'url-loader?limit=10000&name=fonts/[name].[ext]',
      },
    ],
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
    }),
    new CopyWebpackPlugin([
      // { from: './node_modules/great-styles/static/images', to: 'images' },
      // { from: './node_modules/great-styles/static/fonts', to: '../../core/static/fonts/' },
      // copies the images to core/static only if not present. This avoids
      // the svg files showing up in diff every time a new build occurs
      // { from: 'react-components/dist/img/', to: '../../static/images/' },
      // { from: 'react-components/dist/fonts/', to: '../../static/fonts/' },
      // copy assets needed by CSS files as they are not automatically moved to dist foler by React
      { from: 'react-components/assets/stylesheet-assets/', to: '../../static/images/' },
    ]),
    new RemovePlugin({ after: { include: ['./react-components/dist/images/', './react-components/dist/fonts/', './react-components/dist/styles.js','./react-components/dist/styles.js.map', './react-components/dist/app.css', './react-components/dist/app.css.map'] } }),
  ],
}
