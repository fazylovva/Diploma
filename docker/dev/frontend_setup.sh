#!/bin/sh

# shellcheck disable=SC2164
cd frontend/app
npm install
# yarn install
# yarn serve --host 0.0.0.0
npm build --watch --mode=production