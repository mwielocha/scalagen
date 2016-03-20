#!/usr/bin/env python
# -*- coding: utf-8 -*-

from subprocess import call
import argparse
import os

parser = argparse.ArgumentParser(description='Create a scala sbt project template')

parser.add_argument('project_name', help='name of the project')

parser.add_argument('--project-version', metavar = 'project_version', help='project version', default = '1.0')

parser.add_argument('--sbt-version', metavar = 'sbt_version', help='sbt version', default = '0.13.9')
parser.add_argument('--scala-version', metavar = 'scala_version', help='scala version', default = '2.11.7')
parser.add_argument('--scalatest-version', metavar = 'scalatest_version', help='scalatest version', default = '2.2.6')

args = parser.parse_args()

build_sbt_template = '''
// Generated with scalagen

lazy val root = (project in file(".")).
  settings(
    name := "{project_name}",
    version := "{project_version}",
    scalaVersion := "{scala_version}"
  )

//mainClass in (Compile, run) := Some("...")

libraryDependencies ++= Seq(
    "org.scalatest" %% "scalatest" % "{scalatest_version}" % "test"
  )
'''

build_properties_template = '''
# Generated with scalagen
sbt.version={sbt_version}
'''

git_ignore = '''
# Generated with scalagen

target
*.class
#These can be generated back easily and could be machine dependent.

#If you're going to use IntelliJ then the following:
*.iml
*.ipr
*.iws
.idea
out

#The .idea folder and the .iml files are created and used only by IntelliJ, other IDEs will just ignore them. They can be generated easily by IntelliJ if needed, try deleting your .idea folder and then open the project in IntelliJ and, lo and behold the first thing it does is generate the .idea folder and it's contents.

#For Vim:
tags
.*.swp
.*.swo

#For Eclipse(Scala IDE):
build
.classpath
.project
.settings
org.scala-ide.sdt.core/META-INF/MANIFEST.MF
org.scala-ide.sdt.update-site/site.xml

#For OS X:
.DS_Store

# Ensime:

.ensime
.ensime_cache

# -*- mode: gitignore; -*-
*~
\#*\#
/.emacs.desktop
/.emacs.desktop.lock
*.elc
auto-save-list
tramp
.\#*

# Org-mode
.org-id-locations
*_archive

# flymake-mode
*_flymake.*

# eshell files
/eshell/history
/eshell/lastdir

# elpa packages
/elpa/

# reftex files
*.rel

# AUCTeX auto folder
/auto/

# cask packages
.cask/

# Flycheck
flycheck_*.el

# server auth directory
/server/

# projectiles files
.projectile

'''

params = vars(args)

build_sbt = build_sbt_template.format(**params)
build_properties = build_properties_template.format(**params)

os.makedirs('./project')

os.makedirs('./src/main/scala')
os.makedirs('./src/main/resources')

os.makedirs('./src/test/scala')
os.makedirs('./src/test/resources')

print >>open('./.gitignore', 'w+'), git_ignore
print >>open('./build.sbt', 'w+'), build_sbt
print >>open('./project/build.properties', 'w+'), build_properties
print >>open('./project/plugins.sbt', 'w+'), ''

call(['sbt', 'test'])

print 'Generated project {project_name} for Scala {scala_version} and sbt {sbt_version}.'.format(**params)
