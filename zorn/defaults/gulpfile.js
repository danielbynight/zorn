'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var cleanCSS = require('gulp-clean-css');
var rename = require('gulp-rename');
var shell = require('gulp-shell')

//  CSS

gulp.task('sass', function () {
  return gulp.src('./scss/main.scss')
    .pipe(sass()
    .on('error', sass.logError))
    .pipe(autoprefixer())
    .pipe(rename('main.css'))
    .pipe(gulp.dest('./'));
});

// Content

gulp.task('generate', shell.task(['python3 admin.py generate']))

// Compile for production environment

gulp.task('prod', function() {
  return gulp.src('./main.css')
    .pipe(cleanCSS({compatibility: 'ie8'}))
    .pipe(rename('main.min.css'))
    .pipe(gulp.dest('./'));
});

// Watch

gulp.task('watch', function () {
  gulp.watch(
    ['./scss/**/*.scss', 'settings.py', './**/*.md'],
    ['sass', 'prod', 'generate']
  );
});

// Default

gulp.task('default', ['sass', 'prod', 'generate']);