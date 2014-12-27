'use strict';

var gulp = require('gulp')
  , gutil = require('gulp-util')
  , sass = require('gulp-sass')
  , autoprefix = require('gulp-autoprefixer')
  , notify = require('gulp-notify')
  , bower = require('gulp-bower')
  , shell = require('gulp-shell')
  , uglify = require('gulp-uglifyjs');

var config = {
  staticPath: './tank_maven/static',
  sassPath: './tank_maven/static/scss',
  bowerDir: './bower_components'
};

var javascripts = [
  config.bowerDir + '/jquery/dist/jquery.js',
  config.bowerDir + '/bootstrap-sass-official/assets/javascripts/bootstrap.js',
  config.bowerDir + '/d3/d3.js',
  config.bowerDir + '/rickshaw/rickshaw.js'
];

// ----------------------------------------------------------------

/**
 * Run bower
 */
gulp.task('bower', function () {
  return bower()
    .pipe(gulp.dest(config.bowerDir))
});

// ----------------------------------------------------------------

/**
 * Deal with font awesome fonts
 */
gulp.task('fonts', function () {
  return gulp.src(config.bowerDir + '/fontawesome/fonts/**.*')
    .pipe(gulp.dest(config.staticPath + '/fonts'));
});

// ----------------------------------------------------------------

/**
 * Bootstrap fonts / images
 */
gulp.task('bootstrap-fonts', function () {
  return gulp.src(config.bowerDir + '/bootstrap-sass-official/assets/fonts/bootstrap/**.*')
    .pipe(gulp.dest(config.staticPath + '/fonts/bootstrap'));

});


// ----------------------------------------------------------------

/**
 * Build sass
 */
gulp.task('sass', function () {
  gulp.src(config.sassPath + '/app.scss')
    .pipe(sass({
      'includePaths': [
          config.staticPath + '/scss',
          config.bowerDir + '/bootstrap-sass-official/assets/stylesheets',
          config.bowerDir + '/fontawesome/scss',
      ],
      'outputStyle': 'expanded',
      'sourceComments': 'map',
      'errLogToConsole': true
    }))
    .pipe(gulp.dest(config.staticPath + '/css/'));

  gulp.src(config.bowerDir + '/rickshaw/rickshaw.css')
    .pipe(gulp.dest(config.staticPath + '/css/'));

});

// ----------------------------------------------------------------

/**
 * Javascript
 */
gulp.task('js', function () {
  gulp.src(javascripts)
    .pipe(uglify('app.js', {
      mangle: false,
      compress: false
    }))
    .pipe(gulp.dest(config.staticPath + '/js/'));
});

// ----------------------------------------------------------------

/**
 * Watch files
 */
gulp.task('watch', function () {
  gulp.watch(config.sassPath + '/**/*.scss', ['sass']);
});

// ----------------------------------------------------------------

/**
 * Serve the python app
 */
gulp.task('server', shell.task([
    'python tank_maven/app.py'
]));

// ----------------------------------------------------------------

/**
 * Default task
 */
gulp.task('default', ['fonts', 'sass', 'js', 'bootstrap-fonts']);
gulp.task('serve', [
  'fonts', 'sass', 'js', 'bootstrap-fonts',
  'server', 'watch'
]);

