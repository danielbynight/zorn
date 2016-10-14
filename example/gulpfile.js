'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var cleanCSS = require('gulp-clean-css');
var rename = require("gulp-rename");

//  CSS

gulp.task('sass', function () {
  return gulp.src('./scss/main.scss')
    .pipe(sass()
    .on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(rename('main.css'))
    .pipe(gulp.dest('./'));
});

// Compile for production environment

gulp.task('prod', function() {
  return gulp.src('./main.css')
    .pipe(cleanCSS({compatibility: 'ie8'}))
    .pipe(rename('main.min.css'))
    .pipe(gulp.dest('./'));
});

 // Watch

gulp.task('watch', function () {
  gulp.watch('./scss/**/*.scss', ['sass', 'prod']);
});

// Default

gulp.task('default', ['sass', 'prod']);