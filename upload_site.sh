#!/bin/bash
rm -rf compiled
ruhoh compile
cd compiled
git init .
git add .
git commit -m "update blog"
git push https://github.com/abulimov/abulimov.github.io.git master:master --force
cd ..
