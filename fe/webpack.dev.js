const path = require( 'path' );
const webpack = require( 'webpack' );
const WebpackBar = require( 'webpackbar' )
const MiniCssExtractPlugin = require( 'mini-css-extract-plugin' );
const Dotenv = require( 'dotenv-webpack' );
const NodePolyfillPlugin = require( 'node-polyfill-webpack-plugin' )

module.exports = {
  mode : 'development',
  output : { path : `${__dirname}/dist`, filename : 'bundle.js' },
  watch : true,
  watchOptions : { ignored : /node_modules/ },
  devServer : {
    allowedHosts : 'all',
    static : [  {
      directory : path.join( __dirname, 'src' )
    } ],
    // noInfo : true,
    // stats : 'minimal'
  },
  module : {
    rules : [
        {
        test : /.jsx?$/,
        loader : 'babel-loader',
        exclude : /node_modules/,
        },
        /* This will put all css, less, styles through CSS Modules' localization except global-style.less */
        
        {
          test : [ /\.css$/ ],
          use : [ 'style-loader', 'css-loader' ]
        }
    ]
  },
  resolve : {
    extensions : [ '*', '.js', '.jsx', '.css' ]
  },
  // Necessary plugins for hot load
  plugins : [
    new NodePolyfillPlugin(),
    new webpack.HotModuleReplacementPlugin(),
    new WebpackBar(),
    new webpack.NoEmitOnErrorsPlugin(),
    new MiniCssExtractPlugin( { filename : 'style.css' } ),
    //    new MiniCssExtractPlugin( 'style.css', { allChunks : true } ),
    new Dotenv( {
      path : './.env', // Path to .env file (this is the default)
    } ),
    new webpack.LoaderOptionsPlugin( {
      options : {
        context : __dirname,
        postcss : []
      }
    } )
  ],
}
