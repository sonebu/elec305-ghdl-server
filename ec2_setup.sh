sudo apt-get update
sudo apt-get install -y zip
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
pip install fastapi jinja2 uvicorn python-multipart aiofiles requests
