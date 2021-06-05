# Infrastructure setup

1. Download and install [vagrant](https://www.vagrantup.com/) and  [virtualbox](https://www.virtualbox.org/)

2. Check if vagrant is successfully installed
```
vagrant version
```
### Create a virtual machine
1. Create a sub directory and init the vagrant config file
```
mkdir -p  ~/Documents/vms/vm-name
cd ~/Documents/vms/vm-name
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