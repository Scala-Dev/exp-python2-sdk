
set -e

sudo add-apt-repository ppa:nginx/stable -y
sudo apt-get update
sudo apt-get install nginx


cd ..
git clone git@github.com:scalainc/exp-api.git
cd exp-api
git checkout eagle
git pull origin eagle
npm install
NODE_ENV=test npm start&
sleep 10
cd ..
git clone git@github.com:scalainc/exp-network.git
cd exp-network
git checkout eagle
git pull origin eagle
npm install
npm start&
sleep 10
cd ..
git clone git@github.com:scalainc/exp-gateway.git
cd exp-gateway
git checkout eagle
git pull origin eagle
./start.sh&
sleep 10

cd ../exp-python2-sdk
