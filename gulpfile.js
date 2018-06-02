const gulp = require('gulp');
const sass = require('gulp-sass');
const spawn = require('child_process').spawn;

const PASSWORD = '1234';

gulp.task('web2py', function (done) {
  spawn('python2', [ 'web2py.py', '-a', PASSWORD, '-e' ], {
    cwd: '../..',
    stdio: 'inherit',
  })
  .on('close', (code) => {
    console.log(`Server closed with code: ${code}`);
    done(code);
  });
});

// Compile sass into CSS & auto-inject into browsers
gulp.task('sass', function() {
  return gulp.src('static/scss/styles.scss')
    .pipe(sass({
      includePaths: ['node_modules'],
      outputStyle: 'compressed',
    }).on('error', sass.logError))
    .pipe(gulp.dest('static/css'));
});

// Static Server + watching scss/html files
gulp.task('watch', function() {
  gulp.watch('static/scss/*.scss', ['sass']);
});

gulp.task('dev', ['sass', 'watch', 'web2py']);

gulp.task('default', ['dev']);
