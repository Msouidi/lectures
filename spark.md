# Spark

### Setup the infrastructure
1. Download and install [vagrant](https://www.vagrantup.com/) and  [virtualbox](https://www.virtualbox.org/)

2. Check if vagrant is successfully installed
```
vagrant version
```
### Create spark virtual machine
1. Create a sub directory and init the vagrant config file
```
mkdir -p  ~/Documents/vms/spark
cd ~/Documents/vms/spark
vagrant init bento/ubuntu-18.04
```
2. Edit the config file (uncomment the IP address section) 
```
vi Vagrantfile
config.vm.network "private_network", ip: "192.168.33.12"
```
3. Bootup the virtual machine
```
vagrant up
vagrant ssh
```

### Install Spark
1. Install Jupyter
```
sudo rm -rf /usr/bin/python
sudo ln -s /usr/bin/python3 /usr/bin/python
sudo apt update
sudo apt install python3-pip
pip3 install jupyter
export PATH=$PATH:~/.local/bin

jupyter notebook --generate-config
vi ~/.jupyter/jupyter_notebook_config.py
# uncomment the line below and put the correct IP address
c.NotebookApp.ip = '@IP’
```
2. Install Java
```
sudo apt install openjdk-8-jdk
```

3. Install spark
```
wget https://downloads.apache.org/spark/spark-2.4.8/spark-2.4.8-bin-hadoop2.7.tgz
tar -xzf spark-2.4.8-bin-hadoop2.7.tgz
sudo mv spark-2.4.8-bin-hadoop2.7 /usr/local/spark
```

4. Edit the bashrc file
   
Add thte following line to end of the file ~/.bashrc
```
#SPARK VARIABLES START
export SPARK_HOME=/usr/local/spark
export PATH=$SPARK_HOME/bin:$PATH
export PYSPARK_DRIVER_PYTHON=jupyter
export PYSPARK_DRIVER_PYTHON_OPTS='notebook'
export PATH=$PATH:~/.local/bin
#SPARK VARIABLE END
```
5. Source the new config
```
source ~/.bashrc
```
6. Start spark
```
pyspark
```