import os

SOURCES = {
    'dependencies': [
        'gulp',
        'gulp-sass',
        'browser-sync',
        'gulp-concat',
        'gulp-uglify',
        'gulp-clean-css',
        'gulp-autoprefixer',
        'del',
        'gulp-concat-css',
        'gulp-babel',
        'gulp-pug',
        'gulp-imagemin',
        'imagemin-pngquant',
        '@babel/core',
        '@babel/cli',
        '@babel/preset-env',
        'jquery',
        'bootstrap'
    ],
    'gulpfile': """let gulp          = require('gulp'),
		sass          = require('gulp-sass'),
		browserSync   = require('browser-sync'),
		concat        = require('gulp-concat'),
		uglify        = require('gulp-uglify'),
		cleancss      = require('gulp-clean-css'),
		autoprefixer  = require('gulp-autoprefixer'),
		del           = require('del'),
    concatcss     = require('gulp-concat-css'),
		babel 				= require('gulp-babel'),
		pug 					= require('gulp-pug'),
		imagemin			= require('gulp-imagemin'),
 		pngquant 			= require('imagemin-pngquant');

gulp.task('styles', function() {
	return gulp.src('src/sass/**/*.sass')
	.pipe(sass({ outputStyle: 'expanded' }))
  .pipe(concatcss('style.min.css'))
	.pipe(autoprefixer(['last 15 versions']))
	.pipe(cleancss( {level: { 1: { specialComments: 0 } } }))
  .pipe(gulp.dest('src/css/'))
});

gulp.task('libstyles', () => {
	return gulp.src([
		'node_modules/bootstrap/dist/css/bootstrap.min.css'
	])
	.pipe(concatcss('libs.min.css'))
	.pipe(cleancss( {level: { 1: { specialComments: 0 } } }))
	.pipe(gulp.dest('src/css/'))
})

gulp.task('scripts', function() {
	return gulp.src('src/srcjs/**/*.js')
	.pipe(concat('index.min.js'))
	.pipe(babel({
		presets: ['@babel/env']
	}))
	.pipe(uglify())
	.pipe(gulp.dest('src/js'))
});

gulp.task('libscripts', (done) => {
	let jslibs = [
		'node_modules/jquery/dist/jquery.min.js'
	];
	return gulp.src(jslibs)
	.pipe(concat('libs.min.js'))
	.pipe(uglify())
	.pipe(gulp.dest('src/js'))

})


gulp.task('pug', function() {
	return gulp.src(['!src/pug/_*.pug', 'src/pug/*.pug'])
	.pipe(pug({
		pretty: true
	}))
	.pipe(gulp.dest('src/'))
});

gulp.task('deldist', () => {
	return new Promise((resolve, reject) => {
		del('dist');
		resolve();
	});
})

gulp.task('bundle', (done) => {
  let html  = gulp.src('src/*.html')
  .pipe(gulp.dest('dist/'))

  let css   = gulp.src('src/css/*')
  .pipe(gulp.dest('dist/css'))

  let js    = gulp.src('src/js/*')
  .pipe(gulp.dest('dist/js'))

	let img 	= gulp.src('src/img/**/*')
	.pipe(imagemin({
		interlaced: true,
		progressive: true,
		svgoPlugins: [
			{
				removeViewBox: false
			}
		],
		une: [pngquant()]
	}))
	.pipe(gulp.dest('./dist/img'))

  done();
})

gulp.task('reload', browserSync.reload)

gulp.task('server', function(done) {

	browserSync({
		server: {
			baseDir: 'src'
		},
		notify: false,
		open: false,
		// online: false, // Work Offline Without Internet Connection
		// tunnel: true, tunnel: "projectname", // Demonstration page: http://projectname.localtunnel.me
	})


	gulp.watch('src/sass/**/*.sass').on('change', gulp.series('styles', 'reload'))

	gulp.watch('src/srcjs/**/*.js').on('change', gulp.series('scripts', 'reload'))

	gulp.watch('src/pug/**/*.pug').on('change', gulp.series('pug'))

	gulp.watch('src/**/*.html').on('change', browserSync.reload);

	done();
});


gulp.task('start', gulp.series(
	'styles',
	'scripts',
	'pug',
	'libscripts',
	'libstyles',
	'server'
));

gulp.task('build', gulp.series(
	'deldist',
	'styles',
	'scripts',
	'pug',
	'libscripts',
	'libstyles',
	'bundle'
));
""",
    'js': 'console.log(...[\'from\', \'index.js\']);',
    'sass': 'body\n\tbackground: #ddf',
    'media_sass': '@media (max-width: 1200px)\n\t// media',
    'layout_pug': """<!DOCTYPE html>
  html(lang="en")
    head
      meta(charset="UTF-8")
      meta(name="viewport", content="width=device-width, initial-scale=1.0")
      meta(http-equiv="X-UA-Compatible", content="ie=edge")
      title Document
      link(rel="stylesheet", href="/css/style.min.css")
      link(rel="stylesheet", href="/css/libs.min.css")
    body
      header
        p header
      main
        block main
      footer
        p footer

      script(src="/js/libs.min.js")
      script(src="/js/index.min.js")
""",
    'pug': """extends layout/layout.pug

block main
  h3.title main
"""
}

PRIMARY_CWD = os.getcwd()

def create_folder(name):
    os.mkdir(name)
    os.chdir(name)

def write_file(file, content):
    with open(file, 'w') as f:
        f.write(content)


def main():
    os.system('npm init')

    write_file('.npmrc', 'package-lock=false')

    write_file('gulpfile.js', SOURCES['gulpfile'])

    create_folder('src')

    create_folder('sass')
    write_file('style.sass', SOURCES['sass'])
    write_file('media.sass', SOURCES['media_sass'])
    os.chdir('..')

    create_folder('img')
    os.chdir('..')

    create_folder('pug')
    write_file('index.pug', SOURCES['pug'])
    create_folder('layout')
    write_file('layout.pug', SOURCES['layout_pug'])
    os.chdir('../..')

    create_folder('srcjs')
    write_file('index.js', SOURCES['js'])
    os.chdir('..')

    os.chdir('..')

    for dep in SOURCES['dependencies']:
        os.system('npm i '+dep)

    os.system('gulp start')

if __name__ == '__main__':
    main()
