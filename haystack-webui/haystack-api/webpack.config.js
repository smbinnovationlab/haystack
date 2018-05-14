"use strict";

var path = require("path");
var webpack = require("webpack");

module.exports = {
	entry: ["./src/index.js"],
	output: {
		path: __dirname + "/build",
		publicPath: "/assets/",
		filename: "bundle.js"
	},
	module: {
		loaders: [
			{
				test: /\.js$/,
				loader: "babel-loader",
				include: [path.resolve(__dirname, "src")],
				query: {
					presets: ["react", "es2015"],
					plugins: [
						["import", { "libraryName": "antd", "style": true }]
					]
				}
			},
			{
				test: /\.less$/,
				use: [
					require.resolve('style-loader'),
					{
						loader: require.resolve('css-loader'),
						options: {
							importLoaders: 1,
						},
					},
					{
						loader: require.resolve('less-loader'),
						options: {
							modifyVars: {
								'@icon-url': '"/src/iconfont/iconfont"',
							},
						},
					},
				],
    		},
		],
	},
	plugins: [
  		new webpack.ProvidePlugin({
    		"React": "react",
    		"ReactDOM": "react-dom",
  		}),
  		new webpack.ProvidePlugin({
            $: "jquery"
        }),
  		new webpack.ProvidePlugin({
            "Highlight": "react-highlight"
        }),
	],
};