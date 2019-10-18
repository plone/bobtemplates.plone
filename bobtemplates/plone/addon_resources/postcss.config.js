module.exports = {
  plugins: [
    require('autoprefixer')({
      grid: true,
    }),
    require('postcss-flexbugs-fixes')(),
    require('cssnano')({
      preset: 'default',
    }),
  ],
};
