Installing Mongodb on Fedora30 and above
=========================================

* Due to licensing changes, Fedora no longer ships mongodb in 30 and above.
* These steps will also setup the mongodb-tools (mongodump, mongorestore etc).

    * [Download MongoDB Binaries](#download-mongodb-binaries)
    * [Extract and Setup MongoDB Binaries](#extract-and-setup-mongodb-binaries)
    * [Create MongoDB Service User](#create-mongodb-service-user)
    * [Setup and Enable MongoDB System Service](#setup-and-enable-mongodb-system-service)

## Download MongoDB Binaries
   - Download the appropriate binaries from [MongoDB sources](https://www.mongodb.com/download-center/community)
   - For Fedora30+ we will choose from the 4.x series: 'server' and 'Linux 64-bit Legacy x64'

![download_mongodb](../image/download-mongodb?raw=true)

## Extract and Setup MongoDB Binaries
   - The below commands will assume the current version is 4.0.9

```
curl https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-4.0.9.tgz -o /tmp/mongodb-linux-x86_64-4.0.9.tgz
```

```
tar -xvf /tmp/mongodb-linux-x86_64-4.0.9.tgz -C /tmp/

```

   - Now copy the binaries into a proper $PATH

   - **If you just want the mongodump and mongorestore tools**

```
cp /tmp/mongodb-linux-x86_64-4.0.9/bin/{mongodump,mongorestore,mongoreplay,bsondump} /usr/bin/
```

   - **If you are installing mongodb-server and everything else**

```
cp /tmp/mongodb-linux-x86_64-4.0.9/bin/* /usr/bin/
```

## Create Mongodb Service User
   - We want to run mongodb as an unprivileged service user
   - We're also going to set the home directory to `/var/lib/mongodb`
   - This will give the mongodb group a gid of 992 and mongodb user a uid of 184

```
useradd -m -d /var/lib/mongodb -c "MongoDB Database Server" -u 184 -g 992 -s /sbin/nologin mongodb
```

## Setup and Enable MongoDB System Service
   - Now you'll want to install a systemd unit for Mongo and drop in generic configs.

```
cat > /etc/sysconfig/mongod <<EOF
OPTIONS="-f /etc/mongod.conf"

   - Mongod options file

# To run numactl before starting mongodb server
# https://docs.mongodb.com/manual/administration/production-notes/#configuring-numa-on-linux
#NUMACTL="/usr/bin/numactl --interleave=all"

EOF
```

   - Mongd.conf

```
cat > /etc/mongod.conf <<EOF
systemLog:
  verbosity: 0
  destination: file
  path: /var/log/mongodb/mongod.log
  logAppend: true
  logRotate: reopen

processManagement:
  fork: true
  pidFilePath: /var/run/mongodb/mongod.pid

net:
  port: 27017
  unixDomainSocket:
    enabled: true
    pathPrefix: /var/run/mongodb

storage:
  dbPath: /var/lib/mongodb
  engine: wiredTiger

processManagement:
  fork: true
  pidFilePath: /var/run/mongodb/mongod.pid

net:
  port: 27017

  unixDomainSocket:
    enabled: true
    pathPrefix: /var/run/mongodb

storage:
  dbPath: /var/lib/mongodb
  engine: wiredTiger

EOF
```

   - Now setup and install your systemd unit file

```
cat > /usr/lib/systemd/system/mongod.service <<EOF
[Unit]
Description=High-performance, schema-free document-oriented database
After=syslog.target network.target

[Service]
Type=forking
User=mongodb
EnvironmentFile=/etc/sysconfig/mongod
ExecStart=/bin/sh -c "exec $NUMACTL /usr/bin/mongod $OPTIONS run"
PrivateTmp=true
LimitNOFILE=64000
TimeoutStartSec=180

[Install]
WantedBy=multi-user.target

EOF
```

   - Enable and start the service

```
systemctl enable mongod
systemctl start mongod
```
