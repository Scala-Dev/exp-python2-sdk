
set -e

cd ..
git clone git@github.com:scalainc/exp-api.git
cd exp-api
git checkout develop
git pull origin develop
npm install
NODE_ENV=test npm start&
sleep 10
cd ..
git clone git@github.com:scalainc/exp-network.git
cd exp-network
git checkout develop
git pull origin develop
npm install
npm start&
sleep 10
cd ../exp-js-sdk
npm run build
