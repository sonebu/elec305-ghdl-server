sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

sudo apt-get update
sudo apt-get install -y zip gnat make libz-dev nginx certbot python3-certbot-nginx
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip
wget -L https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-Linux-x86_64.sh
bash Miniconda3-py39_23.5.2-0-Linux-x86_64.sh -b -p ~/miniconda
rm Miniconda3-py39_23.5.2-0-Linux-x86_64.sh
echo 'export PATH="~/miniconda/bin:$PATH"' >> ~/.bashrc 
source ~/.bashrc
conda update conda -y
conda create -p ~/venv_p39/ python=3.9 -y
source activate ~/venv_p39/
pip install fastapi jinja2 uvicorn python-multipart aiofiles requests jsonlines

cd ~
git clone https://github.com/ghdl/ghdl.git
mv ghdl/ ghdl-4.0.0/
cd ghdl-4.0.0/
git checkout v4.0.0
mkdir build
cd build
../configure
make -j2 
sudo make install -j2 
