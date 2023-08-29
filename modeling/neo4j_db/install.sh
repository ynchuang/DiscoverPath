sudo add-apt-repository universe
sudo apt update
sudo apt install python3-pip
wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable 3.5' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get install neo4j=1:3.5.35
pip3 install py2neo pandas matplotlib sklearn
sudo apt install npm
npm install neovis.js
npm run build
npm run typedoc
